from django.conf.urls import url
from django.urls import include, path

from .views import (
    OrderSummaryView,
    CheckOutView
)

app_name ='orders'

urlpatterns = [
    path('cart/',OrderSummaryView.as_view(),name='cart'),
    path('checkout/',CheckOutView.as_view(),name='checkout'),
]
