from __future__ import unicode_literals
from models import *
from postman.models import Message
from fileupload.models import *
from django import forms
from django.conf import settings
try:
    from django.contrib.auth import get_user_model  # Django 1.5
except ImportError:
    from postman.future_1_5 import get_user_model
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _

from postman.fields import CommaSeparatedUserField
from postman.models import Message
from postman.utils import WRAP_WIDTH


class BaseWriteForm(forms.ModelForm):
    """The base class for other forms."""
    class Meta:
        model = Message
        fields = ('body',)
        widgets = {
            # for better confort, ensure a 'cols' of at least
            # the 'width' of the body quote formatter.
            'body': forms.Textarea(attrs={'cols': WRAP_WIDTH, 'rows': 12}),
        }

    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)
        exchange_filter = kwargs.pop('exchange_filter', None)
        user_filter = kwargs.pop('user_filter', None)
        max = kwargs.pop('max', None)
        channel = kwargs.pop('channel', None)
        self.site = kwargs.pop('site', None)
        super(BaseWriteForm, self).__init__(*args, **kwargs)

        self.instance.sender = sender if (sender and sender.is_authenticated()) else None
        if exchange_filter:
            self.exchange_filter = exchange_filter
        if 'recipients' in self.fields:
            if user_filter and hasattr(self.fields['recipients'], 'user_filter'):
                self.fields['recipients'].user_filter = user_filter

            if getattr(settings, 'POSTMAN_DISALLOW_MULTIRECIPIENTS', False):
                max = 1
            if max is not None and hasattr(self.fields['recipients'], 'set_max') \
            and getattr(self, 'can_overwrite_limits', True):
                self.fields['recipients'].set_max(max)

            if channel and hasattr(self.fields['recipients'], 'set_arg'):
                self.fields['recipients'].set_arg(channel)

    error_messages = {
        'filtered': _("Writing to some users is not possible: {users}."),
        'filtered_user': _("{username}"),
        'filtered_user_with_reason': _("{username} ({reason})"),
    }
    def clean_recipients(self):
        """Check no filter prohibit the exchange."""
        recipients = self.cleaned_data['recipients']
        exchange_filter = getattr(self, 'exchange_filter', None)
        if exchange_filter:
            errors = []
            filtered_names = []
            recipients_list = recipients[:]
            for u in recipients_list:
                try:
                    reason = exchange_filter(self.instance.sender, u, recipients_list)
                    if reason is not None:
                        recipients.remove(u)
                        filtered_names.append(
                            self.error_messages[
                                'filtered_user_with_reason' if reason else 'filtered_user'
                            ].format(username=u.get_username(), reason=reason)
                        )
                except forms.ValidationError as e:
                    recipients.remove(u)
                    errors.extend(e.messages)
            if filtered_names:
                errors.append(self.error_messages['filtered'].format(users=', '.join(filtered_names)))
            if errors:
                raise forms.ValidationError(errors)
        return recipients
    def save(self, recipient=None, parent=None, auto_moderators=[]):
        """
        Save as many messages as there are recipients.

        Additional actions:
        - If it's a reply, build a conversation
        - Call auto-moderators
        - Notify parties if needed

        Return False if one of the messages is rejected.

        """
            
        recipients = self.cleaned_data.get('recipients', [])
        if parent and not parent.thread_id:  # at the very first reply, make it a conversation
            parent.thread = parent
            parent.save()
            # but delay the setting of parent.replied_at to the moderation step
        if parent:
            self.instance.parent = parent
            self.instance.thread_id = parent.thread_id
        initial_moderation = self.instance.get_moderation()
        initial_dates = self.instance.get_dates()
        initial_status = self.instance.moderation_status
        if recipient:
            if isinstance(recipient, get_user_model()) and recipient in recipients:
                recipients.remove(recipient)
            recipients.insert(0, recipient)
        is_successful = True
        for r in recipients:
            if isinstance(r, get_user_model()):
                self.instance.recipient = r
            else:
                self.instance.recipient = None
                self.instance.email = r
            self.instance.pk = None  # force_insert=True is not accessible from here
            self.instance.auto_moderate(auto_moderators)
            self.instance.clean_moderation(initial_status)
            self.instance.clean_for_visitor()
            m = super(BaseWriteForm, self).save()
            if self.instance.is_rejected():
                is_successful = False
            self.instance.update_parent(initial_status)
            self.instance.notify_users(initial_status, self.site)
            # some resets for next reuse
            if not isinstance(r, get_user_model()):
                self.instance.email = ''
            self.instance.set_moderation(*initial_moderation)
            self.instance.set_dates(*initial_dates)
            #print self.instance.pk
            inst = self.instance
            file_ids = [x for x in self.cleaned_data.get('file_ids').split(',') if x]
            #print file_ids
            for file_id in file_ids:
                file_id1 = str('pictures/'+file_id)
                #print file_id1   
                f = Picture.objects.get(file=file_id1)
                a = Attachment(message=inst,attachment=f)
                a.save()
                #print a
                

        return is_successful
    # commit_on_success() is deprecated in Django 1.6 and will be removed in Django 1.8
    save = transaction.atomic(save) if hasattr(transaction, 'atomic') else transaction.commit_on_success(save)


class BaseReplyForm(BaseWriteForm):
    """The base class for a reply to a message."""
    def __init__(self, *args, **kwargs):
        recipient = kwargs.pop('recipient', None)
        super(BaseReplyForm, self).__init__(*args, **kwargs)
        self.recipient = recipient

    def clean(self):
        """Check that the recipient is correctly initialized."""
        if not self.recipient:
            raise forms.ValidationError(ugettext("Undefined recipient."))
        return super(BaseReplyForm, self).clean()

    def save(self, *args, **kwargs):
        return super(BaseReplyForm, self).save(self.recipient, *args, **kwargs)

allow_copies = not getattr(settings, 'POSTMAN_DISALLOW_COPIES_ON_REPLY', False)

class FullReplyImageForm(BaseReplyForm):

	if allow_copies:
		recipients = CommaSeparatedUserField(label=(_("Additional recipients"), _("Additional recipient")), required=False)
	file_ids = forms.CharField(required=False,widget=forms.HiddenInput())

	class Meta(BaseReplyForm.Meta):
		fields = (['recipients'] if allow_copies else []) + ['subject', 'body', 'file_ids']


class WriteFormImageForm(BaseWriteForm):
    recipients = CommaSeparatedUserField(label=(_("Recipients"), _("Recipient")), help_text='')
    file_ids = forms.CharField(required=False,widget=forms.HiddenInput())

    class Meta(BaseWriteForm.Meta):
        fields = ('recipients', 'subject', 'body', 'file_ids')


class QuickReplyFormImage(BaseReplyForm):
	file_ids = forms.CharField(required=False,widget=forms.HiddenInput())
	class Meta(BaseReplyForm.Meta):
		fields = ('subject', 'body', 'file_ids')
