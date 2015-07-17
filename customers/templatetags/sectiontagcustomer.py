from django import template
from contents.models import *
from contents.models import *
register = template.Library()


@register.simple_tag
def status_current(status):
	if status == 1:
		status = "Pendiente"
	elif status== 2:
		status = "Proceso"
	elif status == 3:
		status = "Terminado"
	elif  status== 4:
		status = "Cancelado"
		
	return status


@register.simple_tag
def status_current_hosting(status):
	if status == 1:
		status = "Pendiente"
	elif status== 2:
		status = "Activo"
	elif status == 3:
		status = "Terminado"
		
	return status



@register.simple_tag
def seemore(count):
	if count == 4:
		val = True
	else:
		val = False
	return val

