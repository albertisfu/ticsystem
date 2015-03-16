from django import template
from contents.models import *
from contents.models import *
register = template.Library()

@register.simple_tag
def show_id(form, sec, count):
	sec = str(sec)
	form = form[count][sec]
	return form


@register.simple_tag
def section(sec):
	sec = str(sec)
	return sec

@register.simple_tag
def section_name(sec):
	sec = sec.encode('utf8')
	return sec

@register.simple_tag
def section_active(count):
	if count == 0:
		return 'active'
	return ''