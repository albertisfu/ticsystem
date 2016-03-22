
from django.contrib.auth.models import Permission, User
from customers.models import Customer
from django.contrib.auth.decorators import login_required

from django.conf import settings

def usuario(request):  #procesador de contexto, manda una variable a todos los templates
	if request.user.is_authenticated: #si la variable contiene datos de un usuario tenemos que verificar que este logueado para no causar errores en templates publicos
		try:
			current_user = request.user
			customer= Customer.objects.get(user = current_user)
			return {
            'usuario':customer.name,
        }
		except:
			return {
            'usuario':"", #forzozamente se tiene que retornar algo
        }


def idpayment(request):  #procesador de contexto, manda una variable a todos los templates

	return {
            'idpayment':settings.PAYMENTNUEVOID,
        }
