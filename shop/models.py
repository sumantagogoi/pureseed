from ast import mod
from distutils.command.upload import upload
from random import choices
from sre_constants import CATEGORY
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = (
    ('order_accepted', 'Order Accepted'),
    ('cooking', 'Cooking'),
    ('outForDelivery', 'Out For Delivery'),
    ('delivered', 'Delivered')
)


SIZE = (
    ('kg', 'KG'),
    ('gm', 'Grams')
)


class Category(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='uploads/')
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.title

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField()
    size = models.CharField(max_length=20,choices=SIZE, blank=True, null=True)
    qty = models.CharField(max_length=100, blank=True, null=True)
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

    def __str__(self):
        return str(self._id)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete= models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
    _id = models.AutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order._id)

class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=400, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.order._id)


    