from django.conf.urls import url
from django.urls import include, path

from .views import (
    OrderSummaryView,
    CheckOutView,
    PaymentView
)

app_name ='orders'

urlpatterns = [
    path('cart/',OrderSummaryView.as_view(),name='cart'),
    path('checkout/',CheckOutView.as_view(),name='checkout'),
    path('payment/<payment_option>/',PaymentView.as_view(),name='payment')
]
