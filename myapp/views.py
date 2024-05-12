from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .models import User
from .models import Mesa
from .models import Producto
from .models import Pedido
from mysite import settings
from django.contrib.auth.decorators import login_required
import os
from django.core import serializers

# Create your views here.

def signin(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                errors = {}
                if not username:
                    errors['username_error'] = "Por favor, introduce tu nombre de usuario."
                if not password:
                    errors['password_error'] = "Por favor, introduce tu contraseña."
                else:
                    errors['username_error'] = "El nombre de usuario o la contraseña no coinciden."
                return render(request, 'index.html', errors)
            login(request, user)
            if user.is_waiter == 1:
                return redirect('/verMesas')
            if user.is_chef == 1:
                return redirect('/chef')
            if user.is_superuser == 1:
                return redirect('/administrador')
            
        except Exception as e:
            return HttpResponse(f"Error al logearse: {str(e)}")

def createUser(request):
    if request.method == 'GET':
        return render(request, 'createUser.html')
    else:
        try:
            if request.POST["Tipo"] == 'Mesero':
                    is_waiter=1
                    is_chef=0
            else:
                    is_chef=1
                    is_waiter =0

            user = User.objects.create_user(
                request.POST["username"],
                password=request.POST["password"],
                first_name=request.POST["name"],
                last_name=request.POST["lastname"],
                email=request.POST["email"],
                is_waiter = is_waiter,
                is_chef = is_chef
            )        
            user.save()
            return redirect('administrador')
        except Exception as e:
            return HttpResponse(f"Error al registrar el usuario: {str(e)}")            
       
def administrador(request):
    user_id = request.user.id
    users = User.objects.get(id=user_id)
    return render(request,'administrador.html',{'users':users})

def verMesas(request):
    user_id = request.user.id
    users = User.objects.get(id=user_id)
    return render(request,'verMesas.html',{'users':users})
  

def chef(request):
    user_id = request.user.id
    usuario = User.objects.get(id=user_id)
    pedidos = Pedido.objects.all()  # Obtén todos los pedidos
    return render(request, 'chef.html', {'usuario': usuario, 'pedidos': pedidos})
    
def showUsers(request):
    users = User.objects.all()
    return render(request, 'showUsers.html', {'users': users})

def listUsers(_request):
    user = list(User.objects.values())
    data = {'user': user}
    return JsonResponse(data)
 
def listMesas(request):
   mesa = list(Mesa.objects.values())
   data = {'mesa': mesa}
   return JsonResponse(data)

def listMesasPorId(request, idMesa):
    if request.method == 'GET':
        mesa = get_object_or_404(Mesa, idMesa=idMesa)
        data = {
            'idMesa': mesa.idMesa,
            'numero': mesa.numero,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
def listProductos(request):
   mesa = list(Producto.objects.values())
   data = {'producto': mesa}
   return JsonResponse(data) 
    
def deleteUser(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    usuario.delete()
    return redirect('/showUsers')

def createProduct(request):
    if request.method == 'GET':
        return render(request, 'createProduct.html')
    elif request.method == 'POST':
        try:
            # Convertir el valor del toggle a un booleano
            disponible = request.POST.get("toggleDisponible", False) == "on"

            # Obtener la instancia del Producto del formulario
            producto = Producto(
                nombre=request.POST["nombreProducto"],
                descripcion=request.POST["Descripcion"],
                precio=request.POST["Precio"],
                disponible=disponible
            )

            # Guardar la imagen en la carpeta restaurante/myapp/static/img
            if 'imgProducto' in request.FILES:
                imagen = request.FILES['imgProducto']
                ruta_imagen = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', imagen.name)
                with open(ruta_imagen, 'wb') as f:
                    for chunk in imagen.chunks():
                        f.write(chunk)
                producto.imgProducto = os.path.join('img/', imagen.name)

            # Guardar el producto en la base de datos
            producto.save()
            return redirect('administrador')
        except Exception as e:
            return HttpResponse(f"Error al registrar el producto: {str(e)}")
            
def showProduct(request):
    Productos = Producto.objects.all()
    return render(request, 'showProduct.html', {'Productos': Productos})

def verPedido(request, idMesa):
    print (idMesa)
    pedidos = Pedido.objects.filter(mesa__numero=idMesa)
    return render(request, 'verPedido.html', {'pedidos': pedidos, 'idMesa': idMesa})


def tomarPedido(request, idMesa):
        productos = Producto.objects.all()
        return render(request, 'tomarPedido.html', {'Productos': productos})

def savePedido(request):
    productos_seleccionados = request.POST.getlist('producto')
    cantidad = int(request.POST['cantidad'])

    id_mesero = request.user.id
    id_mesa = 1  # Supongamos que la mesa tiene el id 1

    for producto_id in productos_seleccionados:
        if producto_id:  # Verificar si el producto_id no está vacío
         producto = Producto.objects.get(pk=producto_id)
         pedido = Pedido.objects.create(
             cantidad=cantidad,
             mesa_id=id_mesa,
             idMesero_id=id_mesero,
             idProducto_id=producto_id)
         pedido.save()  # Guardar el pedido en la base de datos
         print(id_mesero)
         print(cantidad)
         print(producto_id)
         print(id_mesa)
    return redirect('verMesas')  
    
def cambiar_estado_pedido(request, pedido_id):
    pedido = Pedido.objects.get(idPedido=pedido_id)
    pedido.hecho = not pedido.hecho  
    pedido.save()
    return redirect('chef')    

def  actualizarDatosUsuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':   
        user.is_active = request.POST.get('is_active') == 'true'
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.save()
    
   
@login_required
def signout(request):
    logout(request)
    return redirect("/")    

  