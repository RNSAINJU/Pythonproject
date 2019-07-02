from django.shortcuts import get_object_or_404,render
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Product,ChildProduct, OrderProduct,Order
from django.shortcuts import reverse, redirect


class ProductView(ListView):
    model=Product
    context_object_name = 'products'
    template_name="products.html"
    # paginate_by = 10

    def get_queryset(self):
        queryset1=Product.objects.all()
        queryset2=ChildProduct.objects.all()
        queryset={'parent':queryset1,'child':queryset2}
        return queryset

def load_prices(request):
    childproduct_id=request.GET.get('childproduct')
    price=ChildProduct.objects.filter(childproduct_id=childproduct_id).order_by('type')
    return render(request,'hr/prices_list.html',{'price':price})

class ProductDetailView(DetailView):
    model= ChildProduct
    template_name= "product.html"

# def add_to_cart(request,slug):
#     product=get_object_or_404(Product,slug=slug)
#     order_product=OrderProduct.objects.create(product=product)
#     order=Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order= order_qs[0]
#         #check if the order item is in order
#         if order.products.filter(product__slug=product.slug).exists():
#             order_product.quantity +=1
#             order_product.save()
#     else:
#         ordered_date=timezone.now()
#         order =Order.objects.create(user=request.user, ordered_date=ordered_date)
#         order.items.add(order_product)
#     return redirect("core:product", slug=slug)
# class ProductListView(ListView):
#     model= ChildProduct
#     context_object_name='childproduct'
#     template_name='products.html'
#     paginate_by=10
#
#
#     def get_context_data(self, **kwargs):
#         kwargs['parent_product']=self.parent_product
#         return super().get_context_data(**kwargs)
#
#     def get_queryset(self):
#         self.parent_product=get_object_or_404(Product, pk=self.kwargs.get('pk'))
#         queryset=self.parent_product.childproduct.order_by('-price')
#         return queryset

# def partner_list_view(request):
#     queryset=Partner.objects.all()
#     context={
#         'partners_list':queryset
#     }
#     return render(request,"partners.html",context)
# Create your views here.
