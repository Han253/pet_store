from django.db import models
from django.contrib.auth.models import User 

from productos.models import Producto

class EstadoPedido(models.Model):
    """
    Modelo que representa los posibles estados de los pedidos
    """
    estado = models.CharField(max_length=100)

    def __str__(self):
        return self.estado


class Pedido(models.Model):
    """
    Modelo que representa los pedidos que son generados por los clientes, los posibles
    estados de un pedido son creados por el administrador del sistema y asociados en la lógica de negocios.
    """
    ref_estado = models.ForeignKey(EstadoPedido, on_delete=models.DO_NOTHING)
    ref_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now=True)
    valor_pedido = models.IntegerField()
    productos = models.ManyToManyField(Producto, through="PedidoProducto")

    def __str__(self):
        return self.fecha_creacion



class PedidoProducto(models.Model):
    """
    Modelo que representa la asociación entre pedidos y productos, solo es necesaria
    cuando la relación muchos a muchos tiene campos adicionales
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    valor = models.IntegerField()

