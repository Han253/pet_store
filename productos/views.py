from django.shortcuts import redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from datetime import datetime

from .forms import ProductoForm
from .models import Producto,Animal,Categoria

# Vista principal de Productos
def productosIndex(request):
    #consultar animales y categorias
    animales = Animal.objects.all()
    categorias = Categoria.objects.all()

    #Consultar productos
    productos_list = Producto.objects.all()
    #Configurar paginación cada 9 productos
    paginator = Paginator(productos_list, 9)

    #Obtener página
    page_number = request.GET.get('page',0)
    page_obj = paginator.get_page(page_number)
    #Obtener el template
    template = loader.get_template("productos.html")
    #Agregar el contexto
    context = {"page_obj": page_obj,"animales":animales,"categorias":categorias}
    #Retornar respuesta http
    return HttpResponse(template.render(context,request))

#Vista para ver detalles de un autor
def detalleProducto(request, id):
    #Consultar producto
    producto = Producto.objects.get(id=id)           

    #Consultar datos de producto
    context = {'producto':producto}
    #Obtener el template
    template = loader.get_template("detalleProducto.html")

    return HttpResponse(template.render(context,request))

# Vista principal de Gestión de Productos
def gestionProductos(request):
    #Consultar productos
    productos_list = Producto.objects.all()
    #Configurar paginación cada 10 productos
    paginator = Paginator(productos_list, 10)

    #Obtener página
    page_number = request.GET.get('page',0)
    page_obj = paginator.get_page(page_number)

    #Obtener el template
    template = loader.get_template("gestionProductos.html")
    #Agregar el contexto
    context = {"page_obj": page_obj}
    #Retornar respuesta http
    return HttpResponse(template.render(context,request))

# Vista para crear productos
def crearProducto(request):
    #Obtener el template
    template = loader.get_template("crearProducto.html")
    #Generar Formulario
    if request.method == "POST":
        form = ProductoForm(request.POST or None, request.FILES)
        if form.is_valid():
            #obtener datos del formulario
            producto_nuevo = form.save(commit=False)
            #Asignar fecha de creación
            producto_nuevo.fecha_creacion = datetime.now()
            #Guardar Producto
            producto_nuevo.save()
            return redirect('gestionProductos')
    else:
        form = ProductoForm()
    #Crear contexto
    context = {}
    context['form'] = form
    #Retornar respuesta http
    return HttpResponse(template.render(context,request))

# Vista de Productos
def editarProducto(request,id):
    #Obtener el template
    template = loader.get_template("editarProducto.html")
    #Buscar Producto
    obj = get_object_or_404(Producto, id = id)
    #formulario que contiene la instancia
    form = ProductoForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return redirect('gestionProductos')   
    #Agregar el contexto
    context = {}
    context['form'] = form
    #Retornar respuesta http
    return HttpResponse(template.render(context,request))

# Vista de Productos
def eliminarProducto(request,id):
    #Obtener el template
    template = loader.get_template("eliminarProducto.html")
    #Buscar el producto
    obj = get_object_or_404(Producto, id = id)
    if request.method == "POST":
        obj.delete()
        return redirect('gestionProductos')
    #Agregar el contexto
    context = {}
    #Retornar respuesta http
    return HttpResponse(template.render(context,request))