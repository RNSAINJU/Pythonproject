from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderProduct, Payment, Coupon, BillingAddress, OrderDetail
from Transactions.models import Balance
from django.views.generic import ListView, DetailView, TemplateView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from .forms import Orderdetailform,OrderForm,CheckoutForm, PaymentForm, CouponForm, Payment2Form
from django.core.files.storage import FileSystemStorage
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView, UpdateView, TemplateView
from products.models import Product, ChildProduct
from django.utils import timezone

class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order= Order.objects.get(user=self.request.user,ordered=False)
            context={
                'object':order
            }
            return render(self.request,'cart.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

class CheckOutView(View):
    template_name='checkout.html'

    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            # for order_item in order.products.all:
            #     if order_item.product.parent_product.category == 'Gametopups':
            #     elif order_item.product.parent_product.category  == 'Gamestopup(Loginrequired)':
            # loginrequiredform=TopupLoginForm()
            form=CheckoutForm()
            context={
                'form':form,
                'couponform':CouponForm(),
                'order':order,
                'DISPLAY_COUPON_FORM':True
            }
            return render(self.request,'checkout.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("orders:checkout")


    def post(self, *args, **kwargs):
        form=CheckoutForm(self.request.POST, self.request.FILES or None)
        try:
            order= Order.objects.get(user=self.request.user,ordered=False)

            if form.is_valid():
                print("The form is valid")
                print(form.cleaned_data)
                game_details= form.cleaned_data.get('game_details')
                # save_info= form.cleaned_data.get('save_info')
                image =form.cleaned_data['game_image']
                payment_option= form.cleaned_data.get('payment_option')
                order_details= OrderDetail(
                    user=self.request.user,
                    details=game_details,
                    game_image=image,
                )
                order_details.save()

                order.order_details=order_details
                order.save()

                if payment_option == 'E':
                    return redirect('orders:payment',payment_option='esewa')
                elif payment_option == 'I':
                    return redirect('orders:payment',payment_option='imepay')
                elif payment_option == 'K':
                    return redirect('orders:payment',payment_option='khalti')
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                # print("The form is valid")
                # print(form.cleaned_data)
                return redirect('orders:checkout')
            messages.warning(self.request, "Failed checkout")
            return redirect('orders:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("orders:cart")

class PaymentView(View):
    template_name='payment.html'

    def get(self, *args, **kwargs):
        form=PaymentForm()
        order= Order.objects.get(user=self.request.user,ordered=False)
        if order.order_details:
            context={
                'form':form,
                'order':order,
                'DISPLAY_COUPON_FORM':False
            }
            return render(self.request,'payment.html',context)
        else:
            messages.error(self.request, "You have not  billing address")
            return redirect("orders:checkout")


    def post(self, *args, **kwargs):
        form=PaymentForm(self.request.POST, self.request.FILES or None)
        order= Order.objects.get(user=self.request.user,ordered=False)
        codes=Payment.objects.all()
        # amount=int(order.get_total())

        try:
            if form.is_valid():
                print("The form is valid")
                print(form.cleaned_data)
                transaction_id=form.cleaned_data.get('transaction_id')
                transaction_image =form.cleaned_data['transaction_image']
                type=form.cleaned_data.get('type')
                amount=order.get_total()
                # transaction_codes=
                payment=Payment(
                    transaction_id=transaction_id,
                    transaction_image=transaction_image,
                    user=self.request.user,
                    type=type,
                    amount=amount,
                    status='Verifying payment'
                )
                payment.save()

                order_items= order.products.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.payment=payment
                order.ordered=True
                order.save()

                messages.success(self.request,"Your order was successfull")
                return redirect('orders:orders')
            messages.warning(self.request, "Failed checkout")
            return redirect('orders:payment')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("orders:cart")

#Checks if coupon is valid or not
def get_coupon(request,code):
    try:
        coupon=Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
            messages.info(request, "This coupon does not exist")
            return redirect("orders:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form= CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code=form.cleaned_data.get('code')
                order=Order.objects.get(user=self.request.user,ordered=False)
                order.coupon =get_coupon(self.request, code)
                order.save()
                messages.success(self.request,"Successfully added coupon")
                return redirect("orders:checkout")

            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("orders:checkout")

class OrderView(ListView):
    model=Order
    context_object_name = 'orders'
    # paginate_by = 1
    template_name="orders.html"


    def get_queryset(self):
        order=Order.objects.filter(user=self.request.user,ordered=True).order_by('ordered_date').reverse()
        queryset={'order':order}
        return queryset




class OrdersView(PermissionRequiredMixin,TemplateView):
    permission_required = 'superuserstatus'
    # paginate_by = 1
    template_name="kgc/orders.html"


    def get(self,request,status):
        form=OrderForm()
        detailform=CheckoutForm()
        paymentform=Payment2Form()
        model_name,view=self.__class__.__name__.split('V')
        product=ChildProduct.objects.all()
        balance= Balance.objects.all()
        order=Order.objects.filter(ordered=True, status=status).order_by('ordered_date')
        total=0
        for item in order:
            total +=item.payment.amount
        queryset={'paymentform':paymentform,
                  'detailform':detailform,
                  'product':product,
                  'form':form,
                  'balance':balance,
                  'order':order,
                  'model_name':model_name,
                  'total':total}
        return render(request,self.template_name,queryset)

    def post(self, request,status):
        form=OrderForm(self.request.POST)
        detailform=CheckoutForm(self.request.POST, self.request.FILES or None)
        paymentform=Payment2Form(self.request.POST, self.request.FILES or None)


        if form.is_valid()  & detailform.is_valid() & paymentform.is_valid():
            print("The form is valid")
            print(form.cleaned_data)

            # Order product
            post=form.save(commit=False)
            post.user=self.request.user
            post.ordered=False
            post.quantity=1
            post.save()

            # Order Details
            print(detailform.cleaned_data)
            game_details= detailform.cleaned_data.get('game_details')
            # save_info= form.cleaned_data.get('save_info')
            image =detailform.cleaned_data['game_image']
            payment_option= detailform.cleaned_data.get('payment_option')
            order_details= OrderDetail(
                user=self.request.user,
                details=game_details,
                game_image=image,
            )
            order_details.save()

            #0rder
            ordered_date=timezone.now()
            # cost_price=product.cost_price
            order =Order.objects.create(user=request.user, ordered_date=ordered_date, cost_price=0)
            order.products.add(post)
            order.order_details=order_details
            order.save()

            # Order payment
            # order= Order.objects.get(user=self.request.user,ordered=False)
            transaction_id=paymentform.cleaned_data.get('transaction_id')
            transaction_image=paymentform.cleaned_data['transaction_image']
            # post2=paymentform.save(commit=False)
            if post.product.discount_price:
                final_price=post.product.discount_price
            else:
                final_price=post.product.price

            if payment_option == 'E':
                    payment_option='Esewa'
            elif payment_option == 'I':
                    payment_option='Imepay'
            elif payment_option == 'K':
                payment_option='Khalti'
            else:
                messages.warning(self.request, "Invalid payment option selected")

            payment_details=Payment(
                transaction_id=transaction_id,
                transaction_image=transaction_image,
                user=self.request.user,
                type=payment_option,
                amount=final_price,
                status='Paid',
            )
            # post2.user=self.request.user
            # post2.type=payment_option
            # post2.amount=final_price
            # post2.status='Paid'
            payment_details.save()
            # post2.save()
            order.ordered=True
            order.cost_price=post.product.cost_price
            order.payment=payment_details
            order.save()

            return redirect('orders:orders-admin',status='Pending')

    def delete(self,request,status):
        id=json.loads(request.body)['id']

        payment=Payment.objects.get(order__id=id)
        orderdetails=OrderDetail.objects.get(order__id=id)
        orderedproduct=OrderProduct.objects.get(order__id=id)

        orderdetails.game_image.delete(save=True)
        payment.transaction_image.delete(save=True)

        orderedproduct.delete()
        payment.delete()
        orderdetails.delete()

        order=get_object_or_404(Order, id=id,status=status)
        order.delete()

        return HttpResponse('')

class OrderDetailView(PermissionRequiredMixin,TemplateView):
    permission_required = 'superuserstatus'
    # paginate_by = 1
    template_name="kgc/order-detail.html"

    def get(self,request,pk):
        form=Orderdetailform()
        model_name,view=self.__class__.__name__.split('V')
        balance= Balance.objects.all()
        order=Order.objects.get(id=pk)
        queryset={'form':form,'balance':balance,'order':order,'model_name':model_name}
        return render(request,self.template_name,queryset)

    def post(self, request,pk):
        form=Orderdetailform(self.request.POST)

        if form.is_valid():
            order=get_object_or_404(Order, id=pk)
            message= form.cleaned_data.get('message')
            status=form.cleaned_data.get('status')
            if message !='':
                order.message=message
            if status !='':
                order.status=status
            order.save()
            return redirect('orders:orders-admin',status='Pending')


    def delete(self,request,id):
        id=id
        order=get_object_or_404(Order, id=id)
        order.delete()
        return HttpResponse('')

# @method_decorator(login_required, name='dispatch')
# class OrderDetailView(UpdateView):
#     model = Order
#     fields = ('cost_price', 'order_details', 'message',)
#     template_name = 'order-detail.html'
#     success_url = reverse_lazy('orders:order-detail')
#
#     def get_object(self,pk):
#         return Order.objects.get(id=pk)

class SalesView(PermissionRequiredMixin,TemplateView):
    permission_required='superuserstatus'
    template_name="kgc/sales.html"

    def get(self,request):
        balance=Balance.objects.all()
        order=Order.objects.filter(status="Completed")
        model_name,view=self.__class__.__name__.split('V')
        queryset={'balance':balance,'order':order,'model_name':model_name}
        return render(request,self.template_name,queryset)
