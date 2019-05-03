import random
import os
from django.db import models

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
    title=models.CharField(max_length=50, unique=True)
    short_description=models.CharField(max_length=50,null=True)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2, max_digits=10, null=True)
    image=models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES)
    featured=models.BooleanField(default=False)

    objects= ProductManager()
    def __str__(self):
        return self.title
