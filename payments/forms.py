from django import forms
from models import *


class PaymentForm(forms.ModelForm):
	class Meta:
		model = Payment

class VerifiedPaymentForm(forms.ModelForm):
	class Meta:
		model = VerifiedPayment



