# Generated by Django 3.0.5 on 2020-05-05 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_wallet_buy_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='symbol',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
