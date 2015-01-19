from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^administrator/payments/$', 'payments.views.paymentAdmin', name='paymentAdmin'), #Vista de pagos
    url(r'^administrator/payments/verified/$', 'payments.views.paymentAdminDetail', name='paymentAdminDetail'), #Verificar un pago
    #url(r'^administrator/customers/(?P<username>[\w\-]+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'),
    url(r'^customer/payments/$', 'payments.views.customerPayment', name='customerPayment'), #Resumen de pagos
    url(r'^customer/payment/(?P<payment>\w+)/', 'payments.views.customerPaymentDetail', name='customerPaymentDetail'), #Detalle de pagos
    url(r'^customer/payments/pay/$', 'payments.views.customerPaymentPay', name='customerPaymentPay'), #Realizar un pago general
    url(r'^customer/proyect-pay/(?P<proyect>\w+)/', 'payments.views.customerPaymentPayProyect', name='customerPaymentPayProyect'), #Realizar un pago especifico
    
    )