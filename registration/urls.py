from django.contrib import admin
from django.urls import path,include
from registration import views

urlpatterns = [
    path("",views.index,name="index"),
    path("login/",views.Register,name="registration"),
    path("login/process/", views.process_login, name='process'),
    path("home/", views.home, name='home'),
    path("user/home",views.UserHomePage,name="userhomepage"),
    path("company/home",views.CompanyHomePage,name="CompanyHomePage"),
    path("user/AddWaste/",views.AddWaste,name="userhomepage"),

]