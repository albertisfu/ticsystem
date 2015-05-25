from django import forms
from models import *


class EmailForm(forms.Form):
    cycle = forms.ChoiceField(widget=Select(attrs={'class':'selector'}), choices=[(1, 'Mac'), (2, 'PC')])