from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'home.views.home', name='home'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="my_login"),
#URLS de customer para administrador
    url(r'^administrator/customers/$', 'customers.views.customerAdmin', name='customerAdmin'),
    url(r'^administrator/customers/(?P<username>\w+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'),
    url(r'^administrator/payments/$', 'payments.views.paymentAdmin', name='paymentAdmin'),
    url(r'^administrator/payments/verified/$', 'payments.views.paymentAdminDetail', name='paymentAdminDetail'),
    #url(r'^administrator/customers/(?P<username>[\w\-]+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'),

#URLS de customer para cliente
    url(r'^customer/$', 'customers.views.customerCustomer', name='customerCustomer'),
    url(r'^customer/proyect/(?P<proyect>\w+)/', 'customers.views.customerProyectDetail', name='customerProyectDetail'),
    url(r'^customer/payments/$', 'payments.views.customerPayment', name='customerPayment'),
    url(r'^customer/payment/(?P<payment>\w+)/', 'payments.views.customerPaymentDetail', name='customerPaymentDetail'),
    url(r'^customer/payments/pay/$', 'payments.views.customerPaymentPay', name='customerPaymentPay'),
    url(r'^customer/proyect-pay/(?P<proyect>\w+)/', 'payments.views.customerPaymentPayProyect', name='customerPaymentPayProyect'),
    
)
