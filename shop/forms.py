from django import forms
from .models import PinCode

class PinCodeForm(forms.ModelForm):
    class Meta:
        model = PinCode
        fields = '__all__'