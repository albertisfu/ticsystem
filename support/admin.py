from django.contrib import admin
from models import Attachment

#class StatusAdmin(admin.ModelAdmin):
  #  model = Status

class AttachmentAdmin(admin.ModelAdmin):
    model = Attachment



admin.site.register(Attachment, AttachmentAdmin)
