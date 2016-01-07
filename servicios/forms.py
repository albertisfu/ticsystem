from django import forms
from models import *


class EmailForm(forms.Form):
    cycle = forms.ChoiceField(widget=forms.Select(attrs={'class':'selector'}), choices=[(1, 'Trimestral'), (2, 'Semestral'), (3, 'Anual'), (4, 'Bianual')])