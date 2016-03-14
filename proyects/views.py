# -*- encoding: utf-8 -*-
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,get_object_or_404, render
from django.contrib.auth.models import Permission, User
from django.core.context_processors import csrf
from proyects.models import Proyect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from payments.models import PaymentNuevo
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
	package = proyects.package
	activation = package.activation
	verifiedpayments = PaymentNuevo.objects.filter(user = current_user, status=2, content_type=11, object_id=proyect)
	print verifiedpayments
	if verifiedpayments: #verificar si por lo menos hay un pago del proyecto para darle acceso a agregar contenidos
		print "true"
		verified = True
	else:
		print "false"
		verified = False

	try:
		content = Content.objects.get(proyect = proyects)
		active = True
	except Content.DoesNotExist:	
		active = False


	""""if payments: //Metodo par verficar el estado de cada elemento en una relacion uno a uno 
		payment = Payment.objects.filter(proyect = proyects).order_by('id')[0]
		paymentsv=[]
		for pay in payments:
			verifiedpayment = VerifiedPayment.objects.filter(payment = pay, status=2) #Verificar si hay pagos verificados
			paymentsv.append(verifiedpayment)
		#print paymentsv #Se anade a la tupla 
		for paysv in paymentsv: #iteramos en la tupla para determinar si existe algun pago verificado mostrar boton de contenidos
			
			if is_empty(paysv)==False:
				print "true"
				verified = True
			else:
				print "false"
				verified = False
	else:
		verified = False
		print "false 2"""


	template = "customerproyect.html"
	return render(request, template,locals())	

from contents.models import *
from forms import ContentForm
from forms import *
from django.core.urlresolvers import reverse

from django.db.models.signals import post_save
from servicios.models import Domain, DomainService, HostingService, billingcycle_hosting, createHosting
from datetime import datetime, timedelta


@login_required
def customerProyectActive(request, proyect):
	current_user = request.user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user)
	try:
		content = Content.objects.get(proyect = proyect)
		if 'save' in request.POST:
			form = ContentForm(request.POST, instance=content)
			if form.is_valid():
				form.save()
			#avoid whois or dns redirection if domain field exist in proyect, redirect to CustomerProyectDesign
			if proyects.domain:
				package = proyects.package
				activation = package.activation
				if activation==True:
					return HttpResponseRedirect(reverse('customerProyectDesign', args=(proyects.id,)))
				elif activation==False:
					Proyect.objects.filter(id=proyect).update(active=True) #set Active Proyect True
					return HttpResponseRedirect(reverse('customerProyectDetail', args=(proyects.id,)))

		if 'deletefile' in request.POST: #eliminar archivo on post
			print request.POST['fileid']
			idfile = request.POST['fileid']
			objfile = objfile = Picture.objects.get(pk=idfile) #get section object
			objfile.delete()
			print 'delete'
			return HttpResponseRedirect(reverse('customerProyectActive', args=(proyects.id,)))

		if 'domain' in request.POST: #the user has domain, only show DNS
			domain = request.POST['domain']
			proyects.domain = domain
			proyects.save()
			print proyects.domain
			#create hosting proyect
			#function in Services.modes createHosting 
			createHosting(request=request, proyect=proyect, domain=domain)
					
			return HttpResponseRedirect(reverse('customerProyectDns', args=(proyects.id,)))
		if 'nodomain' in request.POST: #the user hasn't  domain, redirect to whois
			print 'Nodomain------------------------'
			return HttpResponseRedirect(reverse('customerProyectWhois', args=(proyects.id,)))

		else: #if no post
			files = LogoUpload.objects.filter(content = content)
			form = ContentForm(instance=content)
			#hide domain field on proyect domain exist
			if proyects.domain:
				form.fields['dominio'].widget = forms.HiddenInput()
	except Content.DoesNotExist: #the same previous but when Content object hasn't been created
		if 'save' in request.POST:
			form = ContentForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.proyect = proyects
				post.save()
				post = form.save()
			
		if 'domain' in request.POST:
			domain = request.POST['domain']
			proyects.domain = domain
			proyects.save()
			print proyects.domain
			#create hosting proyect
			#function in Services.modes createHosting 
			createHosting(request=request, proyect=proyect, domain=domain)
			return HttpResponseRedirect(reverse('customerProyectDns', args=(proyects.id,)))
		if 'nodomain' in request.POST:
			print 'Nodomain------------------------'
			return HttpResponseRedirect(reverse('customerProyectWhois', args=(proyects.id,)))
		else:
			form = ContentForm()
		
	args = {}
	args.update(csrf(request))
	args['form'] = form
	template = "proyectactive.html"
	return render(request, template,locals())	


