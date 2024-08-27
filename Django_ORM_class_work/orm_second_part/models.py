from django.db import models
from django.db.models import CharField, IntegerField, DecimalField

# Create your models here.


class Product(models.Model):
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    category = CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    products = models.ManyToManyField(Product, related_name='orders', through='OrderPosition')

class OrderPosition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='positions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='positions')
    quantity = IntegerField()
    
