from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',

url(r'^messages/reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(), name='postman_reply'),
url(r'^messages/write/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(), name='postman_write'),
url(r'^messages/view/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(), name='postman_view_conversation'),
url(r'^messages/view/(?P<message_id>[\d]+)/$', MessageView.as_view(), name='postman_view'),
url(r'^messages/upload/$', PictureCreateView.as_view(), name='PictureCreateView'), #esta vista solo recibie una llamada post no es publica
url(r'^messages/', include('postman.urls')),
	#Estas son las URL que tambien se incluyen
    #url(r'^sent/(?:(?P<option>'+OPTIONS+')/)?$', SentView.as_view(), name='postman_sent'),
    #url(r'^archives/(?:(?P<option>'+OPTIONS+')/)?$', ArchivesView.as_view(), name='postman_archives'),
    #url(r'^trash/(?:(?P<option>'+OPTIONS+')/)?$', TrashView.as_view(), name='postman_trash'),
    
)