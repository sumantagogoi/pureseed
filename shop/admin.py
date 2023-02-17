from django.contrib import admin
from .models import Coupons, Product, Order, OrderItem, ShippingAddress, Category, Coupons, \
    PinCode
# Register your models here.


class CouponAdmin(admin.ModelAdmin):
    list_display =  ('code', 'valid_from', 'valid_to', 'discount' ,'is_active' )
    list_filter = ('is_active', 'valid_from', 'valid_to')
    search_fields = ('code',)



admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category)
admin.site.register(Coupons,CouponAdmin)
admin.site.register(PinCode)



