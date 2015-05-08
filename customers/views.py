from django.shortcuts import render_to_response,get_object_or_404, render
from django.contrib.auth.models import Permission, User
#login
from django.contrib.auth import authenticate, login
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
    logout as auth_logout, get_user_model, update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import resolve_url
from django.conf import settings
#
#Registrer
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
#
from django.template.context import RequestContext
from models import *
from forms import *
from django.core.context_processors import csrf
from proyects.models import Proyect, Package, Status
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from operator import attrgetter
from itertools import chain
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django_filters

from datetime import datetime
#gateway after login, redirect to correct page
@login_required
def customerProcess(request):
	current_user = request.user
	print request.session['idpackage']
	try:
		customer = Customer.objects.get(user = current_user)
		proyects = Proyect.objects.filter(user = customer)
		if proyects:
			return HttpResponseRedirect('/customer/')
			#aqui se debe verificar si hay pagos
		else: #no hay proyectos
			if request.session['idpackage']==None:
				return HttpResponseRedirect('/customer/packages/')
			else:
				print request.session['idpackage']
			#if request.session['idpackage']:
				return HttpResponseRedirect('/customer/add_proyect/')
	except Customer.DoesNotExist:
				return HttpResponseRedirect('/customer/register/')
	template = "registration/process.html"
	return render(request, template,locals())

#gateway create customer if no exist
@login_required
@csrf_protect
def createCustomer(request):
	current_user = request.user
	email = current_user.email
	usuario = User.objects.get(username=current_user.username)
	if usuario.email:
		print 'con email'
		new_customer,created = Customer.objects.get_or_create(user=current_user, email=email)
	else:
		new_customer,created = Customer.objects.get_or_create(user=current_user)
		print 'sin email'
	#new_customer = Customer.objects.get(user=current_user, email=email)
	if created:
		new_customer.save()
	if request.POST:
		form = CustomerForm(request.POST, instance=new_customer) #usamos el form para editar una instancia customer
		if form.is_valid():
			form.save()
			usuario = User.objects.get(username=current_user.username)
			customer = Customer.objects.get(user=current_user)
			usuario.email = customer.email
			usuario.save()
			return HttpResponseRedirect('/customer/process/')
	else:
		form = CustomerForm(instance=new_customer)	

	template = "registration/createcustomer.html"
	return render(request, template,locals())

#Gateway Add Service
@login_required
def addService(request):
	idpackage = request.session['idpackage']
	package = Package.objects.get(id=idpackage)
	featureds = package.featureds.all()
	current_user = request.user
	if request.method == 'POST':
		customer = Customer.objects.get(user = current_user)
		#status = Status.objects.get(name='Pendiente')
		status = 1 #Pendiente
		proyect,created = Proyect.objects.get_or_create(name=package.name, description='Desarrollo Web Pyme', user=customer, progress=0, mount=0, advancepayment=0, remaingpayment=0, package=package, status=status)
		if created:
			proyect.save()
			request.session['idproyect'] = proyect.id
			idproyect = request.session['idproyect']
		return HttpResponseRedirect('/customer/thank_you')
	template = "registration/addservice.html"
	return render(request, template,locals())

@login_required
def Packages(request):
	#idpackage = request.session['idpackage']
	packages = Package.objects.filter()
	current_user = request.user
	date = "{:%d.%m.%Y %H:%M}".format(datetime.now())
	print date
	if request.method == 'POST':
		idpackage=request.POST['package']
		package = Package.objects.get(id=idpackage)
		customer = Customer.objects.get(user = current_user)
		#status = Status.objects.get(name='Pendiente')
		status = 1 #Pendiente
		description = (package.name +'-'+ customer.name+'-'+date).encode('utf8')
		name = (package.name +'-'+ current_user.username+'-'+date).encode('utf8')
		proyect,created = Proyect.objects.get_or_create(name=name, description=description, user=customer, progress=0, mount=0, advancepayment=0, remaingpayment=0, package=package, status=status)
		if created:
			proyect.save()
			request.session['idproyect'] = proyect.id
			idproyect = request.session['idproyect']
		return HttpResponseRedirect('/customer/thank_you')
	template = "packages.html"
	return render(request, template,locals())

@login_required
def ThankYou(request):
	idproyect = request.session['idproyect']
	proyect = Proyect.objects.get(id=idproyect)
	template = "thankyou.html"
	return render(request, template,locals())


def access(request): #vista acceso facebook, twitter o email
    package = request.GET.get('package')
    request.session['idpackage'] = package #save id package
    print request.session['idpackage']
    if request.method == 'POST':
        form = RegistrationForm(request.POST)     # create form object
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/login/')
    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()
    form = RegistrationForm()
    template = "registration/access.html"
    return render(request, template, args)

"""class Access(CreateView):
	form_class=UserCreationForm
	template_name = "registration/access.html"
	success_url ='/gracias'"""


##Login
@sensitive_post_parameters()
@csrf_protect
@never_cache
def custom_login(request, template_name='registration/loginew.html',
			redirect_field_name=REDIRECT_FIELD_NAME,
			authentication_form=LoginForm,
			current_app=None, extra_context=None):
	"""
	Displays the login form and handles the login action.
	"""
	#Si esta logueado el usuario redirigimos a customer, tendria que ser a process
	if request.user.is_authenticated():
		return HttpResponseRedirect('/customer/process')
	else:
		redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))
		if request.method == "POST":
			form = authentication_form(request, data=request.POST)
			if form.is_valid():

            # Ensure the user-originating redirection url is safe.
				if not is_safe_url(url=redirect_to, host=request.get_host()):
					redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
				auth_login(request, form.get_user())

				return HttpResponseRedirect(redirect_to)
		else:
			form = authentication_form(request)

		current_site = get_current_site(request)

		context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
		}
		if extra_context is not None:
			context.update(extra_context)
	return TemplateResponse(request, template_name, context, current_app=current_app)



