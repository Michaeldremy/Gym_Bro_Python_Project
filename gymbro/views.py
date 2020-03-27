from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from .models import *
from chartit import DataPool, Chart, PivotDataPool, PivotChart
from datetime import date
import calendar

# Renders

def Reg_and_Login_index(request):
    return render(request, 'LogReg.html')

def dashboard(request):
    today = date.today()
    today_wkout = Workout.objects.get(weekday=today.strftime("%A"))
    context = {
        "all_workouts": Workout.objects.all(),
        "today_wkout_id": today_wkout.id,

    }
    return render(request,'dashboard.html',context) 

def show_exercise(request,workout_id, exercise_id):
    this_workout = Workout.objects.get(id=workout_id)
    this_exercise = Exercise.objects.get(id=exercise_id)
    exercise_sets = Set.objects.filter(exercise=this_exercise)
    context = {
        "this_workout": this_workout,
        "this_exercise": this_exercise,
        "exercise_sets": exercise_sets
    }
    request.session['restt']=this_exercise.rest
    return render(request,'exercise.html',context)

def show_the_team(request):
    today = date.today()
    today_wkout = Workout.objects.get(weekday=today.strftime("%A"))
    context = {
        "today_wkout_id": today_wkout.id
    }
    return render(request,'our_team.html', context)

def show_data_visualization(request,link_id):
    this_user= User.objects.get(id=request.session['user_id'])
    my_stats = Stat.objects.filter(user=this_user)
    print("I am here",link_id)     
    if link_id != None:
        plotdata = \
        DataPool(
        series=
            [{'options': {
                'source': Stat.objects.filter(user=request.session['user_id'],exercise=Exercise.objects.get(id = link_id)).order_by("date")},
                'terms': ['date','lbs_rep']}
            ])
        #Step 2: Create the Chart object
        excercisename = Exercise.objects.get(id = link_id).name
        cht = Chart(
                datasource = plotdata,
                series_options =
                [{'options':{
                    'type': 'line',
                    'stacking': False},
                    'terms':{'date': ['lbs_rep']}}],
                chart_options =
                {'title': {
                    'text': excercisename},
                'xAxis': {
                        'title':{
                        'text': 'Date'}},
                'YAxis': {
                        'title': {
                        'text': 'Avg'}}
                })
        context = {
            'profile_info': User.objects.get(id=request.session['user_id']),
            'chart_list': [cht],
            'allexercises': Exercise.objects.all(),
            'mystats': my_stats 
        }
        return render(request,'myprofile.html', context) 
    else:
        context = {
            'profile_info': User.objects.get(id=request.session['user_id']), 
            'allexercises': Exercise.objects.all(),
            'mystats': my_stats 
    
        }
        return render(request,'myprofile.html', context)  



def show_myprofile(request):
    today = date.today()
    today_wkout = Workout.objects.get(weekday=today.strftime("%A"))
    this_user= User.objects.get(id=request.session['user_id'])
    my_stats = Stat.objects.filter(user=this_user)

    context = {
        'profile_info': User.objects.get(id=request.session['user_id']),
        'allexercises': Exercise.objects.all(), 
        "today_wkout_id": today_wkout.id,
        'mystats': my_stats 
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

def show_workout(request,workout_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_workout=Workout.objects.get(id=workout_id)
    user_stats = Stat.objects.filter(user=this_user).filter(date=date.today())
    one_exercise = Exercise.objects.filter(id=1)
    all_exercises = Exercise.objects.filter(workout=this_workout)
    for stat in user_stats:
        all_exercises = all_exercises.exclude(id=stat.exercise.id)
    context={
        'workout': this_workout,
        'user_stats': user_stats,
        'exercises': all_exercises,
        'exercise': one_exercise
    }
    if this_workout.category == "WeightTrain":
        return render(request,'weight_train.html',context)
    else:
        return render(request,'cardio.html',context)

def exercise(request):
    return render(request,'exercise.html')


#POST
def create_user(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
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
        user_login = User.objects.filter(email=request.POST['form_email']) 
        # print(f"user login={user_login}")
        if user_login: 
            logged_user = user_login[0] 
            # print(f"logged_user={logged_user}")
            # print(bcrypt.checkpw(request.POST['form_password'].encode(), logged_user.password.encode()))
            if bcrypt.checkpw(request.POST['form_password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                # print("login succesful")
                return redirect('/home')
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            # print("error in login method is running")
            return redirect('/')


# Post Requests for Workout
def begin_workout(request):
    this_user = User.objects.get(id=request.session['user_id'])
    this_workout = Workout.objects.get(id=request.POST['workout_id'])
    this_workout.users.add(this_user)
    this_workout.save()
    return redirect(f'/workout/{this_workout.id}')

def add_sets_data(request,workout_id,exercise_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_workout = Workout.objects.get(id=workout_id)
    this_exercise = Exercise.objects.get(id=exercise_id)
    exercise_sets = Set.objects.filter(exercise=this_exercise)
    sum_weight = 0
    sum_reps = 0
    errors = ""
    for i in exercise_sets:
        post_weight = request.POST[f'{i.id}_weight']
        post_reps = request.POST[f'{i.id}_reps']
        request.session[f'{i.id}_weight'] = post_weight
        request.session[f'{i.id}_reps'] = post_reps
        if post_weight == "" or post_reps == "":
            i.weight = 0
            i.reps = 0
            errors = "FINISH YOUR REPS LOSER"
        else:
            i.weight = post_weight
            i.reps = post_reps
        i.save()
        sum_weight += int(i.weight)*int(i.reps)
        sum_reps += int(i.reps)
    if len(errors)>0:
        messages.error(request, errors)
        return redirect(f'/exercise/{this_workout.id}/{this_exercise.id}')
    try:    
        compute_avg = sum_weight/sum_reps
    except:
        compute_avg = 0    
    newStat = Stat.objects.create(user=this_user,exercise=this_exercise,lbs_rep=compute_avg)    
    return redirect(f'/workout/{this_workout.id}')
    
def logout(request):
    request.session.flush()
    return redirect('/')

def cardio(request,workout_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_workout=Workout.objects.get(id=workout_id)
    user_stats = Stat.objects.filter(user=this_user).filter(date=date.today())
    all_exercises = Exercise.objects.filter(workout=this_workout)
   

    for stat in user_stats:
        all_exercises = all_exercises.exclude(id=stat.exercise.id)

    context={
        'workout': this_workout,
        'user_stats': user_stats,
        'exercises': all_exercises,
        
    }
    return render(request,'cardio.html',context)