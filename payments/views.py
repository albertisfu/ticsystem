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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django_filters

import reportlab

import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context

#PayPalPaymentsForm
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.core.urlresolvers import reverse

from cgi import escape

from django.views.decorators.csrf import csrf_exempt

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

def show_me_the_money(sender, **kwargs):
	ipn_obj = sender
	print ipn_obj
	print ipn_obj.payment_status
	if ipn_obj.payment_status == ST_PP_COMPLETED:
		print ipn_obj.payment_status
		payname = ipn_obj.item_name
		customerid = ipn_obj.custom
		customer = get_object_or_404(Customer, id = customerid)
		mount = int(ipn_obj.mc_gross)
		proyect = ipn_obj.invoice
		content =  get_object_or_404(ContentType, pk = 11)
		print payname
		print customer
		print mount
		print proyect
		newpay= PaymentNuevo.objects.create(name=payname, description=payname, user=customer, mount=mount, method=5, status=2, content_type=content, object_id=proyect)
		#newpay.save()
		# Undertake some action depending upon `ipn_obj`.
valid_ipn_received.connect(show_me_the_money)




@login_required
@csrf_exempt
def paypalthankyou(request):
	if request.POST:
		idproyect = request.POST['invoice']
		mount =request.POST['mc_gross']
	else:
		pass
	template = "paypalthank.html"
	return render(request, template,locals())

@login_required
@csrf_exempt
def paypalcancel(request):
	template = "paypalcancel.html"
	return render(request, template,locals())




def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def oxxopdf(request):
    oxxocode = request.session['oxxocode']
    oxxourl = request.session['oxxourl']
    mount = request.session['mount']
    return render_to_pdf(
            'oxxopdf.html',
            {
                'pagesize':'A4',
                'oxxocode': oxxocode,
                'oxxourl': oxxourl,
                'mount': mount,
            }
        )


def oxxo(request):
	oxxocode = request.session['oxxocode']
	oxxourl = request.session['oxxourl']
	mount = request.session['mount']
	template = "oxxo.html"
	return render(request, template,locals())

conekta.api_key = 'key_zkkg2WvCCoBdbiQq'


CUSTOM_CHOICES = (
    ('11','Proyecto'),
    ('29','Hospedaje'),
    ('31','Dominio'),
    ('','Todos'),
)

#Filtros y orden para customer
class PaymentFilterCustomer(django_filters.FilterSet):

	content_type =  django_filters.ChoiceFilter(choices=CUSTOM_CHOICES,label='Concepto')

	class Meta:
		model = PaymentNuevo
		fields = { 
        		  'content_type': ['exact'],
        		  'status':['exact'],
        		 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
				    ('-date', 'Recientes'),
				    ('date', 'Antiguos'),
				    ('mount', 'Monto Menor'),
				    ('-mount', 'Monto Mayor'),

				)



# Customer Views
@login_required
def customerPayment(request):
	current_user = request.user
	customer = get_object_or_404(Customer, user = current_user)
	payments = PaymentNuevo.objects.filter(user=current_user)

	filters = PaymentFilterCustomer(request.GET, queryset=PaymentNuevo.objects.filter(user=current_user)) #creamos el filtro en base al usuario actual
	paginator = Paginator(filters, 10)
	page = request.GET.get('page')
	try:
		payments = paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		payments = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		payments = paginator.page(paginator.num_pages)


	template = "payment.html"
	return render(request, template,locals())


@login_required
def customerPaymentDetail(request, payment):
	current_user = request.user
	payments = get_object_or_404(PaymentNuevo, pk = payment, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	template = "payment-detail.html"
	return render(request, template,locals())


# @login_required
# def customerPaymentPay(request):
# 	if request.POST:
# 		form = PaymentForm(request.POST)
# 		if form.is_valid():
# 			form.save()
 
# 			return HttpResponseRedirect('/customer/payments')
# 	else:
# 		form = PaymentForm()
     
# 	args = {}
# 	args.update(csrf(request))
    
# 	args['form'] = form

# 	template = "payment-pay.html"
# 	return render(request, template,locals())	



@login_required
def customerPaymentPayProyect(request, proyect):
	current_user = request.user
	customer = get_object_or_404(Customer, user = current_user)
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user)
	content =  get_object_or_404(ContentType, pk = 11)
	#method = Method.objects.get(pk = 1)
	now = datetime.datetime.now()
	string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)
	payname=current_user.username + '_'  + string

	#PayPalPaymentsForm
	paypal_dict = {
	"business": settings.PAYPAL_RECEIVER_EMAIL,
	"amount": proyects.remaingpayment,
	"currency_code":"MXN",
	"item_name": payname,
	"invoice": proyects.id,
	"notify_url": "https://oupddmivkr.localtunnel.me" + reverse('paypal-ipn'),
	"return_url": "https://oupddmivkr.localtunnel.me/customer/paypal-thankyou/",
	"cancel_return": "https://oupddmivkr.localtunnel.me/customer/paypal-cancel/",
	"custom": customer.id,  # Custom command to correlate to some function later (optional)
	}

	# Create the instance.
	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {"form": form}

	if request.POST:
		print request.POST
		if 'paymentcard' in request.POST:
			print "card"
			try:
				mount = int(proyects.remaingpayment)*100
				charge = conekta.Charge.create({
					"amount": mount,
					"currency": "MXN",
					"description": proyects.id,
					"reference_id": payname,
					"card": request.POST["conektaTokenId"] #Para cargo con tarjeta
					#request.form["conektaTokenId"], request.params["conektaTokenId"], "tok_a4Ff0dD2xYZZq82d9"
				})
				print charge.status
				print charge.fee
				print charge.paid_at
				if charge.status=='paid':
					newpay= PaymentNuevo.objects.create(name=payname, description=payname, user=customer, mount=proyects.remaingpayment, method=3, status=2, content_type=content, object_id=proyect)
					#newpay.save() #cuando se usa objects.create se salva en automatico el modelo no es necesario salvarlo
					print "pago"
			except conekta.ConektaError as e:
				print e.message
				#el pago no pudo ser procesado

		elif 'paymentcash' in request.POST:
			print "oxxo"
			try:
				mount = int(proyects.remaingpayment)*100
				charge = conekta.Charge.create({
					"amount": mount,
					"currency": "MXN",
					"description": proyects.id,
					"reference_id": payname,
					"cash": { #para cargo en oxxo
					    "type": "oxxo",
					    "expires_at": "2015-12-27"
					  },
				})
				
				print charge.status
				print charge.fee
				print charge.paid_at
				print charge.payment_method["barcode_url"] #Para cargo en Oxxo
				request.session['oxxourl'] = charge.payment_method["barcode_url"]
				request.session['oxxocode'] = charge.payment_method["barcode"]
				request.session['mount'] = proyects.remaingpayment
				return HttpResponseRedirect('/customer/payments/oxxo')
			except conekta.ConektaError as e:
				print e.message

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








