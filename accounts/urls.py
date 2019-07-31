from django.conf.urls import url
from django.urls import include, path

from .views import *

app_name ='accounts'

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^settings/account/$',UserUpdateView.as_view(),name='my_account'),
    url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]
