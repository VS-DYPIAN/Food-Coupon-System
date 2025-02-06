from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import CouponCreationForm
from django.utils.timezone import now
from .models import Coupon
from .models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Coupon, CouponQuota
import pytz
import uuid
from .models import Wallet
import json
from decimal import Decimal

User = get_user_model()

########################################################################################################################





@user_passes_test(lambda u: u.is_admin)
def create_coupon(request):
    if request.method == 'POST':
        form = CouponCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CouponCreationForm()
    return render(request, 'create_coupon.html', {'form': form})



from django.contrib.auth.decorators import login_required

@user_passes_test(lambda u: u.is_admin)
def admin_dashboard(request):
    if not request.user.is_admin:
        return render(request, '403.html')  # Custom template for unauthorized access
    employees = User.objects.filter(is_employee=True)
    coupons = Coupon.objects.all()
    return render(request, 'admin_dashboard.html', {'employees': employees, 'coupons': coupons})

@login_required


def employee_dashboard(request):
    if not request.user.is_employee:
        return render(request, '403.html')  # Unauthorized access
    
    # Fetch coupons
    coupons = request.user.allocated_coupons.all()  
    redeemed_coupons = coupons.filter(redeemed=True)
    available_coupons = coupons.filter(redeemed=False)
    
    # Ensure wallet exists or create a new one with a default balance
    wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'balance': 0.00})

    return render(request, 'employee_dashboard.html', {
        'redeemed_coupons': redeemed_coupons,
        'available_coupons': available_coupons,
        'wallet': wallet
    })


@login_required
def vendor_dashboard(request):
    if not request.user.is_vendor:
        return render(request, '403.html')  # Custom template for unauthorized access
    
    coupons = Coupon.objects.all()
    
    redeemed_coupons = coupons.filter(redeemed=True)
    available_coupons = coupons.filter(redeemed=False)
    employees = User.objects.filter(is_employee=True)

    wallet = Wallet.objects.all()
    
    
    return render(request, 'vendor_dashboard.html', {
        'employees': employees, 
        'coupons': coupons,
        'redeemed_coupons': redeemed_coupons,
        'available_coupons': available_coupons,
        'wallet': wallet
        })



def avail_monthly_coupons(request):
    if not request.user.is_employee:
        return render(request, '403.html')  # Unauthorized access

    # Convert time to IST and remove timezone info
    ist = pytz.timezone('Asia/Kolkata')  
    current_time = now().astimezone(ist).replace(tzinfo=None)

    # 🔹 Get the latest `CouponQuota` entry
    latest_quota = CouponQuota.objects.order_by('-id').first()

    if latest_quota:
        monthly_quota = latest_quota.monthly_quota  
        # 🔹 Delete all old `CouponQuota` entries except the latest one
        CouponQuota.objects.exclude(id=latest_quota.id).delete()
    else:
        # If no quota exists, create a new one with the default value (5)
        latest_quota = CouponQuota.objects.create(monthly_quota=5)
        monthly_quota = latest_quota.monthly_quota

    this_month = current_time.month  
    this_year = current_time.year  

    allocated_this_month = request.user.allocated_coupons.filter(
        created_at__month=this_month, created_at__year=this_year
    )

    if allocated_this_month.count() < monthly_quota:
        for _ in range(monthly_quota - allocated_this_month.count()):
            Coupon.objects.create(
                code=f'COUPON-{uuid.uuid4().hex[:8]}',  # Ensure uniqueness
                value=100,  
                allocated_to=request.user  
            )
        
        message = "Monthly coupons successfully allocated!"
    else:
        message = "You have already availed your monthly coupons."

    return render(request, 'avail_coupons.html', {'message': message})





# def avail_monthly_coupons(request):
#     if not request.user.is_employee:
#         return render(request, '403.html')  # Unauthorized access

#     # Get monthly quota from database (or set default to 5)
#     quota_obj, created = CouponQuota.objects.get_or_create(id=1)  
#     monthly_quota = quota_obj.monthly_quota  

#     this_month = now().month
#     this_year = now().year

#     allocated_this_month = request.user.allocated_coupons.filter(
#         created_at__month=this_month, created_at__year=this_year
#     )

#     if allocated_this_month.count() < monthly_quota:
#         for _ in range(monthly_quota - allocated_this_month.count()):
#             Coupon.objects.create(
#                 code=f'COUPON-{now().timestamp()}',
#                 value=100,  # Example value
#                 allocated_to=request.user  # Assign the current user
#             )
#         message = "Monthly coupons successfully allocated!"
#     else:
#         message = "You have already availed your monthly coupons."

#     return render(request, 'avail_coupons.html', {'message': message})












@login_required
def redeem_coupon(request, coupon_id):
    try:
        # Fetch the coupon using the ID
        coupon = Coupon.objects.get(id=coupon_id, redeemed=False)

        # Convert to IST and make it naive
        ist = pytz.timezone('Asia/Kolkata')
        current_time = now().astimezone(ist).replace(tzinfo=None)  # Remove timezone info
        
        coupon.redeemed = True
        coupon.redeemed_at = current_time  # Store naive datetime
        
        coupon.save()

        return JsonResponse({'message': 'Coupon redeemed successfully!'})
    except Coupon.DoesNotExist:
        return JsonResponse({'error': 'Coupon not found or already redeemed'}, status=400)







def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User {user.username} registered successfully!")  # Debug log
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            print(form.errors)  # Debug log for errors
            messages.error(request, 'There was an error with your registration. Please try again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # 🔹 Clear the old session to prevent overriding other users' sessions
            request.session.flush()  
            login(request, user)

            # Redirect based on user role
            if hasattr(user, 'is_admin') and user.is_admin:
                return redirect('admin_dashboard')
            elif hasattr(user, 'is_employee') and user.is_employee:
                return redirect('employee_dashboard')
            elif hasattr(user, 'is_vendor') and user.is_vendor:
                return redirect('vendor_dashboard')
        else:
            return render(request, "registration/login.html", {"form": form})
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})




def custom_logout(request):
    logout(request)
    return redirect('login')





@login_required
def spend_money(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = Decimal(data.get("amount", "0"))  # Convert amount to Decimal
            

            if amount <= 0:
                return JsonResponse({"error": "Invalid amount. Enter a positive number."}, status=400)

            # Get or create the user's wallet
            wallet, _ = Wallet.objects.get_or_create(user=request.user)
            wallet.spent = amount
            print(wallet.spent)

            if wallet.balance >= amount:
                wallet.balance -= amount  # Now both are Decimals
                wallet.save()
                return JsonResponse({"message": f"₹{amount} spent successfully! by {wallet.user}", "new_balance": str(wallet.balance) ,"spent_amount": str(wallet.spent), })
                #return JsonResponse({"message": f"₹{amount} spent successfully! by {wallet.user}", "new_balance": str(wallet.balance) ,"by": str(wallet.user)})
            else:
                return JsonResponse({"error": "Insufficient balance."}, status=400)

        except (json.JSONDecodeError, ValueError, TypeError):
            return JsonResponse({"error": "Invalid request format."}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed."}, status=405)