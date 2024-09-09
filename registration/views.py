from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import HttpResponse,redirect
# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from registration.models import Registration
from django.contrib.auth.models import User,auth
from django.contrib import messages
from wsrms import settings
import requests

from django.conf import settings
import json
import random
import os
# from together import Together
# Create your views here.

def index(request):
    return render(request,'registration.html')

def Register(request):


    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        address=request.POST['address']
        user_type=request.POST['user_type']

        if Registration.objects.filter(email=email).exists():
            # Email already exists, do not save and return an error or simply return nothing
            
            return render(request, 'login.html', {'error': 'Email already exists'})
        else:
            # Email does not exist, save the new record
            new_registration = Registration(name=name,email=email,password=password,address=address,work=user_type)
            
            new_registration.save()
            send_mail(
                    subject='Login Successful',
                    message=f'Login Successful',
                    from_email='agrawalharsh0522@gmail.com',  # Use the email you set in settings.py
                    recipient_list=[email],
                    fail_silently=False,
            )
            return render(request,'login.html' ,{'success': 'Registered successfully!!'})
            
    return render(request,'login.html')


def process_login(request):
    if request.method=="POST":
        check_email=request.POST['email']
        check_password=request.POST['password']

        try:
            user = Registration.objects.get(email=check_email)
            if user.password == check_password:
               
                request.session['name'] = user.name
                request.session['email']=user.email
                return redirect("/home")
            else:
                messages.error(request, 'Incorrect Password!!')
                return redirect('/Register')
                # return render(request,'login.html',{'error':'INcorrect Password!!'})


        # Problem faced in this code urls not matching  ---- DONE
        except Registration.DoesNotExist:
            messages.error(request, 'Email not exist, PLease Create an account first!!')
            # return redirect('/')
            # return messages.error(request,'Email not exist')
    
    return render(request,'login.html')

def home(request):
    email=request.session['email']
    user = Registration.objects.get(email=email)

    if user.work=="user":
        return redirect("/user/home")


    return redirect ("/company/home")

def UserHomePage(request):
    return HttpResponse("User Home Page")


def CompanyHomePage(request):
    return HttpResponse("Company Home Page")




