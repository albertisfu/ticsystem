from django import template
from contents.models import *
from contents.models import *
register = template.Library()

@register.simple_tag
def show_id(form, sec, count):
	sec = str(sec)
	form1 = form[count][sec]
	return form1