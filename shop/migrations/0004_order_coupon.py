# Generated by Django 4.0.4 on 2022-06-13 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_shippingaddress_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
