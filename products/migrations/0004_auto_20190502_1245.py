# Generated by Django 2.1.7 on 2019-05-02 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_partner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='fblink',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='instalink',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='ytlink',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]