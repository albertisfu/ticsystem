from __future__ import unicode_literals
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
try:
    from django.contrib.auth import get_user_model  # Django 1.5
except ImportError:
    from postman.future_1_5 import get_user_model
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
try:
    from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit  # Django 1.4.11, 1.5.5
except ImportError:
    from urlparse import urlsplit, urlunsplit
try:
    from django.utils.timezone import now  # Django 1.4 aware datetimes
except ImportError:
    from datetime import datetime
    now = datetime.now
from django.utils.translation import ugettext as _, ugettext_lazy as lz_
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView, TemplateView, View
from django.views.generic import CreateView, DeleteView, ListView

from postman.fields import autocompleter_app
from postman.views import ComposeMixin #importamos solo las funciones requeridas aqui
from postman.forms import WriteForm, AnonymousWriteForm, QuickReplyForm, FullReplyForm
from postman.models import Message, get_order_by
from postman.utils import format_subject, format_body
from forms import *
from fileupload.models import Picture
from fileupload.response import JSONResponse, response_mimetype
from fileupload.serialize import serialize

login_required_m = method_decorator(login_required)
csrf_protect_m = method_decorator(csrf_protect)


##########
# Helpers
##########
def _get_referer(request):
    """Return the HTTP_REFERER, if existing."""
    if 'HTTP_REFERER' in request.META:
        sr = urlsplit(request.META['HTTP_REFERER'])
        return urlunsplit(('', '', sr.path, sr.query, sr.fragment))


########
# Views
########

class PictureCreateView(CreateView): #clase para recibir llamada post  de imagen subida
    model = Picture
    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')

class WriteView(ComposeMixin, FormView):

    form_classes = (WriteFormImageForm, AnonymousWriteForm)
    autocomplete_channels = None
    template_name = 'postman/write.html'

    @csrf_protect_m
    def dispatch(self, *args, **kwargs):
        if getattr(settings, 'POSTMAN_DISALLOW_ANONYMOUS', False):
            return login_required(super(WriteView, self).dispatch)(*args, **kwargs)
        return super(WriteView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        return self.form_classes[0] if self.request.user.is_authenticated() else self.form_classes[1]

    def get_initial(self):
        initial = super(WriteView, self).get_initial()
        if self.request.method == 'GET':
            initial.update(self.request.GET.items())  # allow optional initializations by query string
            recipients = self.kwargs.get('recipients')
            if recipients:
                # order_by() is not mandatory, but: a) it doesn't hurt; b) it eases the test suite
                # and anyway the original ordering cannot be respected.
                user_model = get_user_model()
                usernames = list(user_model.objects.values_list(user_model.USERNAME_FIELD, flat=True).filter(
                    is_active=True,
                    **{'{0}__in'.format(user_model.USERNAME_FIELD): [r.strip() for r in recipients.split(':') if r and not r.isspace()]}
                ).order_by(user_model.USERNAME_FIELD))
                if usernames:
                    initial['recipients'] = ', '.join(usernames)
        return initial

    def get_form_kwargs(self):
        kwargs = super(WriteView, self).get_form_kwargs()
        if isinstance(self.autocomplete_channels, tuple) and len(self.autocomplete_channels) == 2:
            channel = self.autocomplete_channels[self.request.user.is_anonymous()]
        else:
            channel = self.autocomplete_channels
        kwargs['channel'] = channel
        return kwargs



class ReplyView(ComposeMixin, FormView):
    """
    Display a form to compose a reply.

    Optional attributes:
        ``form_class``: the form class to use
        ``formatters``: a 2-tuple of functions to prefill the subject and body fields
        ``autocomplete_channel``: a channel name
        ``template_name``: the name of the template to use
        + those of ComposeMixin

    """
    form_class = FullReplyImageForm
    formatters = (format_subject, format_body)
    autocomplete_channel = None
    template_name = 'postman/reply.html'

    @csrf_protect_m
    @login_required_m
    def dispatch(self, request, message_id, *args, **kwargs):
        perms = Message.objects.perms(request.user)
        self.parent = get_object_or_404(Message, perms, pk=message_id)
        return super(ReplyView, self).dispatch(request,*args, **kwargs)

    def get_initial(self):
        self.initial = self.parent.quote(*self.formatters)  # will also be partially used in get_form_kwargs()
        if self.request.method == 'GET':
            self.initial.update(self.request.GET.items())  # allow overwriting of the defaults by query string
        return self.initial

    def get_form_kwargs(self):
        kwargs = super(ReplyView, self).get_form_kwargs()
        kwargs['channel'] = self.autocomplete_channel
        if self.request.method == 'POST':
            if 'subject' not in kwargs['data']:  # case of the quick reply form
                post = kwargs['data'].copy()  # self.request.POST is immutable
                post['subject'] = self.initial['subject']
                kwargs['data'] = post
            kwargs['recipient'] = self.parent.sender or self.parent.email
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ReplyView, self).get_context_data(**kwargs)
        context['recipient'] = self.parent.obfuscated_sender
        return context


class DisplayMixin(object):
    """
    Code common to the by-message and by-conversation views.

    Optional attributes:
        ``form_class``: the form class to use
        ``formatters``: a 2-tuple of functions to prefill the subject and body fields
        ``template_name``: the name of the template to use

    """
    http_method_names = ['get']
    form_class = QuickReplyFormImage
    formatters = (format_subject, format_body if getattr(settings, 'POSTMAN_QUICKREPLY_QUOTE_BODY', False) else None)
    template_name = 'postman/view.html'
    

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(DisplayMixin, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        self.msgs = Message.objects.thread(user, self.filter)
        if not self.msgs:
            raise Http404
        Message.objects.set_read(user, self.filter)
        return super(DisplayMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DisplayMixin, self).get_context_data(**kwargs)
        user = self.request.user
        # are all messages archived ?
        for m in self.msgs:
            if not getattr(m, ('sender' if m.sender == user else 'recipient') + '_archived'):
                archived = False
                break
        else:
            archived = True
        # look for the most recent received message (and non-deleted to comply with the future perms() control), if any
        for m in reversed(self.msgs):
            if m.recipient == user and not m.recipient_deleted_at:
                received = m
                break
        else:
            received = None
        context.update({
            'pm_messages': self.msgs,
            'archived': archived,
            'reply_to_pk': received.pk if received else None,
            'form': self.form_class(initial=received.quote(*self.formatters)) if received else None,
            'next_url': self.request.GET.get('next') or reverse('postman_inbox'),
        })
        return context


class MessageView(DisplayMixin, TemplateView):
    """Display one specific message."""
    def get(self, request, message_id, *args, **kwargs):
        self.filter = Q(pk=message_id)
        return super(MessageView, self).get(request, *args, **kwargs)


class ConversationView(DisplayMixin, TemplateView):
    """Display a conversation."""
    def get(self, request, thread_id, *args, **kwargs):
        self.filter = Q(thread=thread_id)
        return super(ConversationView, self).get(request, *args, **kwargs)
