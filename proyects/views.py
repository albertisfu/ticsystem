from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,get_object_or_404, render
from django.contrib.auth.models import Permission, User
from django.core.context_processors import csrf
from proyects.models import Proyect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django_filters

# Create your views here.

#vistas administrador
@login_required
@user_passes_test(lambda u: u.is_superuser)
def adminProyectDetail(request, proyect):
	proyects = get_object_or_404(Proyect, pk = proyect) #solamente mostramos el contenido si coincide con pk
	template = "customeradminproyectdetail.html"
	return render(request, template,locals())	




#vistas  customer

	#En esta vista se obtiene el detalle del proyecto
@login_required
def customerProyectDetail(request, proyect):
	current_user = request.user
	proyects = get_object_or_404(Proyect, pk = proyect, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	template = "customerproyect.html"
	return render(request, template,locals())	
