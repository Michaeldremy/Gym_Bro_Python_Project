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
    return render(request,'dashboard.html') 

def show_workout(request,workout_id):
    return render(request,'workout.html')  

def show_exercise(request,exercise_id):
    return render(request,'exercise.html')

def show_myprofile(request):
    return render(request,'myprofile.html')    


#POST
def create_user(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        fname = request.POST['form_first_name']
        lname = request.POST['form_last_name']
        email = request.POST['form_email']
        weight = request.POST['form_weight']
        rawPassword = request.POST['form_password']
        hashPass = bcrypt.hashpw(rawPassword.encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(first_name=fname, last_name=lname, email=email, weight=weight, password=hashPass)
        request.session['user_id'] = newUser.id
        return redirect("/home")

def login(request):
    pass