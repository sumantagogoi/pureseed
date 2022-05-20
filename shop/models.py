from ast import mod
from distutils.command.upload import upload
from random import choices
from sre_constants import CATEGORY
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = (
    ('1', 'Order Accepted'),
    ('2', 'Cooking'),
    ('3', 'Out For Delivery'),
    ('4', 'Delivered')
)

CATEGORY = (
    ('1', 'Smoked Meats'),
    ('2', 'Unmixed Natural Rice'),
    ('3', 'Condiments'),
    ('4', 'Ready To Eat')
)
SIZE = (
    ('1', 'KG'),
    ('2', 'Grams')
)


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200,choices=CATEGORY, blank=True, null=True)
    price = models.IntegerField()
    size = models.CharField(max_length=20,choices=SIZE, blank=True, null=True)
    inStock = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True, upload_to='uploads/')
    create_at = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)


    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS, blank=True, null=True)
    isPaid = models.BooleanField(default=False)
    isDelivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
    _id = models.AutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return user.username

class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=400, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.order._id


    