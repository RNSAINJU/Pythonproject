# Generated by Django 2.1.7 on 2019-06-27 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20190627_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='childproduct',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
    ]
