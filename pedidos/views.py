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
        cantidad = int(request.POST['cantidad'])
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
    #Agregar producto a Carrito
    if request.method == "POST":
        pedido = pedido[0]
        estado_procesador = EstadoPedido.objects.filter(estado="procesado")[0]
        pedido.ref_estado = estado_procesador
        productosPedido = PedidoProducto.objects.filter(pedido=pedido)
        total_pedido = 0
        for productoPedido in productosPedido:
            total_pedido += productoPedido.valor
        pedido.valor_pedido = total_pedido
        pedido.save()
        messages.success(request, "Pedido procesado")
        return redirect('productosIndex')
    else:
        if len(pedido)==1:
            pedido = pedido[0]
            productosPedido = PedidoProducto.objects.filter(pedido=pedido)
            total_pedido = 0
            for productoPedido in productosPedido:
                total_pedido += productoPedido.valor
            context = {"pedido":pedido,"productosPedido":productosPedido,"valorPedido":total_pedido}
        else:
            context = {}
    
    #Obtener el template
    template = loader.get_template("carrito.html")

    return HttpResponse(template.render(context,request))



#Controlador para borrar productos del carrito
def borrarProductoCarrito(request, id):
    #Consultar producto
    producto = Producto.objects.get(id=id)
    #Consultar pedido carrito
    estado = EstadoPedido.objects.filter(estado="carrito")[0]
    pedido = Pedido.objects.filter(ref_estado=estado,ref_usuario= request.user)[0]
    pedido_producto = PedidoProducto.objects.get(pedido=pedido,producto=producto)
    pedido_producto.delete()
    messages.warning(request, "Producto Eliminado")
    return redirect('carritoCompras')



#Pagina para ver el historial de pedidos
def pedidos(request):
    #Consultar pedido en estado carrito "si existe"
    pedidos = Pedido.objects.filter(ref_usuario= request.user) 
    
    context = {"pedidos":pedidos}
    
    #Obtener el template
    template = loader.get_template("pedidos.html")

    return HttpResponse(template.render(context,request))