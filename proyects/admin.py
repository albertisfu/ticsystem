from django.contrib import admin
from models import Type, Status, Proyect
from features.models import Featured
from contents.models import Content
from customers.models import Customer
from developers.models import Developer
from payments.models import Payment

class TypeAdmin(admin.ModelAdmin):
    model = Type


class StatusAdmin(admin.ModelAdmin):
    model = Status

class FeaturedInline(admin.StackedInline):
    model = Featured

class ContentInline(admin.StackedInline):
    model = Content

class DeveloperInline(admin.StackedInline):
    model = Developer      
  
class PaymentInline(admin.StackedInline):
    model = Payment  

class ProyectAdmin(admin.ModelAdmin):

	fieldsets = [
        (None,               {'fields': ['name','user', 'description',  'progress', 'mount', 'advancepayment', 'remaingpayment', 'pub_date', 'type1', 'status' ]}),

        ]
 	inlines = [FeaturedInline,PaymentInline,DeveloperInline,ContentInline]





admin.site.register(Proyect, ProyectAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)


# Register your models here.
