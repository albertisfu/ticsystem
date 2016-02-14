from django.shortcuts import render_to_response,get_object_or_404, render
from django.shortcuts import redirect
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
import StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi
import os

#PayPalPaymentsForm
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.core.urlresolvers import reverse

from cgi import escape

from django.views.decorators.csrf import csrf_exempt

#from paypal.standard.models import ST_PP_COMPLETED
#from paypal.standard.ipn.signals import valid_ipn_received

from django.utils import timezone
from datetime import datetime, timedelta

"""def show_me_the_money(sender, **kwargs):
	ipn_obj = sender
	print "paypal hola"
	#print ipn_obj
	#print ipn_obj.payment_status
	if ipn_obj.payment_status == ST_PP_COMPLETED:
		print ipn_obj.payment_status
		payname = ipn_obj.item_name
		print payname
		customerid = ipn_obj.custom
		customer = get_object_or_404(Customer, id = customerid)
		print customer
		mount = int(ipn_obj.mc_gross)
		print mount
		paymentid = ipn_obj.item_number
		print paymentid
		payment = get_object_or_404(PaymentNuevo, pk = paymentid, user=customer)
		payment.method=5
		payment.status=2
		payment.date=timezone.now()
		payment.save()
		#newpay.save()
		# Undertake some action depending upon `ipn_obj`.
valid_ipn_received.connect(show_me_the_money)"""




@login_required
@csrf_exempt
def paypalthankyou(request):
	if request.POST:
		idproyect = request.POST['item_number']
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

def fetch_resources(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    return path

def dd_d(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), dest=result, link_callback=fetch_resources )
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
		return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))



def oxxopdf(request):
    oxxocode = request.session['oxxocode']
    oxxourl = request.session['oxxourl']
    mount = request.session['mount']
    return dd_d(
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



import json
from json import dumps
@csrf_exempt
def oxxo_webhook(request): #aqui se recibe la senal que verifica el pago paypal
	#data = '{"data":{"object":{"id":"56b79f9519ce882a92005e21","livemode":false,"created_at":1454874517,"status":"paid","currency":"MXN","description":"albertisfu_201627194741","reference_id":"53","failure_code":null,"failure_message":null,"monthly_installments":null,"object":"charge","amount":30000,"paid_at":1454874518,"fee":1218,"customer_id":"","refunds":[],"payment_method":{"expiry_date":"070316","barcode":"12345678901234567890123456789012","barcode_url":"http://s3.amazonaws.com/cash_payment_barcodes/12345678901234567890123456789012.png","object":"cash_payment","type":"oxxo","expires_at":1456531200},"details":{"name":null,"phone":null,"email":null,"line_items":[]}},"previous_attributes":{"status":"pending_payment"}},"livemode":false,"webhook_status":"pending","id":"56b79f962412297a2a003843","object":"event","type":"charge.paid","created_at":1454874518,"webhook_logs":[{"id":"webhl_9Kg9aCAzMwPbGs8","url":"https://aqhxcptulx.localtunnel.me/customer/oxxo-webhook/","failed_attempts":0,"last_http_response_status":-1,"object":"webhook_log","last_attempted_at":1454874518}]}'
	print request.body
	event_json = json.loads(request.body)
	#print event_json
	print 'hola post'  
	if event_json["type"] == 'charge.paid':
		print event_json["data"]["object"]["status"]
		if event_json["data"]["object"]["status"] =='paid':
				paymentid = int(event_json["data"]["object"]["reference_id"])
				print paymentid
				payment = get_object_or_404(PaymentNuevo, pk = paymentid)
				print 'pago oxxo'
				#payment = get_object_or_404(PaymentNuevo, pk = paymentid, user=customer)
				# payment = get_object_or_404(PaymentNuevo, pk = paymentid, user=customer)
				payment.method=4
				payment.status=2
				payment.date=timezone.now()
				payment.save() 
	return HttpResponse("OK")
	
	#if event_json.type == 'charge.paid':
	#	print 'pago oxxo'
		# payment = get_object_or_404(PaymentNuevo, pk = paymentid, user=customer)
		# payment.method=5
		# payment.status=2
		# payment.date=timezone.now()
		# payment.save()


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


#@login_required
#def customerPaymentDetail(request, payment):
#	current_user = request.user
#	payments = get_object_or_404(PaymentNuevo, pk = payment, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
#	template = "payment-detail.html"
#	return render(request, template,locals())



@login_required
def customerPaymentPayProyect(request, proyect):
	current_user = request.user
	customer = get_object_or_404(Customer, user = current_user)
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user)
	content =  get_object_or_404(ContentType, pk = 11)
	payments = PaymentNuevo.objects.filter(user=current_user, content_type_id=11, object_id=proyects.id)

	now = timezone.now()
	string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
	payname=current_user.username + '_'  + string
	#print payname
	invoice = str(proyects.id)+'-'+string
	filters = PaymentFilterCustomer(request.GET, queryset=PaymentNuevo.objects.filter(user=current_user,content_type_id=11, object_id=proyects.id)) #creamos el filtro en base al usuario actual
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

	if request.POST: #se tiene que validar formulario
		if 'custompay' in request.POST:
			mount1 = request.POST['mount']
			newpay= PaymentNuevo.objects.create(name=payname, description=payname, user=customer, mount=mount1, status=1, content_type=content, object_id=proyect)
			return HttpResponseRedirect(reverse('customerPaymentDetail', args=(newpay.id,))) #redireccionamos a pagar el nuevo pago pendiente creado
		else:
			mount1 =0 

	#method = Method.objects.get(pk = 1)
	template = "payment-proyect.html"
	return render(request, template,locals())




