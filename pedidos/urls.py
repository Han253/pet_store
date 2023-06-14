from django.urls import path

from . import views

urlpatterns = [
    #ruta, vista, nombre interno
    path('carrito/',views.carritoCompras, name='carritoCompras'),
    path('agregar/<id>',views.agregarProducto, name='agregarProducto')
]