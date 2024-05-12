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

@login_required
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

@login_required       
def administrador(request):
    user_id = request.user.id
    users = User.objects.get(id=user_id)
    return render(request,'administrador.html',{'users':users})

@login_required
def verMesas(request):
    user_id = request.user.id
    users = User.objects.get(id=user_id)
    return render(request,'verMesas.html',{'users':users})
  
@login_required
def chef(request):
    user_id = request.user.id
    usuario = User.objects.get(id=user_id)
    pedidos = Pedido.objects.all()  # Obtén todos los pedidos
    return render(request, 'chef.html', {'usuario': usuario, 'pedidos': pedidos})

@login_required    
def showUsers(request):
    users = User.objects.all()
    return render(request, 'showUsers.html', {'users': users})

@login_required
def listUsers(_request):
    user = list(User.objects.values())
    data = {'user': user}
    return JsonResponse(data)

@login_required 
def listMesas(request):
   mesa = list(Mesa.objects.values())
   data = {'mesa': mesa}
   return JsonResponse(data)

@login_required
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

@login_required    
def listProductos(request):
   mesa = list(Producto.objects.values())
   data = {'producto': mesa}
   return JsonResponse(data) 

@login_required    
def deleteUser(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    usuario.delete()
    return redirect('/showUsers')

@login_required
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

@login_required            
def showProduct(request):
    Productos = Producto.objects.all()
    return render(request, 'showProduct.html', {'Productos': Productos})

@login_required
def verPedido(request, idMesa):
    print (idMesa)
    pedidos = Pedido.objects.filter(mesa__numero=idMesa)
    return render(request, 'verPedido.html', {'pedidos': pedidos, 'idMesa': idMesa})

@login_required
def tomarPedido(request, idMesa):
    # Obtener solo los productos disponibles
    productos_disponibles = Producto.objects.filter(disponible=True)
    idMesa = idMesa
    print(idMesa)
    return render(request, 'tomarPedido.html', {'Productos': productos_disponibles, 'idMesa': idMesa})


@login_required
def savePedido(request, idMesa):
    if request.method == 'POST':
        try:
            # Obtener los productos seleccionados, sus cantidades y notas del formulario
            productos_seleccionados = request.POST.getlist('productos_seleccionados[]')
            cantidades = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('cantidad_')}
            notas = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('notas_')}
            
            idMesero = request.user.id
            idMesa = idMesa
            
            # Guardar los productos seleccionados en la base de datos
            for producto_id in productos_seleccionados:
                cantidad = int(cantidades.get(producto_id, 0))
                nota = notas.get(producto_id, '')  # Obtener la nota asociada al producto
                print(nota)
                if cantidad > 0:
                    pedido = Pedido.objects.create(
                        numeroPedido=idMesa,
                        cantidad=cantidad,
                        nota=nota,  
                        idMesero_id=idMesero,
                        mesa_id=idMesa,
                        idProducto_id=producto_id
                    )
                    pedido.save()
            # Después de guardar el pedido, redirigir a alguna página, por ejemplo:
            return redirect('verMesas')
        except Exception as e:
            # Manejar cualquier error que pueda ocurrir durante la creación del pedido
            return HttpResponseServerError(f"Error al guardar el pedido: {e}")


@login_required
def cambiar_estado_pedido(request, pedido_id):
    pedido = Pedido.objects.get(idPedido=pedido_id)
    pedido.hecho = not pedido.hecho  
    pedido.save()
    return redirect('chef') 

@login_required
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

  