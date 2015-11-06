from django import template
register = template.Library()

@register.simple_tag
def status_payment(status):
	if status == 1:
		status = "Pendiente"
	elif status== 2:
		status = "Verificado"
	elif status == 3:
		status = "Conflicto"
	elif status == 4:
		status = "Cancelado"
	elif status == 5:
		status = "Rembolsado"
		
	return status