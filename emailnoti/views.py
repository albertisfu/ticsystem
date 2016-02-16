from django import get_version
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from notifications.utils import slug2id
from notifications.models import Notification

from distutils.version import StrictVersion
if StrictVersion(get_version()) >= StrictVersion('1.7.0'):
    from django.http import JsonResponse
else:
    # Django 1.6 doesn't have a proper JsonResponse
    import json
    from django.http import HttpResponse

class NotificationViewList(ListView):
    template_name = 'list.html'
    context_object_name = 'notifications'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationViewList, self).dispatch(
            request, *args, **kwargs)


class AllNotificationsList(NotificationViewList):
    """
    Index page for authenticated user
    """

    def get_queryset(self):
        if getattr(settings, 'NOTIFICATIONS_SOFT_DELETE', False):
            qs = self.request.user.notifications.active()
        else:
            qs = self.request.user.notifications.all()
        return qs