from django.conf.urls import patterns, include, url
from views import EmailAjax

urlpatterns = patterns('',
	#URLS  para administrador
	url(r'^administrator/customers/$', 'customers.views.customerAdmin', name='customerAdmin'),#Vista de clientes
	url(r'^administrator/customers/(?P<username>\w+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'), #Detalle del cliente
	#URLS de customer para cliente
    url(r'^customer/$', 'customers.views.customerHome', name='customerHome'), 
    url(r'^customer/proyects$', 'customers.views.customerCustomer', name='customerCustomer'),#Resumen de proyectos
    url(r'^customer/process/$', 'customers.views.customerProcess', name='customerProcess'),
    url(r'^customer/register/$', 'customers.views.createCustomer', name='createCustomer'),
    url(r'^customer/services/$', 'customers.views.Services', name='Services'),
    url(r'^customer/packages/$', 'customers.views.Packages', name='Packages'),
    url(r'^customer/email_packages/$', 'customers.views.Packages_Email', name='EmailPackages'),
    url(r'^customer/add_proyect/(?P<proyect>\w+)/', 'customers.views.addService', name='addService'), #Vista para contratar paquete desde pagina externa por medio de idmail pasado en url
    url(r'^customer/add_service/(?P<service>\w+)/', 'customers.views.addMail', name='addMail'),
    url(r'^customer/thank_you/(?P<proyect>\w+)/', 'customers.views.ThankYou', name='ThankYou'),
    url(r'^customer/thank_you_service/(?P<service>\w+)/', 'customers.views.ThankYouService', name='ThankYouService'),
    url(r'^customer/account/$', 'customers.views.customerAccount', name='customerAccount'),
    url(r'^customer/account/edit$', 'customers.views.customerAccountEdit', name='customerAccountEdit'),
    url(r'^customer/email_ajax$', 'customers.views.EmailAjax', name='EmailAjax'), 
    url(r'^customer/validuser$', 'customers.views.ValidUser', name='ValidUser'), 
    url(r'^customer/validemail$', 'customers.views.ValidEmail', name='ValidEmail'), 
    url(r'^customer/domain_ajax$', 'customers.views.DomainAjax', name='DomainAjax'), 
    url(r'^customer/pending_payments$', 'customers.views.PendingPayments', name='PendingPayments'),
    url(r'^customer/mark_as_read/$', 'customers.views.mark_as_read', name='mark_as_read'),
    #url(r'^customer/email_ajax/$', EmailAjax.as_view()), 
    )