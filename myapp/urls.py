from django.urls import path
from . import views

urlpatterns = [
     path('',views.signin, name = "signin"),
     path('administrador/', views.administrador, name="administrador"),
     path('mesero/', views.mesero, name = "mesero"),
     path('chef/', views.chef, name = "chef"),
     path('signout/', views.signout, name='signout'),
     path('createUser/', views.createUser, name='createUser'),
     path("showUsers/",views.showUsers, name ="showUsers"),
     path("deleteUser/<int:user_id>",views.deleteUser, name ="deleteUser")

]