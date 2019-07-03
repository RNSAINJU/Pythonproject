from django.contrib import admin
from .models import Product, ChildProduct

admin.site.register(Product)
admin.site.register(ChildProduct)

# admin.site.register(Partner)
# Register your models here.
