
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
        return HttpResponse(content=data, status=400, content_type='application/json')


#vistas administrador

#vistas  customer


	#En esta vista se obtiene el detalle del proyecto

@login_required
def customerProyectContent(request, proyect):
	current_user = request.user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user)
	try:
		content = Content.objects.get(proyect = proyect)
		if request.POST:
			form = ContentForm(request.POST, instance=content)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/customer/')
		else:
			form = ContentForm(instance=content)
	except Content.DoesNotExist:
		if request.POST:
			form = ContentForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.proyect = proyects
				post.save()
				return HttpResponseRedirect('/customer/')
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
	try:
		content = Content.objects.get(proyect = proyect)
		sections = Section.objects.filter(content = content)
		forms=[]
		for sec in sections:
			section = Section.objects.get(content = content, name=sec)
			form = SectionForm(instance=section)
			forms.append(form)
		if request.POST:
			objs = dict(request.POST.iterlists())
  			namefield = objs['name']
  			section = Section.objects.get(content = content, name=namefield)
  			#print section
  			form = SectionForm(request.POST, instance=section)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/customer/')
		else:
			form = forms
	except Section.DoesNotExist:
		if request.POST:
			objs = request.POST #diccionario unicode
			print objs
  			namefield = objs['name'] #obtenenos el elemento unicode
  			namefield=namefield.encode('utf8')
  			print namefield
  			section = Section.objects.get(content = content, name=namefield)
  			form = SectionForm(request.POST, instance=section)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/customer/')
		else:
			form = SectionForm()
		
	args = {}
	args.update(csrf(request))
	args['form'] = form
	template = "customerproyectsection.html"
	return render(request, template,locals())	




	