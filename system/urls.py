from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('customers.urls')),
    url(r'', include('payments.urls')),
    url(r'', include('proyects.urls')),
    url(r'', include('contents.urls')),
    #url(r'', include('postman.urls')),
    url(r'', include('support.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="my_login"),
    url(r'^upload/', include('fileupload.urls')),
)
