from django.conf.urls import url
from django.urls import include, path

from .views import (
    OrderSummaryView,
    CheckOutView,
    PaymentView,
    AddCouponView,
    OrderView,
    OrdersPendingView,
    SalesView
    # order_success
)

app_name ='orders'

urlpatterns = [
    path('cart/',OrderSummaryView.as_view(),name='cart'),
    path('checkout/',CheckOutView.as_view(),name='checkout'),
    path('add-coupon/',AddCouponView.as_view(),name='add-coupon'),
    # path('success/',order_success,name='success'),
    path('payment/<payment_option>/',PaymentView.as_view(),name='payment'),
        path('orders/',OrderView.as_view(),name='orders'),

    path('kgc/pending-orders', OrdersPendingView.as_view(),name='pending-orders'),
    path('kgc/sales', SalesView.as_view(),name='sales'),
]
