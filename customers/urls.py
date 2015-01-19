from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	#URLS  para administrador
	url(r'^administrator/customers/$', 'customers.views.customerAdmin', name='customerAdmin'),#Vista de clientes
	url(r'^administrator/customers/(?P<username>\w+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'), #Detalle del cliente
	url(r'^administrator/proyect/(?P<proyect>\w+)/', 'customers.views.adminProyectDetail', name='adminProyectDetail'), #Detalle de proyecto
	#URLS de customer para cliente
    url(r'^customer/$', 'customers.views.customerCustomer', name='customerCustomer'), #Resumen de proyectos
    url(r'^customer/proyect/(?P<proyect>\w+)/', 'customers.views.customerProyectDetail', name='customerProyectDetail'), #Detalle de proyecto

    )