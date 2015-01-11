from django.contrib import admin
from models import Featured

class FeaturedAdmin(admin.ModelAdmin):
    model = Featured

admin.site.register(Featured, FeaturedAdmin)
