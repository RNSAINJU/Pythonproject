from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView

from .models import Balance, Expense, Investment
from products.models import Product
from django.contrib.auth.models import User
from orders.models import Order
from boards.models import Board
from home.models import Enquiries

from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import InvestmentForm, ExpenseForm
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.contrib.auth.decorators import login_required, permission_required


class InvestmentView(PermissionRequiredMixin,TemplateView):
    permission_required = 'superuserstatus'
    # paginate_by = 1
    template_name="kgc/investment.html"


    def get(self,request):
        form=InvestmentForm()
        model_name,view=self.__class__.__name__.split('V')
        balance=Balance.objects.all()
        investment=Investment.objects.all()
        queryset={'form':form,'balance':balance,'investment':investment,'model_name':model_name}
        return render(request,self.template_name,queryset)

    def post(self,request):
        form=InvestmentForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()
            return redirect('Transactions:investments')

    def delete(self,request):
        id=json.loads(request.body)['id']
        investment=get_object_or_404(Investment, id=id)
        investment.delete()
        return redirect('Transactions:investments')

class ExpensesView(PermissionRequiredMixin,TemplateView):
    permission_required = 'superuserstatus'
    # paginate_by = 1
    template_name="kgc/expenses.html"


    def get(self,request):
        form=ExpenseForm()
        balance= Balance.objects.all()
        expenses=Expense.objects.all()
        model_name,view=self.__class__.__name__.split('V')
        queryset={'balance':balance,'expenses':expenses,'form':form,'model_name':model_name}
        return render(request,self.template_name,queryset)

    def post(self,request):
        form=ExpenseForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()
            return redirect('Transactions:expenses')

    def delete(self,request):
        id=json.loads(request.body)['id']
        expense=get_object_or_404(Expense, id=id)
        expense.delete()
        return redirect('Transactions:expenses')


class DashboardView(PermissionRequiredMixin,TemplateView):
    permission_required = 'superuserstatus'
    # paginate_by = 1
    template_name="kgc/index.html"


    def get(self,request):
        form=ExpenseForm()
        product=Product.objects.all().count()
        users=User.objects.all().count()
        order=Order.objects.filter(status="Completed")
        sales=Order.objects.filter(status="Completed").count()
        users_list=User.objects.all()
        balance= Balance.objects.all()
        expenses=Expense.objects.all()
        model_name,view=self.__class__.__name__.split('V')
        queryset={'product':product,
                  'users':users,
                  'sales':sales,
                  'order':order,
                  'users_list':users_list,
                  'balance':balance,
                  'expenses':expenses,
                  'form':form,
                  'model_name':model_name
                  }
        return render(request,self.template_name,queryset)


# @login_required
# @permission_required('superuserstatus', raise_exception=True)
# def balance_detail(request):
#     balance= Balance.objects.all()
#     investment=Investment.objects.all()
#
#     if request.method == 'GET':
#         form=InvestmentForm()
#         queryset={'balance':balance,'investment':investment,'form':form}
#         return render(request,'kgc/investment.html',queryset)
#
#     elif request.method =='POST':
#         form=InvestmentForm(request.POST)
#         if form.is_valid():
#             post=form.save(commit=False)
#             post.save()
#             return redirect('Transactions:investments')
#
#     elif request.method == 'DELETE':
#         id=json.loads(request.body)['id']
#         investment=get_object_or_404(Investment, id=id)
#         investment.delete()
#         return redirect('Transactions:investments')
#
#     return redirect('Transactions:investments')


# class InvestmentCreateView(CreateView):
#     model=Balance
#     template_name='kgc/add-investment.html'
#     fields=('name','amount')
#
#     def form_valid(self,form):
#         self.object=form.save(commit=False)
#         self.object.save()
#
#         return HttpResponseRedirect(self.get_success_url())
#
#     def get_success_url(self):
#         return slugify(self.request.POST['name'])

# def project_detail(request,project_slug):
#     project=get_object_or_404(Balance,slug=slug)
#     return render(request,'')
