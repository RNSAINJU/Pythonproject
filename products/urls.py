from django.conf.urls import url
from django.urls import include, path

from .views import (
ProductView,
ProductDetailView,
add_to_cart,
remove_from_cart,
remove_single_item_from_cart,
product_type,
product_category,
admin_product_detail,
admin_product_detail_view
)

app_name ='products'

urlpatterns = [
    url(r'^products/$',ProductView.as_view(),name='products'),
    path('product/<int:pk>/',product_type,name='products_with_pk'),
    path('product/<int:pk>/',product_category,name='products_with_category'),
    # url(r'^products/options/(?P<pk>\d+)/$',OptionView.as_view(),name='products'),
    path('product/<slug>/',ProductDetailView.as_view(),name='product'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),

    path('kgc/products', admin_product_detail,name='kgcproducts'),
    path('kgc/products/<int:pk>/', admin_product_detail_view,name='kgcproductsdetails'),

]
