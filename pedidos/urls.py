from django.urls import path

from . import views

urlpatterns = [
    #ruta, vista, nombre interno
    path('carrito/',views.carritoCompras, name='carritoCompras'),
    path('pedidos/',views.pedidos, name='pedidos'),
    path('agregar/<id>',views.agregarProducto, name='agregarProducto'),
    path('borrar/<id>',views.borrarProductoCarrito, name='borrarProducto')
]