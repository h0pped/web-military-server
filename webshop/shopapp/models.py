from tkinter import CASCADE
from turtle import ondrag
from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=1)
    # age = models.DateField()

    def __str__(self) -> str:
        return self.email


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)


class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.FloatField(default=0)
    photoPath = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    avg_rating = models.FloatField(default=0)


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    remarks = models.CharField(max_length=200)
    zipCode = models.CharField(max_length=10)
    shipment_method = models.CharField(max_length=50)
    order_status = models.CharField(max_length=20)
    items = models.ManyToManyField(Item, through='Order_Item')


class Order_Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
