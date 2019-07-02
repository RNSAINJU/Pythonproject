import random
import os
from django.db import models
from django.conf import settings
from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy

def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name,ext=os.path.splitext(base_name)
    return name,ext

def upload_image_path(instance, filename):
    new_filename=random.randint(1,3910209312)
    name, ext= get_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
    )

class ProductManager(models.Manager):
    def featured(self):
        return self.get_queryset().filter(featured=True)
    # def get_by_status(self, status):
    #     qs=self.queryset().filter(status='active')
    #     if qs.co

class Product(models.Model):
    STATUS_CHOICES=(
    ('active','Active'),
    ('in-active','In-active'),
    )
    # TYPE_CHOICES=(
    # ('parent','Parent'),
    # ('child','Child'),
    # )
    # type=models.CharField(blank=True,max_length=50,choices=TYPE_CHOICES)
    title=models.CharField(max_length=50, unique=True,blank=True)
    short_description=models.CharField(max_length=40, unique=True)
    description=models.TextField()
    image=models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES)
    featured=models.BooleanField(default=False)
    hover=models.DecimalField(decimal_places=2, max_digits=10, blank=True,null=True)

    objects= ProductManager()
    def __str__(self):
        return self.title

class ChildProduct(models.Model):
    STATUS_CHOICES=(
    ('active','Active'),
    ('in-active','In-active'),
    )
    parent_product=models.ForeignKey(Product, related_name='childproduct', on_delete=models.CASCADE)
    type=models.CharField(max_length=50,null=True)
    price=models.DecimalField(decimal_places=2, max_digits=10, blank=True,null=True)
    discount_price=models.DecimalField(decimal_places=2, max_digits=10, blank=True,null=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES)

    featured=models.BooleanField(default=False)
    slug=models.SlugField()

    objects= ProductManager()

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
                'slug':self.slug
                })

    # def get_add_to_cart_url(self):
    #     return reverse("core:add-to-cart", kwargs={
    #         'slug':self.slug
    #     })

class OrderProduct(models.Model):
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
        return self.title
