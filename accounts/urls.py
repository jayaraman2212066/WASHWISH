from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login/', views.login, name="login"),
    path('accounts/register/', views.register, name="register"),
    path('accounts/logout/', views.logout, name="logout"),
    path('login/', views.login, name="login_alt"),
    path('register/', views.register, name="register_alt"),
    path('logout/', views.logout, name="logout_alt"),
]
