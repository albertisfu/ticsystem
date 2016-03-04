from django.contrib import admin
from models import Section, Content, LogoUpload, FilesUpload, Design, Examples



class SectionInline(admin.StackedInline):
    model = Section  

class LogoInline(admin.StackedInline):
    model = LogoUpload 

class FileInline(admin.StackedInline):
    model = FilesUpload 

class ExampleInline(admin.StackedInline):
    model = Examples  

class ContentAdmin(admin.ModelAdmin):
    model = Content
    inlines = [SectionInline, LogoInline]

class SectionAdmin(admin.ModelAdmin):
    model = Section
    inlines = [FileInline]


class LogoUploadAdmin(admin.ModelAdmin):
    model = LogoUpload

class FilesUploadAdmin(admin.ModelAdmin):
    model = FilesUpload

class DesignAdmin(admin.ModelAdmin):
    model = Design
    inlines = [ExampleInline]

admin.site.register(Section, SectionAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(LogoUpload, LogoUploadAdmin)
admin.site.register(FilesUpload, FilesUploadAdmin)
admin.site.register(Design, DesignAdmin)