from customers.models import Customer
from proyects.models import ActivationMailAdmin
@login_required
def customerProyectDns(request, proyect):
	current_user = request.user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	if 'next' in request.POST:
		package = proyects.package
		activation = package.activation
		if activation==True:
			return HttpResponseRedirect(reverse('customerProyectDesign', args=(proyects.id,)))
		elif activation==False:
			Proyect.objects.filter(id=proyect).update(active=True) #set Active Proyect True
			#email admin activation notification
			ActivationMailAdmin(request=request, proyect=proyect)

			return HttpResponseRedirect(reverse('customerProyectDetail', args=(proyects.id,)))
	template = "proyectdns.html"
	return render(request, template,locals())	

from servicios.models import Domain, DomainService
import urllib, json

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


@login_required
def customerProyectWhois(request, proyect):
	current_user = request.user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	customer = get_object_or_404(Customer, user = current_user)
	#d = {'one':'itemone', 'two':'itemtwo', 'three':'itemthree'}
	d=dict()
	if 'domain' in request.POST:
		#print request.POST.getlist('domains')
		domains = request.POST.getlist('domains')
		print domains
		for domain in domains:
			print domain
			url =u''.join(("https://www.whoisxmlapi.com/whoisserver/WhoisService?cmd=GET_DN_AVAILABILITY&domainName=",domain,"&getMode=DNS_AND_WHOIS&username=albertisfu&password=6k7SaP9XsjDyEr2Z4b&outputFormat=JSON")).encode('utf-8')
			response = urllib.urlopen(url);
			data = json.loads(response.read())
			print data
			avalaible = data['DomainInfo']['domainAvailability']
			domainName = data['DomainInfo']['domainName']
			print avalaible
			print domainName
			if avalaible == 'AVAILABLE':
				avalaible = 'Disponible'
			elif avalaible == 'UNAVAILABLE':
				avalaible ='No Disponible'

			d.update({domainName:avalaible})
			print d
	if 'registro' in request.POST:
		domain = request.POST['registro']
		proyects.domain = domain
		proyects.save()
		dom = domain.split(".")  
		print len(dom)
		if len(dom) == 2: #crear Domain TLD en DB com, commx, biz, edumx, org
			dtld = dom[1]
			print dtld
		if len(dom) == 3:
			dtld = dom[1] + dom[2]
			print dtld
		tld = get_object_or_404(Domain, tdl = dtld)
		customer = get_object_or_404(Customer, user = current_user)
		DomainService.objects.create(name=domain, user=customer, domain=tld)

		#create hosting proyect
		#function in Services.modes createHosting 
		createHosting(request=request, proyect=proyect, domain=domain)

		package = proyects.package
		activation = package.activation
		if activation==True:
			return HttpResponseRedirect(reverse('customerProyectDesign', args=(proyects.id,)))
		elif activation==False:
			Proyect.objects.filter(id=proyect).update(active=True) #set Active Proyect True
			#email admin activation notification
			ActivationMailAdmin(request=request, proyect=proyect)

			return HttpResponseRedirect(reverse('customerProyectDetail', args=(proyects.id,)))
			


	template = "customerhostingwhois.html"
	return render(request, template,locals())	

@login_required
def customerProyectDesign(request, proyect):
	current_user = request.user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	package = proyects.package
	content = get_object_or_404(Content, proyect = proyects)
	designs = Design.objects.filter(package=package)

	if 'design' in request.POST:
		selected = request.POST['design']
		print selected
		design = get_object_or_404(Design, pk = selected)
		print design
		content.design = design
		content.save()
		return HttpResponseRedirect(reverse('customerProyectExamples', args=(proyects.id,)))

	template = "customerproyectdesign.html"
	return render(request, template,locals())	

from django.contrib import messages
@login_required
def customerProyectExamples(request, proyect):
	current_user = request.user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	content = get_object_or_404(Content, proyect = proyects)
	design =  content.design
	examples = Examples.objects.filter(design=design)

	if 'design' in request.POST:
		selected = request.POST['design']
		print selected
		example = get_object_or_404(Examples, pk = selected)
		print example
		content.example = example
		content.save()
		Proyect.objects.filter(id=proyect).update(active=True) #set Active Proyect True
		#email admin activation notification
		ActivationMailAdmin(request=request, proyect=proyect)

		messages.add_message(request, messages.SUCCESS, 'Gracias, hemos recibido su información correctamente!', extra_tags='alert alert-success alert-dismissable')
		return HttpResponseRedirect(reverse('customerProyectDetail', args=(proyects.id,)))



	template = "customerproyectexample.html"
	return render(request, template,locals())	



