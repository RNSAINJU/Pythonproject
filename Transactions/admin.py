from django.contrib import admin

from .models import Balance, Expense,Investment

class BalanceAdmin(admin.ModelAdmin):
    list_display=['name','amount','rate','date']
    list_display_links=('name','amount')

class ExpenseAdmin(admin.ModelAdmin):
    list_display=['transaction_name','amount']
    list_display_links=('transaction_name','amount')

class InvestmentAdmin(admin.ModelAdmin):
    list_display=['name','type','amount']
    list_display_links=('name','type')

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Balance, BalanceAdmin)
