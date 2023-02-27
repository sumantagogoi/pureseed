from genericpath import exists
from http import server
from time import timezone
from django.shortcuts import render

from django.contrib.auth.models import User
from accounts.models import ResetPasswordToken
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from rest_framework.views import APIView 

# from backend.manxho.shop.models import OrderItem


from .serializers import CategorySerializer, CouponsSerializer, OrderSerializer, ProductSerializer, UserSerializerWithToken, UserSerializer, OrderSerializer, PinCodeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from shop.models import Product, Category, Order, OrderItem, ShippingAddress, Coupons, PinCode
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random, string

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.utils import timezone



from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

# Create your views here.



@api_view(['GET'])
def getAllProducts(request):
    products = Product.objects.all().order_by("-order")
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def getSingleProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def getAllCategories(request):
     categories = Category.objects.all().order_by('-order')
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


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'https://api.manxho.co.in/api/users/'
    client_class = OAuth2Client

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status = status.HTTP_200_OK)





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
            totalPrice = data['totalPrice'],
            coupon = data['coupon'],
            shippingPrice = data['shippingPrice'],
        )

        # create Shipping Address for the order 
        shippingAddress = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city =  data['shippingAddress']['city'],
            state =  data['shippingAddress']['stateValue'],
            phone_number = data['shippingAddress']['phoneNumber'],
            zipcode =  data['shippingAddress']['zipcode'],
            country = data['shippingAddress']['country'],


        )
        try:
            coupon = Coupons.objects.get(code = order.coupon)
            coupon.max_limit -=1
            coupon.save()
        except:
            pass

            

        # Create order Item and set the order to OrderItems relationship
        for i in orderItems:
            print(i['_id'])
            product = Product.objects.get(_id=i['_id'])

            item = OrderItem.objects.create(
                user = user,
                order=order,
                product = product,
                qty = i['qty'],
                price = product.price,
                image= product.image.url,
                name=product.title,
            )
        
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)




class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        user = User.objects.get(email=email)
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _i in range(12))

        ResetPasswordToken.objects.create(
            email=email,token=token,
        )

        message = render_to_string("password_reset_email.html", {
            'user':user,
            'token':token,
        })

        send_mail(
            subject='Password Reset Link',
            message=message,
            recipient_list=[email],
            from_email= 'manxho@xynocast.com',
        )
        return Response({'message':'Reset Link Send Successfully'}, status=status.HTTP_200_OK)


class ChangeForgotPassword(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        if data['password'] != data['confirm_password']:
            raise Exception.ApiException('Password Does not match')

        reset_token = ResetPasswordToken.objects.filter(token= data['token']).first()

        if not reset_token:
            raise Exception.ApiException('Invalid Link')

        user = User.objects.filter(email=reset_token.email).first()
        if not user:
            raise Exception.ApiException('User Not Found')

        user.set_password(data['password'])
        user.save()
        reset_token.delete()
        return Response({'message:Password Successfully Reset'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatePassword(request):
    user = request.user
    data = request.data
    
    if data['password'] != data['confirm_password']:
        raise Exception.ApiException('Password Does Not Match')
        
    user.set_password(data['password'])
    user.save()
    return Response({'message':'Password Successfully Updated'}, status = status.HTTP_200_OK)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUserDetails(request):
    user = request.user
    data= request.data
    first_name = data['first_name']
    last_name = data['last_name']
    try:
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except:
       return Response(status=status.HTTP_400_BAD_REQUEST)

    


class ValidateCoupon(APIView):
    def post(self, request, *args, **kwargs):
        now = timezone.now()
        data = request.data
        coupon_code = data['coupon_code']

        # Check in backennd that coupon is exists

        try:
            coupon = Coupons.objects.get(code__iexact =coupon_code, valid_from__lte=now, valid_to__gte= now, is_active=True)
            if coupon.max_limit > 0 :
            # if not coupon:
            #     raise Exception.ApiException('Invalid Coupon Code')
                serializer = CouponsSerializer(coupon, many=False)
                return Response( serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message":"Invalid Coupon"}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllOrdersByUser(request):
    user = request.user
    order = user.order_set.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSingleOrderByUser(request, pk):
    user = request.user
    order = Order.objects.get(_id=pk)
    try:
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

    except:
        return Response({'message':'Sorry order not found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editOrder(request):
    user = request.user
    order_id = request.data['order_id']
    transactionId = request.data['transactionId']
    
    # Check if order id is exist with the associated user
    try:
        order = Order.objects.get(_id = order_id)
        order.transactionId = transactionId
        order.isPaid = True
        order.status = "order_confirmed"
        order.save()
        return Response({"message":"Order Successfully Updated"}, status=status.HTTP_200_OK)
    except:
        return Response({'message':'No Order Found'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upiOrder(request):
    user = request.user
    order_id = request.data['order_id']

    # Check if order id is exist with the associated user
    try:
        order = Order.objects.get(_id = order_id)
        order.status = "upi_unconfirmed"
        order.save()
        return Response({"message":"Order Successfully Updated"}, status=status.HTTP_200_OK)
    except:
        return Response({'message':'No Order Found'}, status = status.HTTP_400_BAD_REQUEST)


        

class CheckPincode(APIView):
    def get(self, request, pincode):
        queryset = PinCode.objects.filter(pincode=pincode)
        if queryset.exists():
            serializer = PinCodeSerializer(queryset.first())
            return Response(serializer.data)
        else:
            return Response({'servicibility': False, 'state':'unknown'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editOrderStatus(request):
    user = request.user
    order_id = request.data['order_id']
    new_status = request.data['new_status']
    
    # Check if order id is exist with the associated user
    try:
        order = Order.objects.get(_id = order_id)
        order.status = new_status
        if new_status == "dispatched":
            order.courierInfo = request.data['courier-info']
        order.save()
        return Response({"message":"Order Successfully Updated"}, status=status.HTTP_200_OK)
    except:
        return Response({'message':'No Order Found'}, status = status.HTTP_400_BAD_REQUEST)
