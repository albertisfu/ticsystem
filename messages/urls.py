from django.conf.urls import patterns, include, url
from forms import *




urlpatterns = patterns('',

url(r'^reply/(?P<message_id>[\d]+)/$', 'postman.views.ReplyView', {'form_class': FullReplyImageForm}, name='postman_reply'),
#url(r'^view/(?P<message_id>[\d]+)/$', 'postman.views.MessageView', {'form_class': FullReplyImageForm}, name='postman_view'),
url(r'^write/(?:(?P<recipients>[^/#]+)/)?$', 'postman.views.WriteView', {'form_class': WriteFormImageForm}, name='postman_write'),
url(r'^view/t/(?P<thread_id>[\d]+)/$', 'postman.views.ConversationView', {'form_class': FullReplyImageForm}, name='postman_view_conversation'),
#url(r'^messages/reply/(?P<message_id>[\d]+)/$', 'postman.views.ReplyView',
        #{'form_class': FullReplyImageForm},
       # name='postman_reply'),
#url(r'^messages/view/t/(?P<thread_id>[\d]+)/$', 'postman.views.ConversationView',
        #{'form_class': FullReplyImageForm},
        #name='postman_view_conversation'),
url(r'^messages/', include('postman.urls')),
)