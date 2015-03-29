from django.contrib import admin
from models import Method, Payment, VerifiedPayment, PaymentHosting, VerifiedPaymentHosting, PaymentDomain, VerifiedPaymentDomain

#class StatusAdmin(admin.ModelAdmin):
  #  model = Status

##proyects
class MethodAdmin(admin.ModelAdmin):
    model = Method


class VerifiedPaymentAdmin(admin.ModelAdmin):
    fieldsets = [(None,{'fields': ['payment', 'status', 'date' ]}),]


class PaymentAdmin(admin.ModelAdmin):

	fieldsets = [(None,{'fields': ['name', 'description', 'user', 'proyect', 'mount', 'method', 'date' ]}),]


#Hosting

class VerifiedPaymentAdminHosting(admin.ModelAdmin):
    fieldsets = [(None,{'fields': ['payment', 'status', 'date' ]}),]


class PaymentAdminHosting(admin.ModelAdmin):

	fieldsets = [(None,{'fields': ['name', 'description', 'user', 'service', 'mount', 'method', 'date' ]}),]


#Domain

class VerifiedPaymentAdminDomain(admin.ModelAdmin):
    fieldsets = [(None,{'fields': ['payment', 'status', 'date' ]}),]


class PaymentAdminDomain(admin.ModelAdmin):

	fieldsets = [(None,{'fields': ['name', 'description', 'user', 'service', 'mount', 'method', 'date' ]}),]


#Proyects
admin.site.register(VerifiedPayment, VerifiedPaymentAdmin)
admin.site.register(Method, MethodAdmin)
admin.site.register(Payment, PaymentAdmin)

#Hosting
admin.site.register(VerifiedPaymentHosting, VerifiedPaymentAdminHosting)
admin.site.register(PaymentHosting, PaymentAdminHosting)

#Domain
admin.site.register(VerifiedPaymentDomain, VerifiedPaymentAdminDomain)
admin.site.register(PaymentDomain, PaymentAdminDomain)