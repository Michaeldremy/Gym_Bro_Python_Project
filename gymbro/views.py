from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from .models import *
from chartit import DataPool, Chart, PivotDataPool, PivotChart

# Renders

def Reg_and_Login_index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'LogReg.html')

def dashboard(request):
    context = {
        "all_workouts": Workout.objects.all()
    }
    return render(request,'dashboard.html',context) 

def show_workout(request,workout_id):
    return render(request,'workout.html')  

def show_exercise(request,workout_id, exercise_id):
    this_workout = Workout.objects.get(id=workout_id)
    this_exercise = Exercise.objects.get(id=exercise_id)
    context = {
        "this_workout": this_workout,
        "this_exercise": this_exercise,
        "exercise_sets": Set.objects.filter(exercise=this_exercise)
    }
    return render(request,'exercise.html',context)

def show_the_team(request):
    return render(request,'our_team.html')

def show_myprofile(request):
    context = {
        'profile_info': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'myprofile.html', context)    

def edit_profile(request):
    if request.method =='POST':
        errors = User.objects.edit_form_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/edit_profile')
        c = User.objects.get(id=request.session['user_id'])
        c.first_name = request.POST['form_first_name']
        c.last_name = request.POST['form_last_name']
        c.desc = request.POST['form_desc']
        c.save()
        return redirect('/myprofile')
    context = {
        'profile_info': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'edit_myprofile.html' , context)

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
        newUser = User.objects.create(first_name=fname, desc="none", last_name=lname, email=email, weight=weight, password=hashPass, profile_picture="default1.png")
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
    this_user = User.objects.get(id=request.session['user_id'])
    this_workout = Workout.objects.get(id=request.POST['workout_id'])
    this_workout.users.add(this_user)
    this_workout.save()
    return redirect(f'/exercise/{this_workout.id}') ## need to redirect to /workout/workout_id

def add_sets_data(request,workout_id,exercise_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_workout = Workout.objects.get(id=workout_id)
    this_exercise = Exercise.objects.get(id=exercise_id)
    exercise_sets = Set.objects.filter(exercise=this_exercise)
    sum_weight = 0
    sum_reps = 0
    for i in exercise_sets:
        i.weight = request.POST[f'{i.id}_weight']
        i.reps = request.POST[f'{i.id}_reps']
        i.save()
        sum_weight += int(i.weight)*int(i.reps)
        sum_reps += int(i.reps)
    compute_avg = sum_weight/sum_reps
    newStat = Stat.objects.create(user=this_user,exercise=this_exercise,lbs_rep=compute_avg)    
    return HttpResponse("Added") ## need to redirect to /workout/workout_id
def logout(request):
    request.session.flush()
    return redirect('/')
