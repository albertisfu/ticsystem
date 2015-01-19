from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('customers.urls')),
    url(r'', include('payments.urls')),

    #url(r'^$', 'home.views.home', name='home'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="my_login"),

    url(r'^administrator/payments/$', 'payments.views.paymentAdmin', name='paymentAdmin'), #Vista de pagos
    url(r'^administrator/payments/verified/$', 'payments.views.paymentAdminDetail', name='paymentAdminDetail'), #Verificar un pago
    #url(r'^administrator/customers/(?P<username>[\w\-]+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'),
    url(r'^customer/payments/$', 'payments.views.customerPayment', name='customerPayment'), #Resumen de pagos
    url(r'^customer/payment/(?P<payment>\w+)/', 'payments.views.customerPaymentDetail', name='customerPaymentDetail'), #Detalle de pagos
    url(r'^customer/payments/pay/$', 'payments.views.customerPaymentPay', name='customerPaymentPay'), #Realizar un pago general
    url(r'^customer/proyect-pay/(?P<proyect>\w+)/', 'payments.views.customerPaymentPayProyect', name='customerPaymentPayProyect'), #Realizar un pago especifico
    
)
