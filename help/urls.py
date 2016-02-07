from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	#URLS  para administrador
    #url(r'^administrator/customers/(?P<username>[\w\-]+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'),
    #URLS de customer para cliente
    url(r'^$', 'help.views.homepage', name='help_home'), #Resumen de proyectos
    url(r'^view/$', 'help.views.view_ticket', name='help_public_view'),
    url(r'^view/(?P<ticket>\w+)/$', 'help.views.view_ticket_detail', name='help_public_detail'),
    url(r'^all/$', 'help.views.view_all_ticket', name='help_all_public_view'),
    
    )