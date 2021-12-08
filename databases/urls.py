from django.urls import path
from django.conf import urls
from . import views

urlpatterns = [
    urls.url('',views.index,name='index'),
]