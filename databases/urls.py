from django.urls import path
from django.conf import urls
from . import views

app_name = 'databases'
urlpatterns = [
    path('',views.index,name='index'),
    path('stocks',views.stock_manage,name='stocks')
]