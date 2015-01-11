from django.contrib import admin
from models import Section, Content

class SectionAdmin(admin.ModelAdmin):
    model = Section

class SectionInline(admin.StackedInline):
    model = Section  

class ContentAdmin(admin.ModelAdmin):
    model = Content
    inlines = [SectionInline]


admin.site.register(Section, SectionAdmin)
admin.site.register(Content, ContentAdmin)
