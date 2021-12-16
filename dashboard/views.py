from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    if (request.user.is_authenticated):
        return render(request,'index_dash.html')
    else:
        return HttpResponse('error',status=404)