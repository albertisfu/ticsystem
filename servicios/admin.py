from django.contrib import admin
from models import HostingPackage, Status, HostingService


class PackageHostingAdmin(admin.ModelAdmin):
    model = HostingPackage

class StatusHostingAdmin(admin.ModelAdmin):
    model = Status

class HostingServiceAdmin(admin.ModelAdmin):
	model = HostingService


admin.site.register(HostingService, HostingServiceAdmin)
admin.site.register(Status, StatusHostingAdmin)
admin.site.register(HostingPackage, PackageHostingAdmin)

# Register your models here.