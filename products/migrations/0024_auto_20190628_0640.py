# Generated by Django 2.1.7 on 2019-06-28 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20190628_0638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discount_price',
            new_name='hover',
        ),
    ]