@login_required
def customerPaymentDetail(request, payment):
	current_user = request.user
	customer = get_object_or_404(Customer, user = current_user)
	payment = get_object_or_404(PaymentNuevo, pk = payment, user=current_user)
	#proyects = get_object_or_404(Proyect, pk = payment.object_id, user=current_user)
	#method = Method.objects.get(pk = 1)
	now = timezone.now()
	string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
	payname=current_user.username + '_'  + string
	print payname
	invoice = str(payment.id)+'-'+string
	#PayPalPaymentsForm
	paypal_dict = {
	"business": settings.PAYPAL_RECEIVER_EMAIL,
	"amount": payment.mount,
	"currency_code":"MXN",
	"item_name": payname,
	"invoice": invoice, #campo unico irrepetible usar para identificar pago
	"notify_url": "https://ocrnyrwlxd.localtunnel.me" + reverse('paypal-ipn'),
	"return_url": "https://ocrnyrwlxd.localtunnel.me/customer/paypal-thankyou/",
	"cancel_return": "https://ocrnyrwlxd.localtunnel.me/customer/paypal-cancel/",
	"custom": customer.id,  # Custom command to correlate to some function later (optional)
	"item_number": payment.id,
	}
	#print paypal_dict
	# Create the instance.
	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {"form": form}

	if request.POST:
		print request.POST
		if 'paymentcard' in request.POST:
			print "card"
			try:
				mount = int(payment.mount)*100
				charge = conekta.Charge.create({
					"amount": mount,
					"currency": "MXN",
					"description": payment.id,
					"reference_id": payname,
					"card": request.POST["conektaTokenId"] #Para cargo con tarjeta
					#request.form["conektaTokenId"], request.params["conektaTokenId"], "tok_a4Ff0dD2xYZZq82d9"
				})
				print charge.status
				print charge.fee
				print charge.paid_at
				if charge.status=='paid':
					paymentcard = get_object_or_404(PaymentNuevo, pk = payment.pk, user=current_user)
					paymentcard.method=3
					paymentcard.status=2
					paymentcard.date=timezone.now()
					paymentcard.save()
					#newpay.save() #cuando se usa objects.create se salva en automatico el modelo no es necesario salvarlo
					messages.add_message(request, messages.SUCCESS, 'Pago realizado con exito!', extra_tags='alert alert-success alert-dismissable')
					return HttpResponseRedirect(reverse('customerPaymentDetail', args=(payment.id,)))
					print "pago"
			except conekta.ConektaError as e:
				messages.add_message(request, messages.ERROR, 'El pago no puedo ser procesado, intente de nuevo por favor.', extra_tags='alert alert-danger alert-dismissable')
				print e.message
				#el pago no pudo ser procesado

		elif 'paymentcash' in request.POST:
			now = timezone.now()
			expire = now + timedelta(days = 10)
			month = '%02d' % expire.month
			day = '%02d' % expire.day
			date = str(expire.year)+'-'+str(month)+'-'+str(day)
			print "oxxo pago"
			try:
				mount = int(payment.mount)*100
				charge = conekta.Charge.create({
					"amount": mount,
					"currency": "MXN",
					"description": payname,
					"reference_id": payment.id,
					"cash": { #para cargo en oxxo
					    "type": "oxxo",
					    "expires_at": date
					  },
				})
				print charge.status
				print charge.fee
				print charge.paid_at
				print charge.payment_method["barcode_url"] #Para cargo en Oxxo
				request.session['oxxourl'] = charge.payment_method["barcode_url"]
				request.session['oxxocode'] = charge.payment_method["barcode"]
				request.session['mount'] = payment.mount
				return HttpResponseRedirect('/customer/payments/oxxo')
			except conekta.ConektaError as e:
				print e.message

	template = "payment-detail.html"
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








