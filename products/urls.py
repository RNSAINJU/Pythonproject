from django.conf.urls import url
from django.urls import include, path

from .views import (
ProductView,
ProductDetailView,
add_to_cart,
remove_from_cart,
remove_single_item_from_cart
)

app_name ='products'

urlpatterns = [
    url(r'^products/$',ProductView.as_view(),name='products'),
    # url(r'^products/options/(?P<pk>\d+)/$',OptionView.as_view(),name='products'),
    path('product/<slug>/',ProductDetailView.as_view(),name='product'),
    path(r'^add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path(r'^remove-from-cart/<slug>/',remove_from_cart,name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),

]
