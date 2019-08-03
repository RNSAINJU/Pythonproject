from django.shortcuts import get_object_or_404,render
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Product,ChildProduct
from orders.models import OrderProduct,Order
from django.shortcuts import reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

class ProductView(ListView):
    model=ChildProduct
    context_object_name = 'child'
    # paginate_by = 1
    template_name="products.html"


    def get_queryset(self):
        product=ChildProduct.objects.filter(productsfeatured=True)
        queryset={'products':product}
        return queryset

def load_prices(request):
    childproduct_id=request.GET.get('childproduct')
    price=ChildProduct.objects.filter(childproduct_id=childproduct_id).order_by('type')
    return render(request,'hr/prices_list.html',{'price':price})


def product_type(request, pk):
    queryset=ChildProduct.objects.filter(parent_product_id=pk).order_by('price')
    queryset2=Product.objects.get(id=pk)
    context={
        'products':queryset,
        'product':queryset2
    }
    return render(request,"options.html",context)

def product_category(request, pk):
    queryset=ChildProduct.objects.filter(parent_product_category_id=pk)
    # queryset2=Product.objects.get(id=pk)
    context={
        'products':queryset,
    }
    return render(request,"options.html",context)


class ProductDetailView(DetailView):
    model= ChildProduct
    template_name= "product.html"
#
# class ProductOptions(ListView):
#     model=ChildProduct
#     context_object_name='items'
#     template_name='alloptions.html'
#
#     # def get_context_data(self, **kwargs):
#     #     kwargs['childproduct']
#     def get_queryset(self):
#         self.product=get_object_or_404(ChildProduct, parent_product__pk=self.kwargs.get('parent_product_pk'))
#         queryset=self.

@login_required
def add_to_cart(request,slug):
    product=get_object_or_404(ChildProduct,slug=slug)
    order_product, created=OrderProduct.objects.get_or_create(
    product=product,
    user=request.user,
    ordered=False
    )
    order_qs=Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order= order_qs[0]
        #check if the order item is in order
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity +=1
            order_product.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("orders:cart")
        else:
            messages.info(request, "This item was added to your cart.")
            order.products.add(order_product)
            return redirect("orders:cart")
    else:
        ordered_date=timezone.now()
        cost_price=product.cost_price
        order =Order.objects.create(user=request.user, ordered_date=ordered_date, cost_price=cost_price)
        order.products.add(order_product)
        messages.info(request, "This item was added to your cart.")
        return redirect("orders:cart")

def remove_from_cart(request, slug):
    product=get_object_or_404(ChildProduct,slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order= order_qs[0]
        #check if the order item is in order
        if order.products.filter(product__slug=product.slug).exists():
            order_product=OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
                )[0]
            order.products.remove(order_product)
            messages.info(request, "This item was removed from your cart.")
            return redirect("orders:cart")
        else:
            #add a message saying user doent have order
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("core:product", slug=slug)

def remove_single_item_from_cart(request, slug):
    product=get_object_or_404(ChildProduct,slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order= order_qs[0]
        #check if the order item is in order
        if order.products.filter(product__slug=product.slug).exists():
            order_product=OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
                )[0]
            if order_product.quantity >1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, "This item quantity was updated.")
            return redirect("orders:cart")
        else:
            #add a message saying user doent have order
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("core:product", slug=slug)

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
