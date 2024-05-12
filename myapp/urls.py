from django.urls import path
from . import views

urlpatterns = [
     path('',views.signin, name = "signin"),
     path('administrador/', views.administrador, name="administrador"),
     path('verMesas/', views.verMesas, name = "verMesas"),
     path('chef/', views.chef, name = "chef"),
     path('signout/', views.signout, name='signout'),
     path('createUser/', views.createUser, name='createUser'),
     path("showUsers/",views.showUsers, name ="showUsers"),
     path("listUsers/",views.listUsers, name = "listUsers"),
     path("listMesas/",views.listMesas, name = "listMesas"),
     path("listMesasPorId/<int:idMesa>",views.listMesasPorId, name = "listMesasPorId"),
     path("listProductos/",views.listProductos, name = "listProductos"),
     path("deleteUser/<int:user_id>/",views.deleteUser, name ="deleteUser"),
     path("actulizarDatosUsuario/<int:user_is>/",views.actualizarDatosUsuario,name="actulizarUsuario"),
     path('createProduct/', views.createProduct, name='createProduct'),
     path('tomarPedido/<int:idMesa>', views.tomarPedido, name='tomarPedido'),
     path('verPedido/<int:idMesa>/', views.verPedido, name='verPedido'),
     path('showProduct/', views.showProduct, name='showProduct'),
     path('cambiar_estado_pedido/<int:pedido_id>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido')
] 