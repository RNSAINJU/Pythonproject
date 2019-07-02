from django.conf.urls import url
from django.urls import include, path

from .views import (
ProductView,
ProductDetailView
)

app_name ='products'

urlpatterns = [
    url(r'^products/$',ProductView.as_view(),name='products'),
    path('product/<slug>/',ProductDetailView.as_view(),name='product'),
    # url(r'^add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    # path('ajax/load_prices/', views.load_prices, name='ajax_load_prices'),  # <-- this one here
]
