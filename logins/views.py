from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse, response
from django.views.generic import View
from django.views import generic
from .models import *
from .forms import UserForm

# Create your views here.
def index(request):
    return render(request,'home.html')

def home_view(request):
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
        if user is not None:
            return HttpResponse("<h1> Success</h1>")
        else:
            return HttpResponse("<h1> Invalid Credentials </h1>")
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




