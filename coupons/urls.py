from django.urls import path
from django.contrib.auth import views as auth_views
from .views import redeem_coupon




from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('create-coupon/', views.create_coupon, name='create_coupon'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('vendor_dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('avail_coupons/', views.avail_monthly_coupons, name='avail_coupons'),
    
    
    #path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    #path('logout/', auth_views.LoginView.as_view(template_name='login.html'), name='logout'),
    
    
    path('redeem-coupon/<int:coupon_id>/', views.redeem_coupon, name='redeem_coupon'),
    # Other URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),

   
    path("wallet/spend-money/", views.spend_money, name="spend_money"),
    
    
    
]







