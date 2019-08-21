from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from datetime import *
import bcrypt

# Create your views here.
def home(request):
    request.session['user_id'] = 'logged out'
    
    return render(request, 'login_registration_app/login_registration_home.html')

def success(request):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    context = {
        'show' : User.objects.get(id=request.session['user_id'])
    }

    return render(request, 'login_registration_app/success.html', context)

def create(request):
    if request.method == 'POST':
        request.session['login_message'] = 'none'
        request.session['registration_message'] = 'inline-block'
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        request.session['register_login'] = request.POST['register_login']

        errors = User.objects.basic_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')

        else:
            new_entry = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                birthday=request.POST['birthday'],
                password=pw_hash)

            new_entry.save()
            request.session['user_id'] = new_entry.id

            return redirect("/success")

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    errors = User.objects.basic_validator(request.POST)
    request.session['registration_message'] = 'none'
    request.session['login_message'] = 'inline-block'

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')

    if len(user) > 0:
        logged_user = user[0] 

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/success')

    return redirect("/")
    
def logout(request):
    request.session['user_id'] = 'logged out'

    return redirect("/")