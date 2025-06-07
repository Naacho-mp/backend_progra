from django.shortcuts import redirect, render, get_object_or_404
from tienda.models import Producto
from django.views.decorators.http import require_POST
from django.contrib import messages

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    stock = producto.stock
    carrito = request.session.get('carrito', {})
    cantidad = int(request.POST.get('cantidad', 1))

    cantidad_actual = carrito.get(str(producto_id), 0)
    nueva_cantidad = cantidad_actual + cantidad
    
    if nueva_cantidad > stock:
        messages.error(request, f"No hay suficiente stock disponible del producto: '{producto.nombre}'")
        return redirect('ver_producto', producto_id = producto_id)
    
    carrito[str(producto_id)] = nueva_cantidad
    request.session['carrito'] = carrito

    messages.success(request, f"Se agregaron {cantidad} '{producto.nombre}' al carrito")
    return redirect('ver_producto', producto_id = producto_id)



def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    
    carrito_detalle = []
    total = 0 
    for producto in productos:
        cantidad = carrito[str(producto.id)]
        subtotal = producto.precio * cantidad
        total += subtotal  

        carrito_detalle.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })
    return render(request, 'carrito/ver_carrito.html', {
        'carrito': carrito_detalle,
        'total': total  
    })


@require_POST
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]

    request.session['carrito'] = carrito
    return redirect('ver_producto', producto_id=producto_id)


def pagado(request):
    carrito = request.session.get('carrito', {})

    request.session['carrito'] = {}
    return render(request, 'carrito/pagado.html')