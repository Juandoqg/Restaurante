from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .models import User
from .models import Mesa
from .models import Producto
from .models import Pedido
from django.contrib.auth.decorators import login_required

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
                return redirect('/tomarPedido')
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

def tomarPedido(request):
    user_id = request.user.id
    users = User.objects.get(id=user_id)
    return render(request,'tomarPedido.html',{'users':users})
  
def chef(request):
    user_id = request.user.id
    users = User.objects.get(id=user_id)
    return render(request,'chef.html',{'users':users})
    
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
    
def deleteUser(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    usuario.delete()
    return redirect('/showUsers')

def createProduct(request):
    if request.method == 'GET':
        return render(request, 'createProduct.html')
    else:
        try:
            # Convertir el valor del toggle a un booleano
            disponible = request.POST.get("toggleDisponible", False) == "on"

            producto = Producto.objects.create(
                nombre=request.POST["nombreProducto"],
                descripcion=request.POST["Descripcion"],
                precio=request.POST["Precio"],
                disponible=disponible
            )
            producto.save()
            return redirect('administrador')
        except Exception as e:
            return HttpResponse(f"Error al registrar el producto: {str(e)}")
            
def showProduct(request):
    Productos = Producto.objects.all()
    return render(request, 'showProduct.html', {'Productos': Productos})
















@login_required
def signout(request):
    logout(request)
    return redirect("/")    