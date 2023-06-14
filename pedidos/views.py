from django.shortcuts import loader,redirect
from django.http import HttpResponse
from django.contrib import messages


from productos.models import Producto
from .models import Pedido, EstadoPedido, PedidoProducto

#Pagina para agregar producto a carrito
def agregarProducto(request, id):
    #Consultar producto
    producto = Producto.objects.get(id=id)           

    #Agregar producto a Carrito
    if request.method == "POST":
        cantidad = request.POST['cantidad']
        if cantidad:
            #obtener pedido que tenga estado de carrito para el usuario
            estado = EstadoPedido.objects.filter(estado="carrito")[0]
            pedido = Pedido.objects.filter(ref_estado=estado,ref_usuario= request.user)                       
            if len(pedido)==0:
                pedido = Pedido.objects.create(ref_estado=estado,ref_usuario= request.user,valor_pedido=0)
            else:
                pedido = pedido[0]
            
            #Revisar si el pedido ya no tenia este producto agregado
            pedido_producto = PedidoProducto.objects.filter(pedido=pedido,producto=producto)
            valor = producto.precio*cantidad

            if len(pedido_producto)==0:
                
                pedido_producto = PedidoProducto(
                    pedido=pedido,
                    producto = producto,
                    cantidad = cantidad,
                    valor = valor
                )
            else:
                pedido_producto = pedido_producto[0]
                pedido_producto.cantidad = cantidad
                pedido_producto.valor = valor
            
            #Guardar asignación de pedido y producto
            pedido_producto.save()

            messages.success(request, "Producto Agregado")
            
            return redirect('productosIndex')

    #Consultar datos de producto
    context = {'producto':producto}
    #Obtener el template
    template = loader.get_template("agregarProducto.html")

    return HttpResponse(template.render(context,request))


#Pagina para ver el carrito de compras, corresonde al pedido que esta en estado carrito
def carritoCompras(request):
    #Consultar pedido en estado carrito "si existe"
    estado = EstadoPedido.objects.filter(estado="carrito")[0]
    pedido = Pedido.objects.filter(ref_estado=estado,ref_usuario= request.user)                       
    if len(pedido)==1:
        pedido = pedido[0]
        productosPedido = PedidoProducto.objects.filter(pedido=pedido)
        context = {"pedido":pedido,"productosPedido":productosPedido}
    else:
        context = {}
    
    #Obtener el template
    template = loader.get_template("carrito.html")

    return HttpResponse(template.render(context,request))