from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Stock(models.Model):
    # name = models.CharField(max_length=200)
    symbol = models.CharField(max_length = 10)
    price = models.FloatField()
    updated = models.DateTimeField(auto_now_add=True)
    change_percent = models.FloatField(default=0.0)

    def __str__(self):
        return self.symbol