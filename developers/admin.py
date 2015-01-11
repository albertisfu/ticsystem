from django.contrib import admin
from models import Developer

class DeveloperAdmin(admin.ModelAdmin):
    model = Developer

admin.site.register(Developer, DeveloperAdmin)
