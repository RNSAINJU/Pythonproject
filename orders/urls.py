from django.conf.urls import url
from django.urls import include, path

from .views import (
    OrderSummaryView
)

app_name ='orders'

urlpatterns = [
    path('cart/',OrderSummaryView.as_view(),name='cart'),
]
