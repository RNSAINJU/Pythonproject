from django.contrib import admin
from .models import OrderProduct, Order, Payment, Coupon,OrderDetail

# class OrderPayment(admin.StackedInline):
#     model=OrderDetail

class OrderAdmin(admin.ModelAdmin):
    # inlines=[OrderPayment]
    list_display=['id','user','ordered','ordered_date','payment','order_details','status']
    list_display_links=('id','user')
    # list_editable=('',)
    list_filter=('ordered','ordered_date','status')
    # search_fields= ('user',)


admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(OrderDetail)
