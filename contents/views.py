
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,get_object_or_404, render
from django.contrib.auth.models import Permission, User
from django.core.context_processors import csrf
from proyects.models import Proyect
from forms import *
from models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from operator import attrgetter
from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django_filters
from django.views.generic import CreateView
from fileupload.response import JSONResponse, response_mimetype
from fileupload.serialize import serialize
import json
from django.utils.encoding import *
# Create your views here.

from django.core.urlresolvers import reverse

class PictureCreateView(CreateView): #clase para recibir llamada post  de imagen subida
    model = Picture
    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        print data
        return HttpResponse(content=data, status=400, content_type='application/json')

from customers.models import Customer
from servicios.models import HostingService
from datetime import datetime, timedelta
@login_required
def customerProyectContent(request, proyect):
	current_user = request.user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user)
	try:
		content = Content.objects.get(proyect = proyect)
		if 'save' in request.POST:
			form = ContentForm(request.POST, instance=content)
			if form.is_valid():
				form.save()
		if 'deletefile' in request.POST:
			print request.POST['fileid']
			idfile = request.POST['fileid']
			objfile = objfile = Picture.objects.get(pk=idfile) #get section object
			objfile.delete()
			print 'delete'
			return HttpResponseRedirect(reverse('customerProyectContent', args=(proyects.id,)))

		if 'domain' in request.POST:
			print request.POST
			domain = request.POST['domain']
			proyects.domain = domain
			proyects.save()
			print proyects.domain
			if proyects.package.hosting: #if not hosting selected en package proyect
				billingcycle = 3 #anual
				package = proyects.package.hosting
				customer = Customer.objects.get(user = current_user)
				status = 1 #pending
				name = (proyects.name +'-'+'proyect').encode('utf8')
				print name
				#create hosting proyect
				p,created = HostingService.objects.get_or_create(name=name, user=customer, hostingpackage=package, billingcycle=billingcycle, status=status)
				if created:
					print 'creado'
					p.save()
					last_renewnow = p.last_renew #set one year of vigency
					next_renew = last_renewnow + timedelta(days = 365)
					HostingService.objects.filter(id=p.pk).update(next_renew=next_renew,status=2, domain=domain, activo=True)
					
			return HttpResponseRedirect(reverse('customerProyectDns', args=(proyects.id,)))
		if 'nodomain' in request.POST:
			print 'Nodomain------------------------'
			return HttpResponseRedirect(reverse('customerProyectWhois', args=(proyects.id,)))

		else:
			files = LogoUpload.objects.filter(content = content)
			form = ContentForm(instance=content)
	except Content.DoesNotExist:
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
			if proyects.package.hosting: #if not hosting selected en package proyect
				billingcycle = 3 #anual
				package = proyects.package.hosting
				customer = Customer.objects.get(user = current_user)
				status = 1 #pending
				name = (proyects.name +'-'+'proyect').encode('utf8')
				print name
				#create hosting proyect
				p,created = HostingService.objects.get_or_create(name=name, user=customer, hostingpackage=package, billingcycle=billingcycle, status=status)
				if created:
					print 'creado'
					p.save()
					last_renewnow = p.last_renew #set one year of vigency
					next_renew = last_renewnow + timedelta(days = 365)
					HostingService.objects.filter(id=p.pk).update(next_renew=next_renew,status=2, domain=domain, activo=True)
			return HttpResponseRedirect(reverse('customerProyectDns', args=(proyects.id,)))
		if 'nodomain' in request.POST:
			print 'Nodomain------------------------'
			return HttpResponseRedirect(reverse('customerProyectWhois', args=(proyects.id,)))

		else:
			form = ContentForm()
		
	args = {}
	args.update(csrf(request))
	args['form'] = form
	template = "customerproyectcontent.html"
	return render(request, template,locals())	

@login_required
def customerProyectSections(request, proyect):
	current_user = request.user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user)
	content = Content.objects.get(proyect = proyect)
	sections = Section.objects.filter(content = content)
	forms=[]
	filesa=[]
	for sec in sections:
		section = Section.objects.get(content = content, name=sec)
		files = FilesUpload.objects.filter(section = section)
		filesa.append(files) #add section files to array filesa
		idns = str(section.id) #get section id
		form = SectionForm(instance=section) #pass section instance to get  from database current data
		form.fields['text'].widget.attrs['id'] = 'cke'+idns #add custom id to text field to allow cke init
		form1 ={idns:form} #assign form to id section through a dict
		forms.append(form1) #add dict to forms

	if 'save' in request.POST:
		objs = dict(request.POST.iterlists()) #pass submit form fields in a dict
		namefield = objs['name'] #get name section from form
		namefield=namefield[0].encode('utf8') #encode to utf8 to avoid errors in latin characters
		section = Section.objects.get(content=content, name=namefield) #get section object
		#print section
		form = SectionForm(request.POST, instance=section) #pass section instance to form to avoid duplicate

		if form.is_valid(): #if form is valid save
			form.save()
			return HttpResponseRedirect(reverse('customerProyectSections', args=(proyects.id,)))
		else: #if form is no valid 
			print 'errores en form'
			sec = str(section)
			count = 0
			for formi in forms: #get form submit to cach errors and pass to a forms array
				for key in formi.keys(): #get forms keys 'key'
					section = Section.objects.get(pk=key) #get section object from every key
					#print section
					if section == form.instance: # if section equal to form submit
						#print 'encontrada'
						#print 'instance'+str(form.instance)
						idns = str(section.id) #get id section
						form1 ={idns:form} #assign form with errors to id section through a dict
						forms[count]=form1 #replace form with errors
				count += 1
			form = forms
			files = filesa

	if 'deletefile' in request.POST:
			print request.POST['fileid']
			idfile = request.POST['fileid']
			objfile = objfile = Picture.objects.get(pk=idfile) #get section object
			objfile.delete()
			print 'delete'
			return HttpResponseRedirect(reverse('customerProyectSections', args=(proyects.id,)))

	if 'addsection' in request.POST:
		name = request.POST['section']
		print 'section add'
		f = Content.objects.get(proyect_id=proyects.id)
		p,created = Section.objects.get_or_create(name=name, content=f)
		if created:
			p.save()
		return HttpResponseRedirect(reverse('customerProyectSections', args=(proyects.id,)))

	else:
		files = filesa
		form = forms

	args = {}
	args.update(csrf(request))
	args['form'] = form
	template = "customerproyectsection.html"
	return render(request, template,locals())	




	