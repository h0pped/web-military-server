from select import KQ_NOTE_LOWAT
from unicodedata import category
from xmlrpc.client import ResponseError
from django.shortcuts import render
# import pyrebase
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

from shopapp.serializers import UserSerializer, CategorySerializer, ItemSerializer
from shopapp.models import User, Category, Item


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
                    return Response({"msg": "Succesfully authenticated!"}, status=200)
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

    # else:
    #     qs = User.objects.filter(
    #         email=user_email, password=user_password).first
    #     serializer = UserSerializer(qs)
    #     return Response(serializer.data)

    # def post(self, request, *args, **kwargs):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors)
