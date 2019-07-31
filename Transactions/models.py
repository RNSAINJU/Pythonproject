from django.db import models
from django.utils.text import slugify
from orders.models import Order

class Balance(models.Model):
    name=models.CharField(max_length=50)
    amount=models.FloatField()
    slug=models.SlugField(max_length=100,unique=False,blank=True)



    def __str__(self):
        return self.name

    def balance_left(self):
        # Fetchs dollar added
        investment_list=Investment.objects.filter(type=self)
        investment_list2=Investment.objects.filter(type2=self)

        sales_list=Order.objects.filter(status="Completed",payment__type=self)
        dollar_expense_list=Order.objects.filter(status="Completed",products__product__parent_product__purchase_method=self)
        expense_list=Expense.objects.filter(type=self)
        total_sales_amount=0
        total_invest_amount=0
        total_invest_expense=0
        total_expense_amount=0
        total_dollar_amount=0
        for item in investment_list:
            total_invest_amount += item.amount
        for item in expense_list:
            total_expense_amount +=item.amount
        for item in sales_list:
            total_sales_amount +=item.payment.amount
        for item in dollar_expense_list:
            total_dollar_amount +=item.cost_price
        for item in investment_list2:
            total_invest_expense +=item.total

        return (self.amount + total_invest_amount + total_sales_amount) -total_expense_amount - total_dollar_amount- total_invest_expense

    # def get_percentage(self):
    #     investment_list=Investment.objects.filter(type=self)
    #     total_invest_amount=0
    #     for item in investment_list:
    #         total_invest_amount += item.amount
    #
    #     return total_invest_amount *100/self.amount
    #
    # def total_transactions(self):
    #     expense_list=Expense.objects.filter(name=self)
    #


class Expense(models.Model):
    transaction_name=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    amount=models.FloatField()


    def __str__(self):
        return self.transaction_name

    # def add_expense(self):
    #     balance=Balance.objects.get(name=self.type)
    #     balance.amount=balance.amount-amount
    #     balance.save()


class Investment(models.Model):
    name=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    rate=models.FloatField()
    type2=models.CharField(max_length=7,default="Esewa")
    # models.ForeignKey(Balance,on_delete=models.CASCADE, related_name='investment')
    amount=models.FloatField()
    total=models.FloatField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.rate=self.total/self.amount
        super(Investment,self).save(*args,**kwargs)

    # def add_investment(self):
    #     balance=Balance.objects.get(name=self.type)
    #     print(balance.amount)
    #     balance.amount=balance.amount+amount
    #     balance.save()
