from django import forms
from .models import PinCode
from django.core.validators import RegexValidator

class PinCodeForm(forms.ModelForm):
    pincode = forms.CharField(max_length=6, widget=forms.TextInput(attrs={
        'pattern': '[0-9]{6}',
    }))
    class Meta:
        model = PinCode
        fields = '__all__'