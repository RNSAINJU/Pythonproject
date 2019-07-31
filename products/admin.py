from django.contrib import admin
from .models import *


class Categories(admin.StackedInline):
    model=ChildProduct
    extra =1

class ProductAdmin(admin.ModelAdmin):
    inlines=[Categories]
    list_display=['id','title','short_description','description','category','status']
    list_display_links=('id','title')
    list_editable=('status',)
    list_filter=('category','status')
    # search_fields= ('user',)

class ChildProductAdmin(admin.ModelAdmin):
    list_display=['type','cost_price','price','discount_price','status','homefeatured','productsfeatured','enabledetail']
    list_editable=('cost_price','price','discount_price','status','homefeatured','productsfeatured','enabledetail')
    list_filter=('parent_product','status')

# admin.site.register(Main_Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(ChildProduct,ChildProductAdmin)
