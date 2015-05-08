from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,get_object_or_404, render
from django.contrib.auth.models import Permission, User
from django.core.context_processors import csrf
from proyects.models import Proyect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from payments.models import Payment, VerifiedPayment
import django_filters

# Create your views here.

#vistas administrador
@login_required
@user_passes_test(lambda u: u.is_superuser)
def adminProyectDetail(request, proyect):
	proyects = get_object_or_404(Proyect, pk = proyect) #solamente mostramos el contenido si coincide con pk
	template = "customeradminproyectdetail.html"
	return render(request, template,locals())	


def is_empty(any_structure):
    if any_structure:
        #print('Structure is not empty.')
        return False
    else:
        #print('Structure is empty.')
        return True

#vistas  customer

	#En esta vista se obtiene el detalle del proyecto
@login_required
def customerProyectDetail(request, proyect):
	current_user = request.user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	payments = Payment.objects.filter(proyect = proyects)
	if payments:
		payment = Payment.objects.filter(proyect = proyects).order_by('id')[0]
		paymentsv=[]
		for pay in payments:
			verifiedpayment = VerifiedPayment.objects.filter(payment = pay, status=2) #Verificar si hay pagos verificados
			paymentsv.append(verifiedpayment)
		#print paymentsv #Se anade a la tupla 
		for paysv in paymentsv: #iteramos en la tupla para determinar si existe algun pago verificado mostrar boton de contenidos
			if is_empty(paysv)==False:
				verified = True
			else:
				verified = False
	else:
		verified = False
	template = "customerproyect.html"
	return render(request, template,locals())	
