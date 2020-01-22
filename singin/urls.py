from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout_url'),
    path('create_regist/', views.PostUser.as_view(), name='create_regist'),
   #url(r'^logout/', 'loginsys.views.logout'),
]