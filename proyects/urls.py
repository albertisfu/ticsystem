from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	#URLS  para administrador
   url(r'^administrator/proyect/(?P<proyect>\w+)/', 'proyects.views.adminProyectDetail', name='adminProyectDetail'), #Detalle de proyecto
    #url(r'^administrator/customers/(?P<username>[\w\-]+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'),
    #URLS de customer para cliente
    url(r'^customer/proyect/(?P<proyect>\w+)/', 'proyects.views.customerProyectDetail', name='customerProyectDetail'), #Detalle de proyecto
    url(r'^customer/proyect-active/(?P<proyect>\w+)/', 'proyects.views.customerProyectActive', name='customerProyectActive'), #First View Active
    #url(r'^customer/proyect-domain/(?P<proyect>\w+)/', 'proyects.views.customerProyectAddDomain', name='ProyectAddDomain'), #Add Domain Individual
    url(r'^customer/proyect-dns/(?P<proyect>\w+)/', 'proyects.views.customerProyectDns', name='customerProyectDns'), #Second View Active If they have domain
    url(r'^customer/proyect-whois/(?P<proyect>\w+)/', 'proyects.views.customerProyectWhois', name='customerProyectWhois'), #Second View Active If they doesn't have domain
    url(r'^customer/proyect-design/(?P<proyect>\w+)/', 'proyects.views.customerProyectDesign', name='customerProyectDesign'), #Third  View Active, Select kind of design
    url(r'^customer/proyect-examples/(?P<proyect>\w+)/', 'proyects.views.customerProyectExamples', name='customerProyectExamples'), #Four View Active, Select Example 
    #send Sections URL is in Contents/URLS customerProyectSections
    )