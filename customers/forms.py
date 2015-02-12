from django import forms
from models import *


class AccountForm(forms.ModelForm):
	class Meta:
		model = Customer
		exclude = ('user',) 