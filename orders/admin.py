from django.contrib import admin
from .models import OrderProduct, Order, Payment, Coupon

class OrderAdmin(admin.ModelAdmin):
    list_display=['user','ordered']

admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
# admin.site.register(BillingAddress)
