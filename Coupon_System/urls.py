from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from coupons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('coupons/', include('coupons.urls')),  # Include the URLs from the coupons app
    #path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.custom_login, name='login'),

    
]
