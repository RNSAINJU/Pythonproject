from django.db import models
from django.conf import settings
from products.models import ChildProduct
import random
import os


class OrderProduct(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    product=models.ForeignKey(ChildProduct, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.type}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price()-self.get_total_discount_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_price()
        return self.get_total_product_price()

class Order(models.Model):
    STATUS_CHOICES=(
        ('Pending','pending'),
        ('Processing','processing'),
        ('Completed','completed'),
        )

    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cost_price=models.FloatField()
    products=models.ManyToManyField(OrderProduct)
    start_Date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    billing_address =models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    order_details =models.ForeignKey(
    'OrderDetail', on_delete=models.SET_NULL, blank=True, null=True)
    payment =models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon=models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    message=models.TextField(blank=True, null=True)

    def total_sales_amount(self):
        # Fetchs dollar added
        sales_list=Order.objects.filter(status="Completed")
        total_sales_amount=0
        for item in sales_list:
            total_sales_amount += item.payment.amount

        return total_sales_amount

    def total_paypal_sales_amount(self):
        # Fetchs dollar added
        sales_list=Order.objects.filter(status="Completed")
        total_sales_amount=0
        for item in sales_list:
            total_sales_amount += item.cost_price

        return total_sales_amount


    def total_sales(self):
        # Fetchs dollar added
        sales_list=Order.objects.filter(status="Completed").count()
        return sales_list

    def total_profit(self):
        # Fetchs dollar added
        list=Order.objects.filter(status="Completed")
        total_sales_amount=0
        total_cost_price=0
        for item in list:
            total_sales_amount += item.payment.amount
        for item in list:
            total_cost_price += item.cost_price

        return total_sales_amount- (total_cost_price*121)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

class BillingAddress(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete =models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return self.details

def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name,ext=os.path.splitext(base_name)
    return name,ext

def upload_image_path1(instance, filename):
    new_filename=random.randint(1,3910209312)
    name, ext= get_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "gamedetails/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
    )

class OrderDetail(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete =models.CASCADE)
    details = models.TextField()
    game_image=models.ImageField(upload_to=upload_image_path1, null=True, blank=False)

    def __str__(self):
        return self.details

def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name,ext=os.path.splitext(base_name)
    return name,ext

def upload_image_path(instance, filename):
    new_filename=random.randint(1,3910209312)
    name, ext= get_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "payments/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
    )

class Payment(models.Model):
    PAYMENT_CHOICES=(
        ('Esewa','esewa'),
        ('Imepay','imepay'),
        ('Khalti','khalti'),
        )

    STATUS_CHOICES=(
        ('Not paid','not paid'),
        ('Verifying payment','verifing payment'),
        ('Paid','paid'),
        )

    transaction_id= models.CharField(max_length=50)
    transaction_image=models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    type=models.CharField(max_length=50,choices=PAYMENT_CHOICES)
    amount =models.FloatField()
    status=models.CharField(max_length=50,choices=STATUS_CHOICES, default='verifing payment')
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id

class Coupon(models.Model):
    code=models.CharField(max_length=15)
    amount =models.FloatField()

    def __str__(self):
        return self.code
