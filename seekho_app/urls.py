# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.REGISTER, name='register'),
    path('login/', views.DO_LOGIN, name='login'),
]
