from django.contrib.auth import authenticate, login, logout,password_validation
from django.shortcuts import redirect, render
from django.http import HttpResponse, response,HttpResponseRedirect
from django.views.generic import View
from django.views import generic
from .models import *
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
import random,string

# Create your views here.
def index(request):
    return render(request,'home.html')

def user_login(request):
    form = UserForm(request.POST)
    template_name = 'home.html'
    context = {}
    context['form'] = form
    print(request.POST)
    if form.is_valid():
        #user = form.save(commit=False)    
        username = request.POST['username']
        password = request.POST['password']
        #user.set_password(password)
        #user.save()
        print(username)
        user = authenticate(request,password=password,username=username) 
        #logout(request)
        if user is not None:
             login(request,user)
             return render(request,'index.html',context)
        else:
             return HttpResponse("<h1> Invalid Credentials </h1>")
    return render(request,template_name,context)
    
def user_logout(request):
    print(request.POST)
    template_name = 'index.html'
    logout(request) 
    return redirect('index:index')
    #return render(request,template_name)

def user_reg(request):
    try:
        form = UserForm(request.POST)
        template_name = 'signup.html'
        context = {}
        context['form'] = form
        print(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            fn = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            if (password != confirm_password or User.objects.filter(email=email).exists() or User.objects.filter(password=password).exists() or User.objects.filter(first_name=fn).exists()):
                print(1)
                raise ValidationError(
                    "password and confirm_password does not match"
                )
            else:
                # user = form.save(commit=False)
                # user.set_password(password)
                # user.save()
                user = User.objects.create_user(username,email,confirm_password)
                if password_validation.validate_password(confirm_password,user) is not None:
                    print("123")
                    raise ValidationError("The password is too similar to the username. This password is too short. It must contain at least 8 characters.")
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.set_password(password)
                user.save()
                return redirect('index:index')
        else:
            form = UserForm()
            HttpResponse("Invalid <a href = 'register'> go back </a>")
            #messages.error(request,"Bad Registration <a href = 'register'> go back </a>")
    except ValidationError:
        print(Exception)
        return HttpResponse("<h1>Invalid Credentials, Maybe Redundancy or error in fields <a href = 'register'> go back </a></h1>")
    return render(request,template_name,context)

def user_reset(request):
    form = UserForm(request.POST)
    template_name = 'reset.html'
    context = {}
    context['form'] = form
    print(request.POST)
    x = ''.join(random.choices(string.ascii_letters + string.digits + '@',k=10))
    if form.is_valid():
        print("123")
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            print(user.first_name)
            user.set_password(x)
            user.save()
            send_mail('New Password Reset',f'Hi {user.first_name} Ur new password is {x}',from_email=None,recipient_list=[email])
            return HttpResponse("<h1> Done, check mail (if its in spam otherwise) n <a href='reset/login'> login </a></h1>")
        else:
            return HttpResponse('error')
    return render(request,template_name,context)
    




# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'home.html'

#     def get(self,request):
#         form = self.form_class(None)
#         return render(request,self.template_name,{'form' : form})

#     def post(self,request):
#         form = self.form_class(request.POST)

#         if form.is_valid():

#             #user = form.save(commit=False)
            
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             #user.set_password(password)
#             #user.save()

#             user = authenticate(username=username,password=password)

#             if user is not None:
#                 HttpResponse("Success")
#         return render(request,self.template_name,{'form':form})




