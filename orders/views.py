from django.shortcuts import render, redirect
from .models import Order, OrderProduct
from django.views.generic import ListView, DetailView, TemplateView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CheckoutForm


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

        context={
            'form':form
        }
        return render(self.request,'checkout.html',context)

    def post(self, *args, **kwargs):
        form=CheckoutForm(self.request.POST or None)
        if form.is_valid():
            # print("The form is valid")
            # print(form.cleaned_data)
            return redirect('orders:checkout')
        messages.warning(self.request, "Failed checkout")
        return redirect('orders:checkout')
