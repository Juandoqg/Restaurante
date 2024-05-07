from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Tus propiedades personalizadas
    is_chef = models.BooleanField(default=False)
    is_waiter = models.BooleanField(default=False)

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    nombre = models.CharField(max_length=50,default="")
    imgProducto = models.ImageField(upload_to="myapp/static/img", null=True)

class Mesa (models.Model):
    idMesa = models.AutoField(primary_key=True)
    numero = models.IntegerField()

class Pedido(models.Model):
    idPedido = models.AutoField(primary_key=True)
    idMesero = models.ForeignKey(User, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa,on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class Factura(models.Model):
    idFactura = models.AutoField(primary_key=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    hora = models.DateTimeField(auto_now_add=True)
    idPedido =models.ForeignKey(Pedido, on_delete=models.CASCADE)