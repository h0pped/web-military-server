from collections import OrderedDict
from rest_framework import serializers

from .models import Order, User, Category, Item, Order_Item, Order, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'email',
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


class UserField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        id = super(UserField, self).to_representation(value)
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user)
            return serializer.data
        except User.DoesNotExist:
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
                  'price', 'photoPath', 'category', 'avg_rating', 'quantity', 'visible')


class ItemField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        id = super(ItemField, self).to_representation(value)
        try:
            item = Item.objects.get(pk=id)
            serializer = ItemSerializer(item)
            return serializer.data
        except Item.DoesNotExist:
            return None

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}
        return OrderedDict([(item.id, self.display_value(item)) for item in queryset])


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemField(queryset=Item.objects.all())

    class Meta:
        model = Order_Item
        fields = ('id', 'order', 'item', 'price')


class OrderSerializer(serializers.ModelSerializer):
    user = UserField(queryset=User.objects.all())

    class Meta:
        model = Order
        fields = ('id', 'user', 'address', 'country', 'remarks',
                  'zipCode', 'shipment_method', 'order_status')


class ReviewSerializer(serializers.ModelSerializer):
    user = UserField(queryset=User.objects.all())
    item = ItemField(queryset=Item.objects.all())

    class Meta:
        model = Review
        fields = ('id', 'item', 'user', 'rating', 'comment')
