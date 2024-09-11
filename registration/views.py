from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import HttpResponse,redirect
# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from registration.models import Registration,Additem
from django.contrib.auth.models import User,auth
from django.contrib import messages
from wsrms import settings
import requests
from together import Together
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
                    from_email='Your email id',  # Use the email you set in settings.py
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
    name=request.session['name']
    email=request.session['email']
    client = Together(api_key="API KEY")
    Recent = Additem.objects.filter(email=email)[:5]
    recent_list = [
        {'type': item.type, 'quantity': item.quantity}
        for item in Recent
    ]

    recent = ""
    for item in recent_list:
        recent += f"Type: {item['type']}, Quantity: {item['quantity']}\n"
    
    
    stream = client.chat.completions.create(
              model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
              messages=[{"role": "user", "content": "This is my waste till now"+ recent +"Suggest me in fun way where this waste can use after recycle"}],
              stream=True,
        )
        # response = client.chat.completions.create(
        #     model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        #     messages=[],
        #     max_tokens=512,
        #     temperature=0.7,
        #     top_p=0.7,
        #     top_k=50,
        #     repetition_penalty=1,
        #     stop=["<|eot_id|>","<|eom_id|>"],
        #     stream=True
        # )
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            print(content, end='', flush=True)

# Render the result in the templat
    # request.session['result']=full_response
            
    recent_activities = Additem.objects.filter(email=email)[:5]
    context={
        'name':name,
        'result':full_response,
        'recent_activities':recent_activities
    }
    return render (request,'UserDashboard.html',context=context)


def CompanyHomePage(request):
    name=request.session['name']
    email=request.session['email']

    
    context={
        'name':name
    }
    return render(request,'CompanyDashboard.html',context=context)

def AddWaste(request):
    if request.method=="POST":
        email=request.session['email']
        type=request.POST['waste_name']
        quantity=request.POST['quantity']
        measure=request.POST['unit']

        new_item = Additem(email=email,type=type,quantity=quantity,measure=measure)

        new_item.save()

        message=messages.success(request,"Added item Successsfully!!")

        return redirect("/home")

    return HttpResponse("No")



        




