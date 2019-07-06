from django.shortcuts import render, redirect
from .models import Order, OrderProduct, BillingAddress, Payment, Coupon
from django.views.generic import ListView, DetailView, TemplateView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CheckoutForm, PaymentForm


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
        form=CheckoutForm()
        order= Order.objects.get(user=self.request.user,ordered=False)

        context={
            'form':form,
            'order':order
        }
        return render(self.request,'checkout.html',context)

    def post(self, *args, **kwargs):
        form=CheckoutForm(self.request.POST or None)
        try:
            order= Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                street_address= form.cleaned_data.get('street_address')
                secondary_address= form.cleaned_data.get('secondary_address')
                # save_info= form.cleaned_data.get('save_info')
                payment_option= form.cleaned_data.get('payment_option')
                billing_address= BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    secondary_address=secondary_address
                )
                billing_address.save()
                order.billing_address=billing_address
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
        context={
            'form':form,
            'order':order
        }
        return render(self.request,'payment.html',context)


    def post(self, *args, **kwargs):
        form=PaymentForm(self.request.POST or None)
        order= Order.objects.get(user=self.request.user,ordered=False)
        # amount=int(order.get_total())
        try:
            if form.is_valid():
                transaction_id=form.cleaned_data.get('transaction_id')
                amount=order.get_total()
                payment=Payment(
                    transaction_id=transaction_id,
                    user=self.request.user,
                    amount=amount
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
                return redirect('home')
            messages.warning(self.request, "Failed checkout")
            return redirect('orders:payment')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("orders:cart")

#Checks if coupon is valid or not
def get_coupon(request,code):
    try:
        coupon=Coupon.object.get(code=code)
        return coupon
    except ObjectDoesNotExist:
            messages.info(request, "This coupn does not exist")
            return redirect("orders:checkout")

def add_coupon(request, code):
    try:
        order=Order.objects.get(user=request.user,ordered=false)
        coupon=get_coupon(request, code)

    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("orders:checkout")
