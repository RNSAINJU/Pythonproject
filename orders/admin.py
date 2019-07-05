from django.contrib import admin
from .models import OrderProduct, Order, Payment, BillingAddress

admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(BillingAddress)
