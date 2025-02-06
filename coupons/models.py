from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid
from django.conf import settings

class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

# class Coupon(models.Model):
#     code = models.CharField(max_length=20, unique=True)
#     value = models.DecimalField(max_digits=10, decimal_places=2)
#     allocated_to = models.ForeignKey(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE, 
#         related_name='allocated_coupons'
#     )
#     redeemed = models.BooleanField(default=False)
#     redeemed_at = models.DateTimeField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def redeem(self):
#         if not self.redeemed:
#             self.redeemed = True
#             self.redeemed_at = now()
#             self.save()

class Coupon(models.Model):
    code = models.CharField(max_length=12, unique=True, editable=True)
    name = models.CharField(max_length=100, default="Default Coupon")
    value = models.DecimalField(max_digits=10, decimal_places=2)
    redeemed = models.BooleanField(default=False)
    
    redeemed_at = models.DateTimeField(null=True, blank=True)
    allocated_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='allocated_coupons')  # Correct related_name
    created_at = models.DateTimeField(auto_now_add=True)
    is_availed = models.BooleanField(default=False)  # Track if availed

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_coupon_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_coupon_code():
        """Generates a unique coupon code."""
        return str(uuid.uuid4())[:12].replace('-', '').upper()

    def __str__(self):
        return f"{self.name} ({self.code})"


class CouponQuota(models.Model):
    monthly_quota = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"Monthly Quota: {self.monthly_quota}"
    

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    spent = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    def deposit(self, amount):
        """Adds money to the wallet."""
        self.balance += amount
        self.save()

    def spend(self, amount):
        """Deducts money if sufficient balance exists."""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False  # Insufficient balance

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"