# Generated by Django 2.1.7 on 2019-05-02 12:19

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_featured'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=50, unique=True)),
                ('title', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to=products.models.upload_image_path)),
                ('ytlink', models.CharField(max_length=50, unique=True)),
                ('fblink', models.CharField(max_length=50, unique=True)),
                ('instalink', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
