from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from tasks.models import Task
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        print("User is authenticated")
        tasks=Task.objects.filter(user=request.user).order_by('-created_at')
        context = {
            'tasks': tasks
        }
        return render(request, 'home.html',context)
    else:
        return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        # confirm_password=password
        
        if password != confirm_password:
            messages.error(request, 'Password does not match')
            return render(request, 'register.html')
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'register.html')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password,first_name=fname,last_name=lname)
                user.save()
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                messages.success(request, f'You have successfully registered: {user.username}')
                return redirect('home')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        
        username=request.POST['username']
        password=request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, f'You have successfully logged-in: {user.username}')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            print("Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('home')

