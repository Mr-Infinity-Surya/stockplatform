from django.urls import path
from django.conf import urls
from . import views

app_name = 'databases'
urlpatterns = [
    path('',views.index,name='index'),
    path('stocks',views.stock_manage,name='stocks'),
    path('userstock',views.user_stock,name='userstock'),
    path('filldb',views.fill_db,name='filldb'),
    path('filldb2',views.fill_db2,name='filldb2'),
    path('redisdata',views.redis_data,name='redisdata'),
]