from django.urls import path
from django.conf import urls
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('',views.index,name='index'),
]