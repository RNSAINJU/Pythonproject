from django.db import models
import random
import os
# from .products.models import get_filename_ext, upload_image_path

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

class Partner(models.Model):
        profession=models.CharField(max_length=50, unique=True)
        title=models.CharField(max_length=50, unique=True)
        description=models.TextField()
        image=models.ImageField(upload_to=upload_image_path, null=True, blank=False)
        ytlink=models.CharField(max_length=100, unique=True)
        fblink=models.CharField(max_length=100, unique=True)
        instalink=models.CharField(max_length=100, unique=True)

        def __str__(self):
            return self.title

class Reviews(models.Model):
    image=models.ImageField(upload_to=upload_image_path,null=True, blank=False)
    message=models.CharField(max_length=100, unique=True)
    customername=models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.customername

class News(models.Model):
    title=models.CharField(max_length=50, unique=True)
    description=models.TextField()
    image=models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    date=models.DateField(unique=True)

    def __str__(self):
        return self.title

class Enquiries(models.Model):
    firstname=models.CharField(max_length=100, unique=True)
    lastname=models.CharField(max_length=100, unique=True)
    email=models.CharField(max_length=100, unique=True)
    phoneno=models.CharField(max_length=100, unique=True)
    message=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str(self):
        return self.firstname
