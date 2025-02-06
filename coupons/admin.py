from django.contrib import admin
from .models import User, Coupon
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import CouponQuota

from .models import Wallet

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'value', 'allocated_to', 'redeemed', 'created_at')
    list_filter = ('redeemed', 'allocated_to')
    search_fields = ('code',)






@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_employee', 'is_admin','is_vendor')
    list_filter = ('is_employee', 'is_admin','is_vendor')
    search_fields = ('username', 'email')

@user_passes_test(lambda u: u.is_admin)
def admin_dashboard(request):
    employees = User.objects.filter(is_employee=True)
    coupons = Coupon.objects.all()
    return render(request, 'admin_dashboard.html', {'employees': employees, 'coupons': coupons})

@admin.register(CouponQuota)
class CouponQuotaAdmin(admin.ModelAdmin):
    list_display = ['id', 'monthly_quota']  # Add 'id' as the first column
    list_display_links = ['id']  # Make 'id' clickable
    list_editable = ['monthly_quota']  # Now this will work






from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html
from .models import Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")
    search_fields = ("user__username",)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('deposit-money/<int:wallet_id>/', self.deposit_money, name='deposit_money'),
        ]
        return custom_urls + urls

    def deposit_money(self, request, wallet_id):
        wallet = get_object_or_404(Wallet, id=wallet_id)
        amount = request.GET.get("amount")

        if amount:
            try:
                amount = float(amount)
                wallet.deposit(amount)  # Assuming `deposit()` method exists in Wallet model
                self.message_user(request, f"Successfully added ₹{amount} to {wallet.user.username}'s wallet.")
            except ValueError:
                self.message_user(request, "Invalid amount entered.", level="error")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))