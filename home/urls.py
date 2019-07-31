from django.conf.urls import url
from django.urls import include, path

from .views import *

app_name ='home'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^partners/$', PartnerView.as_view(), name='partners'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    # url(r'^about/(?P<pk>\d+)/new/$', home_views.new_enquiry, name='new_enquiry'),

    url(r'^news/$', news_list_view, name='news'),
]
