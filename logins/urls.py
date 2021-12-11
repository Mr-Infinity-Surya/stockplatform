from django.urls import path
from django.conf.urls.static import static
from django.conf import settings, urls
from . import views

urlpatterns = [
    #path('',views.index,name='index'),
    #urls.url('',views.UserFormView.as_view(),name='logins'),
    path('',views.user_login,name='logins'),
    path('logout',views.user_logout,name='logout'),
    path('register',views.user_reg,name='registration'),
    path('reset',views.user_reset,name='reset'),
    path('reset/login',views.user_login,name='resetlogin'),
]