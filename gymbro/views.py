from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

# Renders

def Reg_and_Login_index(request):
    # if 'user_id' not in request.session:
    #     return redirect('/')
    return render(request, 'LogReg.html')