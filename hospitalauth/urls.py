from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.Home, name='Home'),
    path('signup/', views.CreateAccount, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('covid_data/', views.TrackCases, name='trackcases')

]
