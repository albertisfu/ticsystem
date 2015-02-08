from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',

url(r'^messages/reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(), name='postman_reply'),
#url(r'^view/(?P<message_id>[\d]+)/$', 'postman.views.MessageView', {'form_class': FullReplyImageForm}, name='postman_view'),
url(r'^messages/write/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(), name='postman_write'),
url(r'^messages/view/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(), name='postman_view_conversation'),
url(r'^messages/view/(?P<message_id>[\d]+)/$', MessageView.as_view(), name='postman_view'),
url(r'^messages/upload/$', PictureCreateView.as_view(), name='PictureCreateView'),
#url(r'^messages/reply/(?P<message_id>[\d]+)/$', 'postman.views.ReplyView',
        #{'form_class': FullReplyImageForm},
       # name='postman_reply'),
#url(r'^messages/view/t/(?P<thread_id>[\d]+)/$', 'postman.views.ConversationView',
        #{'form_class': FullReplyImageForm},
        #name='postman_view_conversation'),
url(r'^messages/', include('postman.urls')),
)