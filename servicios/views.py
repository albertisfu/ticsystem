from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,get_object_or_404, render
from django.contrib.auth.models import Permission, User
from django.core.context_processors import csrf
from models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django_filters
from itertools import chain
# Create your views here.
from datetime import datetime
from forms import *
#vistas administrador

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

#En esta vista obtenemos una lista de usuarios

"""@login_required
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


@login_required
@user_passes_test(lambda u: u.is_superuser)
def adminProyectDetail(request, proyect):
	proyects = get_object_or_404(Proyect, pk = proyect) #solamente mostramos el contenido si coincide con pk
	template = "customeradminproyectdetail.html"
	return render(request, template,locals())	"""

#Filtros y orden para customer
class ServicesFilterHosting(django_filters.FilterSet):
    class Meta:
		model = HostingService
		fields = { #creamos los filtros necesarios 
        		  'status':['exact'],
        		 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
				    ('-next_renew', 'Recientes'),
				    ('next_renew', 'Antiguos'),

				)

class ServicesFilterDomain(django_filters.FilterSet):
    class Meta:
		model = DomainService
		fields = { #creamos los filtros necesarios 
        		  'status':['exact'],
        		 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
				    ('-next_renew', 'Recientes'),
				    ('next_renew', 'Antiguos'),

				)


#vistas  customer

# Vistas Para Cliente
@login_required
def hostingCustomer(request):
	current_user = request.user
	filters = ServicesFilterHosting(request.GET, queryset=HostingService.objects.filter(user=current_user)) 
	paginator = Paginator(filters, 10)
	page = request.GET.get('page')
	try:
		hostings= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		hostings = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		hostings = paginator.page(paginator.num_pages)
	template = "hostingcustomer.html"
	return render(request, template,locals())



	#Vista Detalle hospedaje
@csrf_protect	
@login_required
def customerHostingDetail(request, hosting):
	current_user = request.user
	hostings = get_object_or_404(HostingService, pk = hosting, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	hosting = hostings.hostingpackage
	form = CyclehForm()
	content =  get_object_or_404(ContentType, pk = 21)
	if request.method == 'POST':
		customer = get_object_or_404(Customer, user = current_user)
		now = datetime.now()
		string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
		payname=current_user.username + '_'  + string
		billingcycle = request.POST['cycle']
		billingcycle1 = int(billingcycle)
		#hostingm = get_object_or_404(HostingService, pk = hostings.pk, user=current_user)
		#hostingm.billingcycle=billingcycle1
		#hostingm.save()
		hostingn = get_object_or_404(HostingService, pk = hostings.pk, user=current_user)

		if billingcycle1 == 1:
			cycleprice = hostingn.hostingpackage.trimestralprice
		elif billingcycle1 == 2:
			cycleprice = hostingn.hostingpackage.semestralprice
		elif billingcycle1 == 3:
			cycleprice = hostingn.hostingpackage.anualprice
		elif  billingcycle1 == 4:
			cycleprice = hostingn.hostingpackage.bianualprice
		description = 'renovar-'+str(billingcycle1)
		print cycleprice
		mount1= cycleprice
		newpay= PaymentNuevo.objects.create(name=payname, description=description, user=customer, mount=mount1, status=1, content_type=content, object_id=hostings.pk)
		return HttpResponseRedirect(reverse('customerPaymentDetail', args=(newpay.id,)))
	template = "customerhostingdetail.html"
	return render(request, template,locals())	





	# Vistas Para Cliente
@login_required
def domainCustomer(request):
	current_user = request.user
	filters = ServicesFilterDomain(request.GET, queryset=DomainService.objects.filter(user=current_user)) 
	paginator = Paginator(filters, 10)
	page = request.GET.get('page')
	try:
		domains= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		domains = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		domains = paginator.page(paginator.num_pages)
	template = "domaincustomer.html"
	return render(request, template,locals())


@login_required
def customerDomainDetail(request, domain):
	current_user = request.user
	domains = get_object_or_404(DomainService, pk = domain, user=current_user) #solamente mostramos el contenido si coincide con pk y es del usuario
	domain = domains.domain
	form = CycledForm()
	content =  get_object_or_404(ContentType, pk = 23)
	if request.method == 'POST':
		customer = get_object_or_404(Customer, user = current_user)
		now = datetime.now()
		string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
		payname=current_user.username + '_'  + string
		billingcycle = request.POST['cycle']
		billingcycle1 = int(billingcycle)
		#hostingm = get_object_or_404(HostingService, pk = hostings.pk, user=current_user)
		#hostingm.billingcycle=billingcycle1
		#hostingm.save()
		domainn = get_object_or_404(DomainService, pk = domains.pk, user=current_user)

		if billingcycle1 == 1:
			cycleprice = domainnn.domain.anualprice
		elif billingcycle1 == 2:
			cycleprice = domainn.domain.bianualprice
		elif billingcycle1 == 3:
			cycleprice = domainn.domain.trianualprice
		elif  billingcycle1 == 4:
			cycleprice = domainn.domain.quadanualprice
		description = 'renovar-'+str(billingcycle1)
		print cycleprice
		mount1= cycleprice
		newpay= PaymentNuevo.objects.create(name=payname, description=description, user=customer, mount=mount1, status=1, content_type=content, object_id=domains.pk)
		return HttpResponseRedirect(reverse('customerPaymentDetail', args=(newpay.id,)))
	template = "customerdomaindetail.html"
	return render(request, template,locals())	





