from django.urls import path

from . import views

urlpatterns = [
    #ruta, vista, nombre interno
    path('',views.productosIndex, name='productosIndex'),
    path('gestion/',views.gestionProductos, name='gestionProductos'),
    path('crear/',views.crearProducto, name='crearProductos'),
    path('detalle/<id>/',views.detalleProducto, name='detalleProducto'),
    path('editar/<id>/',views.editarProducto, name='editarProductos'),
    path('borrar/<id>/',views.eliminarProducto, name='eliminarProductos')
]