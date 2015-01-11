from django.contrib import admin
from models import Customer
from proyects.models import Proyect


#class ProyectInline(admin.StackedInline):
    #model = Proyect 


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    #inlines = [ProyectInline]

admin.site.register(Customer, CustomerAdmin)
