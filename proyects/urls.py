from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	#URLS  para administrador
   url(r'^administrator/proyect/(?P<proyect>\w+)/', 'proyects.views.adminProyectDetail', name='adminProyectDetail'), #Detalle de proyecto
    #url(r'^administrator/customers/(?P<username>[\w\-]+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'),
    #URLS de customer para cliente
    url(r'^customer/proyect/(?P<proyect>\w+)/', 'proyects.views.customerProyectDetail', name='customerProyectDetail'), #Detalle de proyecto
    
    )