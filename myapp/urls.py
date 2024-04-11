from django.urls import path
from . import views

urlpatterns = [
     path('',views.signin, name = "signin"),
     path('administrador/', views.administrador, name="administrador"),
     path('tomarPedido/', views.tomarPedido, name = "tomarPedido"),
     path('chef/', views.chef, name = "chef"),
     path('signout/', views.signout, name='signout'),
     path('createUser/', views.createUser, name='createUser'),
     path("showUsers/",views.showUsers, name ="showUsers"),
     path("listUsers/",views.listUsers, name = "listUsers"),
     path("listMesas/",views.listMesas, name = "listMesas"),
     path("deleteUser/<int:user_id>",views.deleteUser, name ="deleteUser")
] 