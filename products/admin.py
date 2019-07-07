from django.contrib import admin
from .models import Product, ChildProduct,Main_Category

admin.site.register(Product)
admin.site.register(ChildProduct)
admin.site.register(Main_Category)
# admin.site.register(Partner)
# Register your models here.
