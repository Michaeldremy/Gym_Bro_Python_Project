from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

# Renders

def Reg_and_Login_index(request):
    # if 'user_id' not in request.session:
    #     return redirect('/')
    return render(request, 'LogReg.html')

def dashboard(request):
    context = {
        "all_workouts": Workout.objects.all()
    }
    return render(request,'dashboard.html',context) 

def show_workout(request,workout_id):
    return render(request,'workout.html')  

def show_exercise(request,exercise_id):
    return render(request,'exercise.html')

def show_myprofile(request):
    return render(request,'Profile.html')    