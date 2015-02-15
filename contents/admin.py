from django.contrib import admin
from models import Section, Content, LogoUpload

class SectionAdmin(admin.ModelAdmin):
    model = Section

class SectionInline(admin.StackedInline):
    model = Section  

class LogoInline(admin.StackedInline):
    model = LogoUpload 

class ContentAdmin(admin.ModelAdmin):
    model = Content
    inlines = [SectionInline, LogoInline]


class LogoUploadAdmin(admin.ModelAdmin):
    model = LogoUpload


admin.site.register(Section, SectionAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(LogoUpload, LogoUploadAdmin)
