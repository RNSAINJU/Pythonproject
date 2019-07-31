from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView
from .models import Balance, Expense, Investment
from orders.models import Order
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import InvestmentForm, ExpenseForm
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.contrib.auth.decorators import login_required, permission_required


# class BalanceView(PermissionRequiredMixin,TemplateView):
#     permission_required = 'superuserstatus'
#     # paginate_by = 1
#     template_name="kgc/balance.html"
#
#
#     def get(self,request):
#         form=InvestmentForm()
#         balance=Balance.objects.all()
#         investment=Investment.objects.all()
#         queryset={'form':form,'balance':balance,'investment':investment}
#         return render(request,self.template_name,queryset)
#
#     def post(self,request):
#         form=InvestmentForm(request.POST)
#         if form.is_valid():
#             post=form.save(commit=False)
#             post.save()
#             return redirect('Transactions:balance')
#         elif request.method == 'DELETE':
#             id=json.loads(request.body)['id']
#             print(id)
#             expense=get_object_or_404(Expense, id=id)
#             expense.delete()
#             return HttpResponse('')
#         else:
#             form=InvestmentForm()
#         return render(request, self.template_name,{'form':form})

@login_required
@permission_required('superuserstatus', raise_exception=True)
def balance_detail(request):
    balance= Balance.objects.all()
    investment=Investment.objects.all()

    if request.method == 'GET':
        form=InvestmentForm()
        queryset={'balance':balance,'investment':investment,'form':form}
        return render(request,'kgc/investment.html',queryset)

    elif request.method =='POST':
        form=InvestmentForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()
            return redirect('Transactions:investments')

    elif request.method == 'DELETE':
        id=json.loads(request.body)['id']
        investment=get_object_or_404(Investment, id=id)
        investment.delete()
        return redirect('Transactions:investments')

    return redirect('Transactions:investments')

@login_required
@permission_required('superuserstatus', raise_exception=True)
def sales_detail(request):
    balance= Balance.objects.all()
    order=Order.objects.filter(status="Completed")

    if request.method == 'GET':
        queryset={'balance':balance,'order':order}
        return render(request,'kgc/sales.html',queryset)

    elif request.method =='POST':
        form=InvestmentForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()
            return redirect('Transactions:balance')

    elif request.method == 'DELETE':
        id=json.loads(request.body)['id']
        investment=get_object_or_404(Investment, id=id)
        investment.delete()
        return redirect('Transactions:balance')

    return redirect('Transactions:balance')

@login_required
@permission_required('superuserstatus', raise_exception=True)
def expenses_detail(request):
    balance= Balance.objects.all()
    expenses=Expense.objects.all()

    if request.method == 'GET':
        form=ExpenseForm()
        queryset={'balance':balance,'expenses':expenses,'form':form}
        return render(request,'kgc/expenses.html',queryset)

    elif request.method =='POST':
        form=ExpenseForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()
            return redirect('Transactions:expenses')

    elif request.method == 'DELETE':
        id=json.loads(request.body)['id']
        investment=get_object_or_404(Expense, id=id)
        investment.delete()
        return redirect('Transactions:expenses')

    return redirect('Transactions:expenses')
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
