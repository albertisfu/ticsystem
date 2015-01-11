from django.contrib import admin
from models import Method, Payment, VerifiedPayment

#class StatusAdmin(admin.ModelAdmin):
  #  model = Status

class MethodAdmin(admin.ModelAdmin):
    model = Method



class VerifiedPaymentAdmin(admin.ModelAdmin):
    fieldsets = [(None,{'fields': ['payment', 'status', 'date' ]}),]


class PaymentAdmin(admin.ModelAdmin):

	fieldsets = [(None,{'fields': ['name', 'description', 'user', 'proyect', 'mount', 'method', 'date' ]}),]


admin.site.register(VerifiedPayment, VerifiedPaymentAdmin)
admin.site.register(Method, MethodAdmin)
admin.site.register(Payment, PaymentAdmin)


