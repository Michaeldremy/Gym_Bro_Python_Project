from django.urls import path
from . import views

urlpatterns = [
    # This is the path and method to view the login and registration screen.
    path('', views.Reg_and_Login_index),
]