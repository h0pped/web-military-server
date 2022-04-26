from django.contrib import admin
from .models import User, Category, Item, Order, Order_Item


# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order_Item)
admin.site.register(Order)
