from django.conf.urls import patterns, include, url
from proyects import views
from servicios import views

urlpatterns = patterns('',
	#URLS  para administrador
    url(r'^administrator/payments/$', 'payments.views.paymentAdmin', name='paymentAdmin'), #Vista de pagos
    url(r'^administrator/payments/verified/$', 'payments.views.paymentAdminDetail', name='paymentAdminDetail'), #Verificar un pago
    #url(r'^administrator/customers/(?P<username>[\w\-]+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'),
    #URLS de customer para cliente
    url(r'^customer/payments/$', 'payments.views.customerPayment', name='customerPayment'), #Resumen de pagos
    url(r'^customer/payment/(?P<payment>\w+)/', 'payments.views.customerPaymentDetail', name='customerPaymentDetail'), #Detalle de pagos
    #url(r'^customer/payments/pay/$', 'payments.views.customerPaymentPay', name='customerPaymentPay'), #Realizar un pago general
    url(r'^customer/proyect-pay/(?P<proyect>\w+)/', 'payments.views.customerPaymentPayProyect', name='customerPaymentPayProyect'), #Realizar un pago especifico
     url(r'^customer/proyect/(?P<proyect>\w+)/', 'proyects.views.customerProyectDetail', name='customerProyectDetail'), #Detalle de proyecto
    url(r'^customer/hosting/(?P<hosting>\w+)/', 'servicios.views.customerHostingDetail', name='customerHostingDetail'),
    url(r'^customer/domain/(?P<domain>\w+)/', 'servicios.views.customerDomainDetail', name='customerDomainDetail'),
    url(r'^customer/payments/oxxo/$', 'payments.views.oxxo', name='oxxo'), #Resumen de pagos
    url(r'^customer/payments/oxxopdf/$', 'payments.views.oxxopdf', name='oxxopdf'),
    url(r'^customer/payments/paypal/', include('paypal.standard.ipn.urls')), #
    url(r'^customer/paypal-thankyou/$', 'payments.views.paypalthankyou', name='paypalthankyou'),
    url(r'^customer/paypal-cancel/$', 'payments.views.paypalcancel', name='paypalcancel'),
    url(r'^customer/oxxo-webhook/$', 'payments.views.oxxo_webhook', name='oxxo_webhook'),
    )