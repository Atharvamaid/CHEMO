from django.shortcuts import render, redirect, HttpResponse
import pyrebase, requests
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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


dats = {
                        'inpatients' : {
                            'confirmed' : 0,
                            'under_observation' : 0,
                            'total' : 0
                        },
                        'Beds' : {
                            'available' : 0,
                            'occupied' : 0,
                            'total' : 0
                        },
                        'staff' : {
                            'oncall' : 0,
                            'onshift' : 0,
                            'total' : 0
                        },
                        'ventilators' : {
                            'available' : 0,
                            'in_use' : 0,
                            'total' : 0
                        },
                        'surgical_masks' : {
                            'available' : 0,
                            'in_use' : 0,
                            'total' : 0
                        },
                        'gloves' : {
                            'small' : 0,
                            'large' : 0,
                            'total' : 0
                        },
                        'face_shield' : {
                            'available' : 0,
                            'in_use' : 0,
                            'total' : 0
                        },
                        'isolation_gowns' : {
                            'small' : 0,
                            'large' : 0,
                            'total' : 0
                        },
                        'respirators' : {
                            'N95' : 0,
                            'PAPR' : 0,
                            'total' : 0
                        }



                        }

def Home(request):
    return render(request, 'hospitalauth/index.html')

def log_in(request):
    if request.user.is_authenticated:
        return redirect('Home')
    else:
        if request.method == 'POST':
            try:
                username = User.objects.get(email=request.POST['email']).username
                password = request.POST['pass']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'Invalid email or password ! Try again')
            except User.DoesNotExist:
                user = None
                messages.warning(request, 'Invalid email or password ! Try again')
        return render(request, 'hospitalauth/login.html')
@login_required(login_url='login')
def TrackCases(request):
    cases = requests.get('https://api.covid19india.org/state_district_wise.json')
    cases=cases.json()
    cases = cases['Maharashtra']['districtData']
    return render(request, 'hospitalauth/trackcases.html', {'cases' : cases})

@login_required(login_url='login')
def dashboard(request):
    db = firebase.database()

    name = db.child('Hospitals').child(request.user.id).child('Hospital_Name').get()
    address = db.child("Hospitals").child(request.user.id).child("Address").get()
    supplies = db.child("Hospitals").child(request.user.id).child("supplies").get()
    return render(request, 'hospitalauth/dashboard.html', { 'name' : name,"address" : address,  "supplies" : supplies})

def Search(request):
    if request.method=='POST':
        db=firebase.database()
        search  = request.POST['q']
        try:
            hospital_id = User.objects.get(first_name=search).id
            hospital = db.child("Hospitals").child(hospital_id).get()
        except User.DoesNotExist:
            messages.error(request, 'results not found')
    return render(request, 'hospitalauth/search.html', {"hospital": hospital})


def CreateAccount(request):
    if request.method=='POST':
        name = request.POST['hosname']
        username = generate_username(1)
        email = request.POST['email']
        address = request.POST['address']
        try :
            useremail = User.objects.get(email=email)
            messages.warning(request, 'This email is already registered !')
        except User.DoesNotExist:
            password = request.POST['pass']
            user = User.objects.create_user(username=username[0], email=email, password=password, first_name=name)
            if user:
                messages.success(request, f'Account Created for {name}')
                data = dats
                db = firebase.database()
                db.child('Hospitals').child(user.id).set({"Hospital_Name" : name, "Address" : address})
                db.child("Hospitals").child(user.id).child("supplies").set(data)
                login(request, user)
                return redirect('dashboard')
            else:
                messages.warning(request, 'Account not created try again')

    return render(request, 'hospitalauth/signup.html')

def update_data(request):

    try:
        fin = dats

        db = firebase.database()

        for i, j in fin.items():
            for k in j.keys():
                j[k] = request.POST[i + k]
        db.child("Hospitals").child(request.user.id).child("supplies").update(fin)
    except :
        print("error")
    return HttpResponse("fomr submitted")

def log_out(request):
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect('Home')