from django.contrib import admin
from models import Type, Status, Proyect, Featured, Package
from contents.models import Content
from customers.models import Customer
from developers.models import Developer
from payments.models import PaymentNuevo
from django.contrib.contenttypes.admin import GenericTabularInline



class FeaturedAdmin(admin.ModelAdmin):
    model = Featured

class TypeAdmin(admin.ModelAdmin):
    model = Type

class PackageAdmin(admin.ModelAdmin):
    model = Package

class StatusAdmin(admin.ModelAdmin):
    model = Status

class ContentInline(admin.StackedInline):
    model = Content

class DeveloperInline(admin.StackedInline):
    model = Developer      
  
class PaymentInline(GenericTabularInline):
    model = PaymentNuevo

class ProyectAdmin(admin.ModelAdmin):

	fieldsets = [
        (None,               {'fields': ['name','user', 'description',  'progress', 'independent', 'mount', 'advancepayment', 'remaingpayment', 'package', 'status' ]}),

        ]
 	inlines = [PaymentInline,DeveloperInline,ContentInline]





admin.site.register(Proyect, ProyectAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Featured, FeaturedAdmin)
admin.site.register(Package, PackageAdmin)

# Register your models here.
