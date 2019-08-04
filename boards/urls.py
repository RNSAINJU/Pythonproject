from django.conf.urls import url
from django.urls import include, path
from .views import *
# from .views import (
#     OrderSummaryView
# )

app_name ='boards'

urlpatterns = [
    url(r'^fileupload/$',simple_upload, name='fileupload'),
    url(r'^discussion$', BoardListView.as_view(), name='discussion'),
    url(r'^boards/(?P<pk>\d+)/$', TopicListView.as_view(), name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', new_topic, name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', PostListView.as_view(), name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', reply_topic, name='reply_topic'),


    url(r'^new_post/$',NewPostView.as_view(), name='new_post'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        PostUpdateView.as_view(), name='edit_post'),
        
    path('kgc/boards', BoardView.as_view(),name='boards'),
]
