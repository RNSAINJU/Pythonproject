from django.db import models
from django.utils.text import slugify
from orders.models import Order


class Balance(models.Model):
    name=models.CharField(max_length=50)
    amount=models.FloatField()
    rate=models.IntegerField()
    date=models.DateField(blank=True)
    slug=models.SlugField(max_length=100,unique=False,blank=True)


    def __str__(self):
        return self.name

    def balance_left(self):
        # Fetchs dollar added
        investment_list=Investment.objects.filter(type=self)
        other_investments=Investment.objects.filter(type2=self)

        sales_list=Order.objects.filter(status="Completed",payment__type=self)
        dollar_expense_list=Order.objects.filter(status="Completed",products__product__parent_product__purchase_method=self)
        expense_list=Expense.objects.filter(type=self)

        total_sales_amount=total_invest_amount=total_invest_expense=total_expense_amount=total_dollar_amount=0

        for item in investment_list:
            total_invest_amount += item.amount
        for item in expense_list:
            total_expense_amount +=item.amount
        for item in sales_list:
            total_sales_amount +=item.payment.amount
        for item in dollar_expense_list:
            total_dollar_amount +=item.cost_price
        for item in other_investments:
            total_invest_expense +=item.total

        return (self.amount + total_invest_amount + total_sales_amount) -total_expense_amount - total_dollar_amount- total_invest_expense

    # def total_investment_paypal()
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
    TYPECHOICES=(
    ('Esewa','esewa'),
    ('Credit','credit'),
    )

    name=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    rate=models.FloatField(null=True, blank=True, default=0.0)
    type2=models.CharField(blank=True,max_length=7,choices=TYPECHOICES)
    amount=models.FloatField(null=True, blank=True, default=0.0)
    total=models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.total is None:
            self.total=0.0
            if self.rate is None:
                self.total=self.amount
                self.rate=0.0
            else:
                self.total=self.rate*self.amount
        elif self.rate is None:
            self.rate=0.0
            if self.total is None:
                self.total=0.0
                self.total=self.amount
            else:
                self.rate=self.total/self.amount


        super(Investment,self).save(*args,**kwargs)

    # def add_investment(self):
    #     balance=Balance.objects.get(name=self.type)
    #     print(balance.amount)
    #     balance.amount=balance.amount+amount
    #     balance.save()
