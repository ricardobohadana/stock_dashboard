# Generated by Django 3.0.5 on 2020-04-22 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200421_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]