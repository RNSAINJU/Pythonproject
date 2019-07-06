from django.db import models
from django.conf import settings
from products.models import ChildProduct

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
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products=models.ManyToManyField(OrderProduct)
    start_Date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    billing_address =models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment =models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon=models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        return total

class BillingAddress(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete =models.CASCADE)
    street_address = models.CharField(max_length=100)
    secondary_address = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    transaction_id= models.CharField(max_length=50)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount =models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code=models.CharField(max_length=15)

    def __str__(self):
        return self.code
# class OrderDetails(models.Model):
#     game_id
#     game_name
#     image=
