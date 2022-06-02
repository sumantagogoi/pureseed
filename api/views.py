from http import server
from django.shortcuts import render

# from backend.manxho.shop.models import OrderItem


from .serializers import CategorySerializer, ProductSerializer, UserSerializerWithToken, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from shop.models import Product, Category, Order, OrderItem, ShippingAddress
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
    
@api_view(['GET'])
def getAllCategories(request):
     categories = Category.objects.all()
     serializer = CategorySerializer(categories, many=True)
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
            first_name = data['first_name'],
            last_name= data['last_name'],
            username = data['email'],
            email = data['email'], 
            password = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOrder(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']
    if orderItems and len(orderItems) < 1:
        return Response({'message':'No Order Item'})
    else:
        # creat a order 
        order = Order.objects.create(
            user = user,
            totalPrice = data['totalPrice']
        )

        # create Shipping Address for the order 
        shippingAddress = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city =  data['shippingAddress']['city'],
            state =  data['shippingAddress']['state'],
            zipcode =  data['shippingAddress']['zipcode'],
            country = data['shippingAddress']['country'],

        )

        # Create order Item and set the order to OrderItems relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['_id'])

            item = OrderItem.objects.create(
                user = user,
                product = product,
                qty = i['qty'],
                price = product.price,
            )
        return Response({'message':'Order Successfully Created'}, status=status.HTTP_200_OK)

