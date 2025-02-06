from django import forms
from .models import Coupon

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Replace with your custom User model if applicable

# class CouponCreationForm(forms.ModelForm):
#     class Meta:
#         model = Coupon
#         fields = ['value']

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         import uuid
#         instance.code = uuid.uuid4().hex[:12].upper()
#         if commit:
#             instance.save()
#         return instance


from django import forms
from .models import Coupon

class CouponCreationForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['name', 'code', 'value']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter coupon name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique coupon code'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter coupon value'}),
        }


User = get_user_model()






class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set the `is_employee` field to True when saving the user
        user.is_employee = True
        if commit:
            user.save()
        return user