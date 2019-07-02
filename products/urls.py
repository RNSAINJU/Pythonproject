from django.conf.urls import url
from django.urls import include, path

from .views import (
ProductView,
ProductDetailView,
add_to_cart,
remove_from_cart
)

app_name ='products'

urlpatterns = [
    url(r'^products/$',ProductView.as_view(),name='products'),
    path('product/<slug>/',ProductDetailView.as_view(),name='product'),
    path(r'^add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path(r'^remove-from-cart/<slug>/',remove_from_cart,name='remove-from-cart'),
    # path('ajax/load_prices/', views.load_prices, name='ajax_load_prices'),  # <-- this one here
]
