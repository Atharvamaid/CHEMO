from django.shortcuts import render, redirect
import pyrebase
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout, login
from random_username.generate import generate_username
# Create your views here.
from .forms import Register
config = {
  'apiKey': "AIzaSyAkDP2AhobRcAhWelrptCPc8ftXzDLSww0",
  'authDomain': "chemo-8da83.firebaseapp.com",
  'databaseURL': "https://chemo-8da83.firebaseio.com",
  'projectId': "chemo-8da83",
  'storageBucket': "chemo-8da83.appspot.com",
  'messagingSenderId': "699405303797",
  'appId': "1:699405303797:web:729d397cf843942fe22abc",
  'measurementId': "G-9R3DK327S3"
}
firebase = pyrebase.initialize_app(config)

def Home(request):
    return render(request, 'hospitalauth/index.html')

def log_in(request):
    if  request.method == 'POST':
        username = User.objects.get(email = request.POST['email']).username
        password = request.POST['pass']
        user = authenticate(request, username=username,password=password)
        if user:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'hospitalauth/login.html')

def dashboard(request):
    db = firebase.database()
    hospitals = db.child('Hospitals').child(request.user.id).get().each()
    return render(request, 'hospitalauth/dashboard.html', {'hospitals' : hospitals})

def CreateAccount(request):
    if request.method=='POST':
        name = request.POST['hosname']
        username = generate_username(1)
        email = request.POST['email']
        password = request.POST['pass']
        user = User.objects.create_user(username=username[0], email=email, password=password)
        messages.success(request, f'Account Created for {name}')
        dats = {'hospitalName' : name}
        db = firebase.database()
        db.child('Hospitals').child(user.id).set(dats)
        return redirect('login')

    else:
        form = Register()
    return render(request, 'hospitalauth/signup.html', {'form' : form})

def log_out(request):
    logout(request)
    return redirect('Home')