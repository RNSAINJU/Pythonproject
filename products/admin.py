from django.contrib import admin
from .models import Product, ChildProduct, OrderProduct, Order

admin.site.register(Product)
admin.site.register(ChildProduct)
admin.site.register(OrderProduct)
admin.site.register(Order)
# admin.site.register(Partner)
# Register your models here.
