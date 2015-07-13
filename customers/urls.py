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
    url(r'^customer/add_proyect/$', 'customers.views.addService', name='addService'),
    url(r'^customer/add_service/$', 'customers.views.addMail', name='addMail'),
    url(r'^customer/thank_you/$', 'customers.views.ThankYou', name='ThankYou'),
    url(r'^customer/thank_you_service/$', 'customers.views.ThankYouService', name='ThankYouService'),
    url(r'^customer/account/$', 'customers.views.customerAccount', name='customerAccount'),
    url(r'^customer/account/edit$', 'customers.views.customerAccountEdit', name='customerAccountEdit'),
    url(r'^customer/email_ajax$', 'customers.views.EmailAjax', name='EmailAjax'), 
    url(r'^customer/pending_payments$', 'customers.views.PendingPayments', name='PendingPayments'),

    #url(r'^customer/email_ajax/$', EmailAjax.as_view()), 
    )