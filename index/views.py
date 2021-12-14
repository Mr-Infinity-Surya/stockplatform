from django.shortcuts import render
from databases.models import *
from django import forms

# Create your views here.
def index(request):
    context = {}
    check_user = Investor.objects.filter(Username=request.user.username).exists()
    context['check_investor'] = check_user
    return render(request,'index.html',context)