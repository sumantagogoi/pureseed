from dataclasses import fields
from xml.parsers.expat import model



from rest_framework import serializers
from shop.models import Product, Category, OrderItem, ShippingAddress,Order, Coupons
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
    
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)


    class Meta:
        fields = ['id', '_id', 'username', 'email', 'first_name', 'last_name', 'isAdmin']


    def get__id(self, obj):
         return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'first_name', 'last_name',  'isAdmin', 'token']

    def get_token(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

        def get_orderItems(self, obj):
            items = obj.orderitem.set.all()
            serializer = OrderItemSerializer(items, many=True)
            return serializer.data
        def get_shippingAddress(self, obj):
            try:
                address = ShippingAddressSerializer(obj.shippingAddress, many=False).data
            except:
                address= False
            return address

        def get_user(self, obj):
            user = obj.user
            serializer = UserSerializer(user, many=False)
            return serializer.data

class CouponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupons
        fields = ['id', 'discount', 'is_active', 'code', 'discount_type', 'max_limit']
