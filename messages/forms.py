from __future__ import unicode_literals
from models import *
from postman.models import Message
from postman.forms import *
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

allow_copies = not getattr(settings, 'POSTMAN_DISALLOW_COPIES_ON_REPLY', False)

class FullReplyImageForm(BaseReplyForm):

	if allow_copies:
		recipients = CommaSeparatedUserField(label=(_("Additional recipients"), _("Additional recipient")), required=False)
	file_ids = forms.CharField(required=False,widget=forms.HiddenInput())

	class Meta(BaseReplyForm.Meta):
		fields = (['recipients'] if allow_copies else []) + ['subject', 'body', 'file_ids']

	@transaction.commit_on_success
	def save(self, recipient=None, parent=None, auto_moderators=[]):
        ### Bunch of code from original save method in BaseWriteForm from django-postman
		file_ids = [x for x in self.cleaned_data.get('file_ids').split(',') if x]
        ### Bunch of code from original save method in BaseWriteForm from django-postman
		for file_id in file_ids:
			f = Picture.objects.get(id=file_id)
			a = Attachment(message=self.instance,attachment=f)
			a.save()


class WriteFormImageForm(BaseWriteForm):
    recipients = CommaSeparatedUserField(label=(_("Recipientes"), _("Recipiente")), help_text='')
    file_ids = forms.CharField(required=False,widget=forms.HiddenInput())
    class Meta(BaseWriteForm.Meta):
        fields = ('recipients', 'subject', 'body', 'file_ids')
	@transaction.commit_on_success
	def save(self, recipient=None, parent=None, auto_moderators=[]):
        ### Bunch of code from original save method in BaseWriteForm from django-postman
		file_ids = [x for x in self.cleaned_data.get('file_ids').split(',') if x]
        ### Bunch of code from original save method in BaseWriteForm from django-postman
		for file_id in file_ids:
			f = Picture.objects.get(id=file_id)
			a = Attachment(message=self.instance,attachment=f)
			a.save()


class QuickReplyFormImage(BaseReplyForm):
	file_ids = forms.CharField(required=False,widget=forms.HiddenInput())
	class Meta(BaseReplyForm.Meta):
		fields = ('subject', 'body', 'file_ids')
	pass
