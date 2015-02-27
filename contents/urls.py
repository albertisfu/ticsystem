from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
	#URLS  para administrador
  
    #url(r'^administrator/customers/(?P<username>[\w\-]+)/', 'customers.views.customerAdminDetail', name='customerAdminDetail'),
    #URLS de customer para cliente
    url(r'^customer/content-proyect/(?P<proyect>\w+)/', 'contents.views.customerProyectContent', name='customerProyectContent'), #Agregar informacion basica
    url(r'^customer/sections-proyect/(?P<proyect>\w+)/', 'contents.views.customerProyectSections', name='customerProyectSections'), #Agregar contenidos
    url(r'^customer/content/upload/$', PictureCreateView.as_view(), name='PictureCreateView'), #esta vista solo recibie una llamada post no es publica
    )