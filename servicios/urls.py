from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	#URLS  para administrador
    #url(r'^administrator/customers/(?P<username>[\w\-]+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'),
    #URLS de customer para cliente
    url(r'^customer/hosting/$', 'servicios.views.hostingCustomer', name='hostingCustomer'), #Resumen de proyectos
    url(r'^customer/domain/$', 'servicios.views.domainCustomer', name='domainCustomer'),
    url(r'^customer/hosting/(?P<hosting>\w+)/', 'servicios.views.customerHostingDetail', name='customerHostingDetail'),
    url(r'^customer/domain/(?P<domain>\w+)/', 'servicios.views.customerDomainDetail', name='customerDomainDetail'),
    url(r'^customer/hosting-active/(?P<hosting>\w+)/', 'servicios.views.customerHostingActiveS1', name='customerHostingActiveS1'),
    url(r'^customer/hosting-dns/(?P<hosting>\w+)/', 'servicios.views.customerHostingDns', name='customerHostingDns'),
    url(r'^customer/whois/(?P<hosting>\w+)/', 'servicios.views.customerHostingWhois', name='customerHostingWhois'),
    #url(r'^customer/proyect/(?P<proyect>\w+)/', 'proyects.views.customerProyectDetail', name='customerProyectDetail'), #Detalle de proyecto
    
    )