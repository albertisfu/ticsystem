# -*- encoding: utf-8 -*-
from django import forms
from models import *


class CyclehForm(forms.Form):
    cycle = forms.ChoiceField(widget=forms.Select(attrs={'class':'selector'}), choices=[(1, 'Trimestral'), (2, 'Semestral'), (3, 'Anual'), (4, 'Bianual')])

class CycledForm(forms.Form):
    cycle = forms.ChoiceField(widget=forms.Select(attrs={'class':'selector'}), choices=[(1, 'Anual'), (2, 'Bianual'), (3, '3 Años'), (4, '4 Años')])


class IfDomainForm(forms.Form):
    domain= forms.ChoiceField(widget=forms.Select(attrs={'class':'selector'}), choices=[(1, 'Si, ya cuento con dominio'), (2, 'No, deseo registrar un nuevo dominio')])
