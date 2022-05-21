from dataclasses import fields
from xml.parsers.expat import model

from rest_framework import serializers
from shop.models import Product, Category
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)


    class Meta:
        fields = ['id', '_id', 'username', 'email', 'first_name', 'last_name', 'name', 'isAdmin']


    def get_name(self,obj):
        name = obj.first_name 
        if name == "":
            name = obj.email 
        return name

    def get__id(self, obj):
         return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'first_name', 'last_name', 'name', 'isAdmin', 'token']

    def get_token(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)