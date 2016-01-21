from django.contrib import admin
from models import EmailTemplate



class EmailTemplateAdmin(admin.ModelAdmin):
    model = EmailTemplate

admin.site.register(EmailTemplate, EmailTemplateAdmin)
