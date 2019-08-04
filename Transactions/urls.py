from django.conf.urls import url
from django.urls import include, path

from .views import *
app_name ='Transactions'

urlpatterns = [
    path('kgc/',DashboardView.as_view(), name='kgc_admin'),
    path('kgc/investments',InvestmentView.as_view(),name='investments'),
    path('kgc/expenses',ExpensesView.as_view(),name='expenses'),

    # path('addinvestment',InvestmentCreateView.as_view(),name='addinvestment')


]
