from django.contrib import admin
from .models import OrderProduct, Order, Payment, Coupon,OrderDetail

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','ordered','ordered_date','status']

admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(OrderDetail)
