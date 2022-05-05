from http import server
from django.shortcuts import render
from .serializers import ProductSerializer, UserSerializerWithToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from shop.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.



@api_view(['GET'])
def getAllProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def getSingleProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


# User Login View with JWT Tokens

    # Customizing the claimed tokens
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v
        return data
    # View for Login with JWT after Serializing the claimed tokens
class MyTokenObtainpairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Register a User
@api_view(['POST'])
def registerUser(request):
    try:
        data = request.data
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            email = data['email'], 
            password = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_200_ERROR)
