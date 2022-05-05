# Generated by Django 4.0.4 on 2022-05-05 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('payment_method', models.CharField(blank=True, max_length=100, null=True)),
                ('taxPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('shippingPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('totalPrice', models.DecimalField(decimal_places=2, max_digits=7)),
                ('status', models.CharField(blank=True, choices=[('1', 'Order Accepted'), ('2', 'Cooking'), ('3', 'Out For Delivery'), ('4', 'Delivered')], max_length=50, null=True)),
                ('isPaid', models.BooleanField(default=False)),
                ('isDelivered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('address', models.CharField(blank=True, max_length=400, null=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('inStock', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('qty', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]