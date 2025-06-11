from django.shortcuts import redirect, render, get_object_or_404
from tienda.models import Producto
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa 
from django.conf import settings
from datetime import datetime
import os

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
    return redirect('ver_carrito')


def pagado(request):
    carrito = request.session.get('carrito', {})
    
    request.session['boleta_carrito'] = carrito
    request.session['carrito'] = {}
    return render(request, 'carrito/pagado.html')



def boleta(request):
    carrito = request.session.get('boleta_carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    
    # Preparar los datos del carrito para la boleta
    carrito_detalle = []
    total = 0
    for producto in productos:
        cantidad = carrito[str(producto.id)]
        subtotal = producto.precio * cantidad
        total += subtotal
        
        carrito_detalle.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
            'categoria': producto.categoria.nombre if producto.categoria else "Sin categoría"
        })
    
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    template_path = 'Boleta.html'
    context = {
        'carrito': carrito_detalle,
        'total': total,
        'fecha_actual': fecha_actual
    }

    # Render template
    template = get_template(template_path)
    html = template.render(context)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="boleta_compra.pdf"'

    def link_callback(uri, rel):
        if uri.startswith(settings.STATIC_URL):
            path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
        elif uri.startswith(settings.MEDIA_URL):
            path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        else:
            path = None
        return path

    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        encoding='UTF-8',
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar PDF: %s' % pisa_status.err)
    return response