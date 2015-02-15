
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,get_object_or_404, render
from django.contrib.auth.models import Permission, User
from django.core.context_processors import csrf
from proyects.models import Proyect
from forms import *
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
	print current_user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user)
	content = get_object_or_404(Content, proyect = proyect)
	print content
	if request.POST:
		form = ContentForm(request.POST, instance=content)
		if form.is_valid():
			print 'valido'
			form.save()
			return HttpResponseRedirect('/customer/')
	else:
		form = ContentForm(instance=content)
	args = {}
	args.update(csrf(request))
	args['form'] = form
	template = "customerproyectcontent.html"
	return render(request, template,locals())	


	