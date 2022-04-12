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
