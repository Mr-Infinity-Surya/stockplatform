from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse, response,HttpResponseRedirect
from django.views.generic import View
from django.views import generic
from .models import *
from .forms import UserForm
from django.contrib import messages
#from django.contrib.auth.models import User

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
             return HttpResponse("<h1> Success </h1>")
        else:
             return HttpResponse("<h1> Invalid Credentials </h1>")
    return render(request,template_name,context)
    
def user_logout(request):
    print(request.POST)
    template_name = 'home.html'
    logout(request)
    return render(request,template_name)

def user_reg(request):
    form = UserForm(request.POST)
    template_name = 'signup.html'
    context = {}
    context['form'] = form
    print(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']
        email = form.cleaned_data['email']
        if (password != confirm_password):
            raise form.ValidationError(
                "password and confirm_password does not match"
            )
        else:
            form.save()
            return HttpResponse("correct <a href = 'register'> go back </a>")
    else:
        form = UserForm()
        HttpResponse("Invalid <a href = 'register'> go back </a>")
        #messages.error(request,"Bad Registration <a href = 'register'> go back </a>")
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




