from django.conf.urls import url
from django.urls import include, path

from .views import (
    OrderSummaryView,
    CheckOutView,
    PaymentView,
    AddCouponView,
    OrderView,
    OrdersView,
    SalesView,
    OrderDetailView
)

app_name ='orders'

urlpatterns = [
    path('cart/',OrderSummaryView.as_view(),name='cart'),
    path('checkout/',CheckOutView.as_view(),name='checkout'),
    path('add-coupon/',AddCouponView.as_view(),name='add-coupon'),
    # path('success/',order_success,name='success'),
    path('payment/<payment_option>/',PaymentView.as_view(),name='payment'),
        path('orders/',OrderView.as_view(),name='orders'),

    path('kgc/orders/<status>/', OrdersView.as_view(),name='orders-admin'),
    path('kgc/order/<int:pk>/', OrderDetailView.as_view(),name='orders-detail'),
    path('kgc/sales', SalesView.as_view(),name='sales'),
]
