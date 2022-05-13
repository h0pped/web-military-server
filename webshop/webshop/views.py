from select import KQ_NOTE_LOWAT
from unicodedata import category
from xmlrpc.client import ResponseError
from django.shortcuts import render
# import pyrebase
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

from shopapp.models import User, Category, Item, Order_Item, Order, Review
from shopapp.serializers import OrderSerializer, UserSerializer, CategorySerializer, ItemSerializer, OrderItemSerializer, ReviewSerializer


class UserView(APIView):

    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_email = request.query_params.get('user_email')
        user_password = request.query_params.get('user_password')
        if user_email is None:
            qs = User.objects.all()
            serializer = UserSerializer(qs, many=True)
            return Response(serializer.data)
        else:
            if user_password is None:
                qs = User.objects.filter(email=user_email)
                user = qs.first()
                if user is not None:
                    serializer = UserSerializer(user)
                    return Response(serializer.data)
                else:
                    return Response({"error": "No such user"}, status=404)
            else:
                qs = User.objects.filter(
                    email=user_email, password=user_password)
                user = qs.first()
                if user is not None:
                    serializer = UserSerializer(user)
                    return Response({"msg": "Succesfully authenticated!", "id": user.id}, status=200)
                else:
                    return Response({"error": "No user with such credentials"}, status=404)

            # else:
            #     qs = User.objects.filter(
            #         email=user_email, password=user_password).first
            #     serializer = UserSerializer(qs)
            #     return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)


class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Category.objects.all()
        serializer = CategorySerializer(qs, many=True)
        return Response(serializer.data)


class ItemView(APIView):
    def get(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id')
        item_id = request.query_params.get('item_id')
        recent = request.query_params.get('recent')
        if(recent):
            qs = Item.objects.all()
        if item_id is not None:
            qs = Item.objects.filter(id=item_id)
            item = qs.first()
            if item is not None:
                serializer = ItemSerializer(item)
                return Response(serializer.data)
            else:
                return Response({"error": "No such item"}, status=404)
        if category_id is not None:
            print(category_id)
            qs = Item.objects.filter(category=category_id)
        else:
            qs = Item.objects.all()
        serializer = ItemSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)


class OrderItemView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Order_Item.objects.all()
        serializer = OrderItemSerializer(qs, many=True)
        return Response(serializer.data, status=200)


class OrderView(APIView):
    def get(self, request, *args, **kwargs):
        order_id = request.query_params.get('order_id')
        user_id = request.query_params.get('user_id')
        if order_id is not None:
            qs = Order.objects.filter(id=order_id)
            item = qs.first()
            qs_order_items = Order_Item.objects.filter(order=order_id)
            serializer = OrderSerializer(item)
            order_items_serializer = OrderItemSerializer(
                qs_order_items, many=True)
            total = 0
            for item in order_items_serializer.data:
                total += item['item']['price'] * item['quantity']
            return Response({"order": serializer.data, "items": order_items_serializer.data, "total": total})
            data = {
                'order': serializer.data,
                'order_items': order_items_serializer.data
            }
            return Response(data, status=200)
        if user_id is not None:
            user = User.objects.filter(id=user_id).first()
            qs = Order.objects.filter(user=user)
            orders = qs.all()
            orders_serializer = OrderSerializer(orders, many=True)
            for order in orders_serializer.data:
                qs_order_items = Order_Item.objects.filter(order=order['id'])
                order_items_serializer = OrderItemSerializer(
                    qs_order_items, many=True)
                order['order_items'] = order_items_serializer.data
            return Response(orders_serializer.data, status=200)
        if user_id is None and order_id is None:
            qs = Order.objects.all()
            orders = qs.all()
            orders_serializer = OrderSerializer(orders, many=True)
            for order in orders_serializer.data:
                qs_order_items = Order_Item.objects.filter(order=order['id'])
                order_items_serializer = OrderItemSerializer(
                    qs_order_items, many=True)
                order['order_items'] = order_items_serializer.data
            return Response(orders_serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        orderSerializer = OrderSerializer(data=request.data['order'])
        if orderSerializer.is_valid():
            order = orderSerializer.save()
            for item in request.data['items']:
                item['order'] = order.id
                itemSerializer = OrderItemSerializer(data=item)
                if itemSerializer.is_valid():
                    itemSerializer.save()
                    print(f'{item["item"]} was saved')
                else:
                    print(itemSerializer.errors)
            return Response(request.data['order'], status=201)
        print(orderSerializer.errors)
        return Response(request.data['order'], status=500)


class ReviewView(APIView):
    def get(self, request, *args, **kwargs):
        item_id = request.query_params.get('item_id')
        if item_id is not None:
            qs = Review.objects.filter(item=item_id)
            serializer = ReviewSerializer(qs, many=True)
            return Response(serializer.data, status=200)
        qs = Review.objects.all()
        serializer = ReviewSerializer(qs, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            item = Item.objects.filter(id=request.data['item']).first()
            item_reviews = Review.objects.filter(item=item)
            item_reviews_serializer = ReviewSerializer(item_reviews, many=True)
            rating_sum = 0
            for review in item_reviews_serializer.data:
                rating_sum += review['rating']
            avg_rating = rating_sum / len(item_reviews_serializer.data)
            item.__setattr__('avg_rating', avg_rating)
            item.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)
