from django.shortcuts import render
from django.views.generic import ListView

from .models import Product

def featured_list_view(request):
    queryset=Product.objects.filter(featured=True)
    # queryset2=Partner.objects.all()
    context={
        'featured_list':queryset,
        # 'partners_list':queryset2
    }
    return render(request,"index.html",context)
    # def get_context_data(self, *args, **kwargs):
    #     context=super(ProductListView,self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

def product_list_view(request):
    queryset=Product.objects.filter(status='active')
    context={
        'object_list':queryset
    }
    return render(request,"products.html",context)

# def partner_list_view(request):
#     queryset=Partner.objects.all()
#     context={
#         'partners_list':queryset
#     }
#     return render(request,"partners.html",context)
# Create your views here.
