from django.urls import include, path
from accounts import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('otp/',   views.admin_otp_verify, name='admin_otp_verify'),
]
