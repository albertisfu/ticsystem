from django.contrib import admin
from models import HostingPackage, HostingService, DomainService, Domain
from payments.models import PaymentNuevo
from django.contrib.contenttypes.admin import GenericTabularInline


class PaymentInline(GenericTabularInline):
    model = PaymentNuevo

class PackageHostingAdmin(admin.ModelAdmin):
    model = HostingPackage

class HostingServiceAdmin(admin.ModelAdmin):
	model = HostingService
	inlines = [PaymentInline]


class DomainServiceAdmin(admin.ModelAdmin):
    model = DomainService
    inlines = [PaymentInline]

class DomainAdmin(admin.ModelAdmin):
    model = Domain

admin.site.register(HostingService, HostingServiceAdmin)
admin.site.register(HostingPackage, PackageHostingAdmin)
admin.site.register(DomainService, DomainServiceAdmin)
admin.site.register(Domain, DomainAdmin)

# Register your models here.