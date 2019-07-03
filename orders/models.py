from django.db import models
from django.conf import settings
from products.models import ChildProduct

class OrderProduct(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # , blank=True, null=True
    ordered=models.BooleanField(default=False)
    product=models.ForeignKey(ChildProduct, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.type}"

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products=models.ManyToManyField(OrderProduct)
    start_Date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
