from django.conf.urls import url
from django.urls import include, path

from .views import (
    OrderSummaryView,
    CheckOutView,
    PaymentView,
    AddCouponView
)

app_name ='orders'

urlpatterns = [
    path('cart/',OrderSummaryView.as_view(),name='cart'),
    path('checkout/',CheckOutView.as_view(),name='checkout'),
    path('add-coupon/',AddCouponView.as_view(),name='add-coupon'),
    path('payment/<payment_option>/',PaymentView.as_view(),name='payment')
]
