from django.urls import path
from . import views

urlpatterns = [
     path('',views.signin, name = "signin"),
     path('administrador/', views.administrador, name="administrador"),
     path('mesero/', views.mesero, name = "mesero"),
     path('chef/', views.chef, name = "chef"),
     path('signout/', views.signout, name='signout')

]