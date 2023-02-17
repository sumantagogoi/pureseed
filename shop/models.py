from ast import mod
from distutils.command.upload import upload
from random import choices
from sre_constants import CATEGORY
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Create your models here.

STATUS = (
    ('upi_unconfirmed', 'UPI Unconfirmed'),
    ('order_confirmed', 'Order Confirmed'),
    ('processing', 'Processing'),
    ('dispatched', 'Dispatched'),
    ('delivered', 'Delivered'), 
    ('returned', 'Returned'), 
    ('cancelled', 'Cancelled'), 
    ('refunded', 'Refunded'), 
)


SIZE = (
    ('kg', 'KG'),
    ('gram', 'Grams')
)

DISCOUNT_TYPE = (
    ('flat', 'flat'),
    ('percent', 'percent')
)


class Category(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='uploads/')
    _id = models.AutoField(primary_key=True, editable=False)
    status = models.BooleanField(default=False, blank=True, null=True)

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
    _id = models.AutoField(primary_key=True, editable=False)
    custom_order_id = models.CharField(max_length=255, default='WEB-00001', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, default = 0)
    coupon = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, blank=True, null=True)
    isPaid = models.BooleanField(default=False)
    isDelivered = models.BooleanField(default=False)
    transactionId = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return str(self._id)

    class Meta:
        ordering = ['-created_at']
   
    def save(self, *args, **kwargs):
        print('Saving Order')
        last_order = Order.objects.all().order_by('_id').last()
        if last_order:
            last_custom_id = int(last_order.custom_order_id.split('-')[-1])
        else:
            last_custom_id = 0
        self.custom_order_id = 'WEB-{:05}'.format(last_custom_id + 1)
        print(f'custom_id: {self.custom_order_id}')
        super().save(*args, **kwargs)



class OrderItem(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete= models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    qty = models.IntegerField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=7, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    image = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return str(self.order._id)
        
    class Meta:
        ordering = ['-created_at']

    

class ShippingAddress(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=400, blank=True, null=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.order._id)

class Coupons(models.Model):
    code = models.CharField(max_length=20)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    max_limit = models.IntegerField(default=1)

    def __str__(self):
        return self.code
