import random
import os
from django.db import models
from django.conf import settings
from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify


def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name,ext=os.path.splitext(base_name)
    return name,ext

def upload_image_path(instance, filename):
    new_filename=random.randint(1,3910209312)
    name, ext= get_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "products/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
    )

class ProductManager(models.Manager):
    def featured(self):
        return self.get_queryset().filter(featured=True)


class Product(models.Model):
    STATUS_CHOICES=(
    ('active','Active'),
    ('in-active','In-active'),
    )

    PAYMENT_CHOICES=(
        ('Paypal','paypal'),
        ('Payoneer','payoneer'),
        )

    title=models.CharField(max_length=50, unique=True,blank=True)
    short_description=models.CharField(max_length=60, unique=True)
    description=models.TextField()
    category =models.ForeignKey('Main_Category', on_delete=models.SET_NULL, blank=True, null=True)
    image=models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES)
    purchase_method=models.CharField(max_length=50,choices=PAYMENT_CHOICES)

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
    cost_price=models.FloatField()
    cost_price_withcharge=models.FloatField()
    total_cost_price=models.IntegerField()
    total_cost_price_with_profit=models.IntegerField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES)
    homefeatured=models.BooleanField(default=False)
    productsfeatured=models.BooleanField(default=False)
    enabledetail=models.BooleanField(default=False)
    slug=models.SlugField(max_length=100,unique=True,blank=True)

    objects= ProductManager()

    def save(self, *args, **kwargs):
        self.slug=slugify(self.type)
        self.cost_price_withcharge=self.cost_price+(2.90/100*self.cost_price)+0.30
        # rate=Balance.objects.get(name='Paypal')
        rate=120
        self.total_cost_price=self.cost_price_withcharge*rate
        cp_withprofit=(self.cost_price_withcharge+(30/100*self.cost_price_withcharge))
        self.total_cost_price_with_profit=cp_withprofit*(rate)
        super(ChildProduct,self).save(*args,**kwargs)

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
                'slug':self.slug
                })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug':self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug':self.slug
        })

class Main_Category(models.Model):
    name=models.CharField(max_length=50, unique=True,blank=True)

    def __str__(self):
        return self.name
