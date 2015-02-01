from django.shortcuts import render_to_response,get_object_or_404, render
from django.contrib.auth.models import Permission, User
from django.template.context import RequestContext
from models import *
from customers.models import Customer
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from operator import attrgetter
from itertools import chain
from django.contrib.auth.decorators import user_passes_test
from forms import *
from django.core.context_processors import csrf
from proyects.models import Proyect
import conekta
import datetime

conekta.api_key = 'key_zkkg2WvCCoBdbiQq'


# Customer Views
@login_required
def customerPayment(request):
	current_user = request.user
	customer = get_object_or_404(Customer, user = current_user)
	payments = Payment.objects.filter(user=current_user)
	template = "payment.html"
	return render(request, template,locals())


@login_required
def customerPaymentDetail(request, payment):
	current_user = request.user
	payments = get_object_or_404(Payment, pk = payment, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	template = "payment-detail.html"
	return render(request, template,locals())


@login_required
def customerPaymentPay(request):
	if request.POST:
		form = PaymentForm(request.POST)
		if form.is_valid():
			form.save()
 
			return HttpResponseRedirect('/customer/payments')
	else:
		form = PaymentForm()
     
	args = {}
	args.update(csrf(request))
    
	args['form'] = form

	template = "payment-pay.html"
	return render(request, template,locals())	


@login_required
def customerPaymentPayProyect(request, proyect):
	current_user = request.user
	customer = get_object_or_404(Customer, user = current_user)
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user)
	#method = Method.objects.get(pk = 1)
	now = datetime.datetime.now()
	string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)
	payname=current_user.username + '_'  + string
	if request.POST:
		try:
			mount = int(proyects.remaingpayment)*100
			charge = conekta.Charge.create({
				"amount": mount,
				"currency": "MXN",
				"description": proyects.id,
				"reference_id": payname,
				"card": request.POST["conektaTokenId"] 
#request.form["conektaTokenId"], request.params["conektaTokenId"], "tok_a4Ff0dD2xYZZq82d9"
			})
			
			print charge.status
			print charge.fee
			print charge.paid_at
			if charge.status=='paid':
				newpay= Payment.objects.create(name=payname, description=proyects.id, proyect=proyects, user=customer, mount=proyects.remaingpayment, method=method)
				newpay.save()
		except conekta.ConektaError as e:
			print e.message
#el pago no pudo ser procesado

	template = "payment-proyect.html"
	return render(request, template,locals())

# Vistas Administrador-Pagos 

@login_required
@user_passes_test(lambda u: u.is_superuser) #acceso solo a superusuario
def paymentAdmin(request):
	paymentsall = Payment.objects.exclude(verifiedpayment__status__exact=1).exclude(verifiedpayment__status__exact=2).exclude(verifiedpayment__status__exact=3) #obtenemos todos los pagos
	paymentsrevision = Payment.objects.filter(verifiedpayment__status__exact=1) 
	paymentsverified = Payment.objects.filter(verifiedpayment__status__exact=2) 
	paymentsconflict = Payment.objects.filter(verifiedpayment__status__exact=3)
	template = "payments-admin.html"
	return render(request, template,locals())

@login_required
@user_passes_test(lambda u: u.is_superuser) #acceso solo a superusuario
def paymentAdminDetail(request): #recibimos el nombre de usuario a consultar
	if request.POST:
		form = VerifiedPaymentForm(request.POST)
		if form.is_valid():
			form.save()
 
			return HttpResponseRedirect('/administrator/payments/')
	else:
		form = VerifiedPaymentForm()
     
	args = {}
	args.update(csrf(request))
    
	args['form'] = form

	template = "payment-admin.html"
	return render(request, template,locals())








