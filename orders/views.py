from django.shortcuts import render, redirect
from .models import Order, OrderProduct, Payment, Coupon, BillingAddress, OrderDetail
from Transactions.models import Balance
from django.views.generic import ListView, DetailView, TemplateView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from .forms import CheckoutForm, PaymentForm, CouponForm
from django.core.files.storage import FileSystemStorage

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
                image =form.cleaned_data['transaction_image']
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
        model_name,view=self.__class__.__name__.split('V')
        balance= Balance.objects.all()
        order=Order.objects.filter(ordered=True, status=status).order_by('ordered_date')
        queryset={'balance':balance,'order':order,'model_name':model_name}
        return render(request,self.template_name,queryset)


    def delete(self,request):
        id=json.loads(request.body)['id']
        order=get_object_or_404(Order, id=id)
        order.delete()
        return redirect('Transactions:investments')

class SalesView(PermissionRequiredMixin,TemplateView):
    permission_required='superuserstatus'
    template_name="kgc/sales.html"

    def get(self,request):
        balance=Balance.objects.all()
        order=Order.objects.filter(status="Completed")
        model_name,view=self.__class__.__name__.split('V')
        queryset={'balance':balance,'order':order,'model_name':model_name}
        return render(request,self.template_name,queryset)
