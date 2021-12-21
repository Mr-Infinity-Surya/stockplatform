from django.urls import path
from django.conf import urls
from . import views

app_name = 'prediction'
urlpatterns = [
    path('',views.index,name='index'),
]