from django import forms
from .models import PinCode
from django.core.validators import RegexValidator

class PinCodeForm(forms.ModelForm):
    pincode = forms.CharField(
        max_length=6,
        validators=[RegexValidator(r'^\d{6}$', message='Pincode must be a 6-digit number')]
    )
    class Meta:
        model = PinCode
        fields = '__all__'