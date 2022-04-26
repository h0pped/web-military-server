from collections import OrderedDict
from rest_framework import serializers

from .models import Order, User, Category, Item, Order_Item


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'surname', 'email',
                  'gender', 'password', 'role')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class CategoryField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        id = super(CategoryField, self).to_representation(value)
        try:
            category = Category.objects.get(pk=id)
            serializer = CategorySerializer(category)
            return serializer.data
        except Category.DoesNotExist:
            return None

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}
        return OrderedDict([(item.id, self.display_value(item)) for item in queryset])


class ItemSerializer(serializers.ModelSerializer):
    category = CategoryField(queryset=Category.objects.all())

    class Meta:
        model = Item
        fields = ('id', 'title', 'description',
                  'price', 'photoPath', 'category', 'avg_rating')


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False)

    class Meta:
        model = Order_Item
        fields = ('id', 'order', 'item', 'price')
