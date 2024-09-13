from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import HttpResponse,redirect
# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from registration.models import Registration,Additem,OrderDetail
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

        if Registration.objects.filter(email=email,work=user_type).exists():
            # Email already exists, do not save and return an error or simply return nothing
            
            return render(request, 'login.html', {'error': 'Email already exists'})
        else:
            # Email does not exist, save the new record
            new_registration = Registration(name=name,email=email,password=password,address=address,work=user_type,points=0)
            
            new_registration.save()
            send_mail(
                    subject='Login Successful',
                    message=f'Login Successful as '+ user_type,
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
        user_type=request.POST['user_type']

        try:
            user = Registration.objects.get(email=check_email,work=user_type)
            if user.password == check_password:
                request.session.set_expiry(60*15) 
                request.session['name'] = user.name
                request.session['email']=user.email
                request.session['user_type']=user.work
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
    user_type=request.session['user_type']
    user = Registration.objects.get(email=email,work=user_type)

    if user.work=="user":
        return redirect("/user/home")


    return redirect ("/company/home")

def UserHomePage(request):
    name=request.session['name']
    email=request.session['email']
    client = Together(api_key="69a37fbbd710ff4edd5c97b09b5514093dadbddccef5348c1fc764b7f666a2cb")
    Recent = Additem.objects.filter(email=email)[:5]
    recent_list = [
        {'type': item.type, 'quantity': item.quantity}
        for item in Recent
    ]
    coins=Registration.objects.get(email=email , work="user")

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
            # print(content, end='', flush=True)

# Render the result in the templat
    # request.session['result']=full_response
            
    recent_activities = Additem.objects.filter(email=email)[:5]
    context={
        'name':name,
        'result':full_response,
        'recent_activities':recent_activities,
        'coins':coins.points
    }
    return render (request,'UserDashboard.html',context=context)


def CompanyHomePage(request):
    name=request.session['name']
    email=request.session['email']

    activities = Additem.objects.all()

    activity_list = [
        {'type': item.type, 'quantity': item.quantity,'email':item.email,'measure':item.measure,'id':item.waste_id}
        for item in activities
    ]
    context={
        'name':name,
        'waste_reports':activity_list
        
    }


    return render(request,'CompanyDashboard.html',context=context)

def AddWaste(request):
    if request.method=="POST":
        email=request.session['email']
        type=request.POST['waste_name']
        quantity=request.POST['quantity']
        measure=request.POST['unit']

        waste_id=random.randint(9999,99999)

        new_item = Additem(email=email,type=type,quantity=quantity,measure=measure,waste_id=waste_id)

        new_item.save()

        message=messages.success(request,"Added item Successsfully!!")

        return redirect("/home")

    return HttpResponse("No")



def collect_waste(request,waste_id):
    if request.method == "POST":
        # waste_id = request.POST.get('waste_id')
        company_name=request.session['name']
        company_email=request.session['email']
        user=Additem.objects.get(waste_id=waste_id)
        
        user_email=user.email

        send_mail(
                    subject='Will get your Waste to Recycle',
                    message=f'Your request is accepted by '+company_name+'and will get in touch with you to collect waste',
                    from_email='agrawalharsh0522@gmail.com',  # Use the email you set in settings.py
                    recipient_list=[user_email],
                    fail_silently=False,
            )
        
        neworder=OrderDetail(company_email=company_email,user_email=user.email,type=user.type,quantity=user.quantity,measure=user.measure,waste_id=user.waste_id)
        neworder.save()
        user.delete()

        return HttpResponse("You can collect  waste ID"+str(waste_id))
    return HttpResponse("You are handling nothing")

def order_handle(request):
    company_name=request.session['name']
    company_email=request.session['email']
    if request.method=="POST":

        order=OrderDetail.objects.filter(company_email=company_email)

        order_list = [
            {'type': item.type, 'quantity': item.quantity,'user_email':item.user_email,'measure':item.measure,'id':item.waste_id,'company_email':item.company_email}
            for item in order
        ]

        context={
            'order_list':order_list,
            'name':company_name
        }


        return render(request,'order_handle.html',context)

def order_done(request,waste_id):
    if request.method=="POST":

        user= OrderDetail.objects.get(waste_id=waste_id)

        userdata=Registration.objects.get(email=user.user_email,work="user")

        # userdata[0].points=userdata[0].points+(user[0].quantity)*2

        # userdata[0].save()
        # print (type(userdata.points))
        userdata.points=userdata.points+int(5)
        # print(userdata.points)
        userdata.save()
        user.delete()

        send_mail(
                    subject='Congratulations,You won coins!!',
                    message=f'We got your waste items in segregated manner , And you some coins .Here\'s your total '+str(userdata.points)+'.',
                    from_email='agrawalharsh0522@gmail.com',  # Use the email you set in settings.py
                    recipient_list=[userdata.email],
                    fail_silently=False,
        )

        


        return HttpResponse("Done")
        

    
    



