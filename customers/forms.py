# -*- encoding: utf-8 -*-

from django import forms
from models import *
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _
#Acces
class RegistrationForm(UserCreationForm):
	email = forms.EmailField(label='', required=True,widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Email', 'required':""}))
	username = forms.RegexField(label='', max_length=10,
			regex=r'^[\w.@+-]+$',
			help_text=_("10 caracteres maximo, numeros o letras, sin espacios."),
			error_messages={
				'invalid': _("This value may contain only letters, numbers and "
						"@/./+/-/_ characters.")}, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Usuario', 'required':""}))
	password1 = forms.CharField(label='',
			widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder': 'Contraseña', 'required':""}))
	password2 = forms.CharField(label='',
		widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder': 'Repite Contraseña', 'required':""}))


	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')        

	"""def save(self,commit = True):   
					user = super(RegistrationForm, self).save(commit = False)
					user.email = self.cleaned_data['email']
					if commit:
						user.save()
						return user"""

##

class LoginForm(AuthenticationForm):
	username = forms.CharField(label='', max_length=254, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Usuario', 'required':""}))
	password = forms.CharField(label='',  widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder': 'Contraseña', 'required':""}))


class AccountForm(forms.ModelForm):
	class Meta:
		model = Customer
		exclude = ('user',) 

#Create Customer
class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		exclude = ('user',) 

class EmailForm(forms.Form):
    cycle = forms.ChoiceField(widget=forms.Select(attrs={'class':'selector'}), choices=[(1, 'Trimestral'), (2, 'Semestral'), (3, 'Anual'), (4, 'Bianual')])








