from django.conf.urls import patterns, include, url
from django.contrib import admin
import notifications
#from customers.views import Access
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
    url(r'', include('servicios.urls')),
    #url(r'', include('postman.urls')),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="my_login"),
    #url(r'^access/$', Access.as_view()),
    url(r'^access/$', 'customers.views.access', name='access'),
    url(r'^accounts/login/$', 'customers.views.custom_login', name='custom_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^upload/', include('fileupload.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^inbox/notifications/', include('notifications.urls', namespace='notifications')),
    url(r'helpdesk/', include('helpdesk.urls')),
    url(r'customer/help/', include('help.urls')),
    url(r'^customer/help/view/$', 'help.views.view_ticket', name='helpdesk_public_view'),

    #url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
)

from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
