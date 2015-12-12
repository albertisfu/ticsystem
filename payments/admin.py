from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from models import PaymentNuevo

#class StatusAdmin(admin.ModelAdmin):
  #  model = Status


class PaymentNuevoAdmin(admin.ModelAdmin):

	fieldsets = [(None,{'fields': ['name', 'description', 'user', 'status', 'mount', 'method', 'date' ]}),]


admin.site.register(PaymentNuevo, PaymentNuevoAdmin)
