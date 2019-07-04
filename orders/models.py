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

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        return total
