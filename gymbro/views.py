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
    context = {
        "this_exercise": Exercise.objects.get(id=exercise_id)
    }
    return render(request,'exercise.html',context)

def show_myprofile(request):
    return render(request,'myprofile.html')    

def day(request):
    this_workout=Workout.objects.get(weekday='Sunday')
    context={
        'workouts':Workout.objects.get(weekday='Sunday'),
        'sets': Set.objects.all(),
        'exercises':Exercise.objects.filter(workout=this_workout)
    }
    return render(request,'day.html',context)

def exercise(request):
    return render(request,'exercise.html')


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
    if request.method=='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("error in login method is running")
            return redirect('/')
        user_login = User.objects.filter(email=request.POST['form_email']) 
        print(f"user login={user_login}")
        if user_login: 
            logged_user = user_login[0] 
            print(f"logged_user={logged_user}")
            print(bcrypt.checkpw(request.POST['form_password'].encode(), logged_user.password.encode()))
            if bcrypt.checkpw(request.POST['form_password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                print("login succesful")
                return redirect('/home')
            else:
                messages.error(request, "wrong password")
                return redirect('/')
    return redirect('/')


# Post Requests for Workout
def begin_workout(request):
    this_workout = Workout.objects.get(id=request.POST['workout_id'])
    this_workout.users.add(request.session['user_id'])
    this_workout.save()
    request.session['workout_id'] = this_workout.id
    return redirect(f'/exercise/{this_workout.id}')