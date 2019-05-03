# Generated by Django 2.1.7 on 2019-05-03 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=10, unique=True)),
                ('lastname', models.CharField(max_length=10, unique=True)),
                ('email', models.CharField(max_length=10, unique=True)),
                ('phoneno', models.IntegerField(max_length=10)),
                ('message', models.TextField()),
            ],
        ),
    ]