#Filtros y orden para admin
class ProyectFilter(django_filters.FilterSet):
    class Meta:
		model = Proyect
		fields = { #creamos los filtros necesarios 
        		  'package': ['exact'],
        		  'status':['exact'],
        		 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
				    ('mount', 'Costo Menor'),
				    ('-mount', 'Costo Mayor'),
				    ('remaingpayment', 'Restante Menor'),
				    ('-remaingpayment', 'Restante Mayor'),
				    ('progress', 'Progreso Menor'),
				    ('-progress', 'Progreso Mayor'),
				    ('-pub_date', 'Recientes'),
				    ('pub_date', 'Antiguos'),

				)

#Filtros y orden para customer
class ProyectFilterCustomer(django_filters.FilterSet):
    class Meta:
		model = Proyect
		fields = { #creamos los filtros necesarios 
        		  'package': ['exact'],
        		  'status':['exact'],
        		 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
				    ('mount', 'Costo Menor'),
				    ('-mount', 'Costo Mayor'),
				    ('-pub_date', 'Recientes'),
				    ('pub_date', 'Antiguos'),

				)

#Vista Home Publica
def home(request):
    template = "index.html"
    return render(request, template)

# Vistas Para Administrador
#En esta vista obtenemos una lista de usuarios
@login_required
@user_passes_test(lambda u: u.is_superuser) #acceso solo a superusuario
def customerAdmin(request):
	current_user = request.user
	customer_list = Customer.objects.filter() #obtenemos todos los usuarios
	template = "customeradmin.html"
	paginator = Paginator(customer_list, 25) #definimos paginacion y numero de elementos maximos por pagina
	page = request.GET.get('page')
	try:
		customers = paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		customers = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		customers = paginator.page(paginator.num_pages)
	return render(request, template,locals())

#En esta vista obtenemos el detalle del usuario y sus proyectos
@login_required
@user_passes_test(lambda u: u.is_superuser) #acceso solo a superusuario
def customerAdminDetail(request, username): #recibimos el nombre de usuario a consultar
	filter_user = username  #definimos el usuario
	customer = get_object_or_404(Customer, user = username) #asignamos el modelo Customer para el usuario filtrando a customer
	#proyect_list = Proyect.objects.filter(user=filter_user) #obtenemos los proyectos del usuario filtrado
	filters = ProyectFilter(request.GET, queryset=Proyect.objects.filter(user=filter_user)) #creamos el filtro en base al usuario actual
	paginator = Paginator(filters, 5)
	page = request.GET.get('page')
	try:
		proyects = paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		proyects = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		proyects = paginator.page(paginator.num_pages)
	
	template = "customeradmindetail.html"
	return render(request, template,locals())	



# Vistas Para Cliente
#En esta vista obtenemos los proyectos del cliente
@login_required
def customerCustomer(request):
	current_user = request.user
	customer = get_object_or_404(Customer, user = current_user) #asignamos el modelo Customer para el usuario filtrando a customer
	#proyect_list = Proyect.objects.filter(user=filter_user) #obtenemos los proyectos del usuario filtrado
	filters = ProyectFilterCustomer(request.GET, queryset=Proyect.objects.filter(user=current_user)) #creamos el filtro en base al usuario actual
	paginator = Paginator(filters, 5)
	page = request.GET.get('page')
	try:
		proyects = paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		proyects = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		proyects = paginator.page(paginator.num_pages)
	template = "customer.html"
	return render(request, template,locals())
	

#En esta se muestran los detalles de la cuenta del usuario
@login_required
def customerAccount(request):
	current_user = request.user
	customer = get_object_or_404(Customer, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	template = "customerAccount.html"
	return render(request, template,locals())

@login_required
def customerAccountEdit(request): #recibimos el nombre de usuario a consultar
	current_user = request.user
	customer = get_object_or_404(Customer, user = current_user)
	print customer
	if request.POST:
		form = AccountForm(request.POST, instance=customer) #usamos el form para editar una instancia customer
		if form.is_valid():
			form.save()
 
			return HttpResponseRedirect('/customer/account/')
	else:
		form = AccountForm(instance=customer) #que se muestre llenado con los datos del usuario customer
     
	args = {}
	args.update(csrf(request))
    
	args['form'] = form

	template = "account-edit.html"
	return render(request, template,locals())


#@login_required
#def messages(request, id_messages):
	#current_user = request.user #obtenemos id de usuario http://stackoverflow.com/questions/12615154/how-to-getting-currently-logged-user-id-in-django
	#usuarios = Usernametw.objects.all()
	#user = get_object_or_404(Usernametw, pk = id_messages)
	#respuesta = Answer.objects.filter(users=current_user, usuario__usertw=user) #Filtramos por usuario logueado y usuario a quien envio
	#enviado = Direct.objects.filter(users=current_user, usuario__usertw=user)
	#result_list = sorted(chain(respuesta, enviado), key=attrgetter('pub_date')) #combine querys http://stackoverflow.com/questions/431628/how-to-combine-2-or-more-querysets-in-a-django-view
	#template = "mensajes_user.html"
	#return render(request, template,locals())
