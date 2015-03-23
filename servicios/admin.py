from django.contrib import admin
from models import HostingPackage, Status, HostingService, DomainService, Domain


class PackageHostingAdmin(admin.ModelAdmin):
    model = HostingPackage

class StatusHostingAdmin(admin.ModelAdmin):
    model = Status

class HostingServiceAdmin(admin.ModelAdmin):
	model = HostingService


class DomainServiceAdmin(admin.ModelAdmin):
    model = DomainService

class DomainAdmin(admin.ModelAdmin):
    model = Domain

admin.site.register(HostingService, HostingServiceAdmin)
admin.site.register(Status, StatusHostingAdmin)
admin.site.register(HostingPackage, PackageHostingAdmin)
admin.site.register(DomainService, DomainServiceAdmin)
admin.site.register(Domain, DomainAdmin)

# Register your models here.