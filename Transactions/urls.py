from django.conf.urls import url
from django.urls import include, path

from .views import (
    balance_detail,
    expenses_detail,
    sales_detail
)

app_name ='Transactions'

urlpatterns = [
    path('admin/investments',balance_detail,name='investments'),
    path('admin/expenses',expenses_detail,name='expenses'),
    path('admin/sales', sales_detail,name='sales'),
    # path('addinvestment',InvestmentCreateView.as_view(),name='addinvestment')
]
