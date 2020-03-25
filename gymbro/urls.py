from django.urls import path
from . import views

urlpatterns = [
    # This is the path and method to view the login and registration screen.
    path('', views.Reg_and_Login_index),
    path('home', views.dashboard),
    path('workout/<int:workout_id>', views.show_workout),
    path('exercise/<int:exercise_id>', views.show_exercise),
    path('myprofile', views.show_myprofile),
    path('create_user', views.create_user),
    path('login', views.login),
    path('day',views.day),
    path('exercise',views.exercise),
    path('logout',views.logout),

]