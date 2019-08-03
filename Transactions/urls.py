from django.conf.urls import url
from django.urls import include, path

from .views import (
    balance_detail,
    expenses_detail,
    sales_detail,
    pending_orders_detail
)

app_name ='Transactions'

urlpatterns = [
    path('kgc/pending-orders', pending_orders_detail,name='pending-orders'),
    path('kgc/investments',balance_detail,name='investments'),
    path('kgc/expenses',expenses_detail,name='expenses'),
    path('kgc/sales', sales_detail,name='sales'),
    # path('addinvestment',InvestmentCreateView.as_view(),name='addinvestment')


]
