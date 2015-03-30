from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	#URLS  para administrador
	url(r'^administrator/customers/$', 'customers.views.customerAdmin', name='customerAdmin'),#Vista de clientes
	url(r'^administrator/customers/(?P<username>\w+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'), #Detalle del cliente
	#URLS de customer para cliente
    url(r'^customer/$', 'customers.views.customerCustomer', name='customerCustomer'), #Resumen de proyectos
    url(r'^customer/process$', 'customers.views.customerProcess', name='customerProcess'),
    url(r'^customer/account/$', 'customers.views.customerAccount', name='customerAccount'),
    url(r'^customer/account/edit$', 'customers.views.customerAccountEdit', name='customerAccountEdit'), 
    )