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
    # Funcion que agrega productos creados en la bd segun una pk.
    # Se recupera el producto en la variable 'producto', y se accede a sus atributos.
    producto = get_object_or_404(Producto, pk=producto_id)

    stock = producto.stock
    carrito = request.session.get('carrito', {})
    cantidad = int(request.POST.get('cantidad', 1))

    # Se crea una variable 'cantidad_actual' para comparar con la cantidad que se ingresará.
    cantidad_actual = carrito.get(str(producto_id), 0)
    nueva_cantidad = cantidad_actual + cantidad
    
    # Se hace la comparacion entre la nueva cantidad, y el stock base del producto
    # Se captura el mensaje, para el caso donde lo que se agrega sea superior al stock

    if nueva_cantidad > stock:
        messages.error(request, f"No hay suficiente stock disponible del producto: '{producto.nombre}'")
        return redirect('ver_producto', producto_id = producto_id)
    
    carrito[str(producto_id)] = nueva_cantidad
    request.session['carrito'] = carrito

    # En el caso de exito, se envia un mensaje de agregado exitoso
    messages.success(request, f"Se agregaron {cantidad} '{producto.nombre}' al carrito")
    return redirect('ver_producto', producto_id = producto_id)



def ver_carrito(request):
    # Se accede a la sesion del usuario actual, para crear un diccionario con lo que tenga en su interior
    # carrito se convierte en un diccionario
    # Luego en la variable 'productos' se consulta a la bd si segun los id de carrito existen productos en la bd
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    
    carrito_detalle = []
    total = 0 
    # Se crea una lista vacia para el detalle del carrito
    
    for producto in productos:
        # Se recorren los productos, se guardan la cantidad, y se va creando el subtotal y total
        cantidad = carrito[str(producto.id)]
        subtotal = producto.precio * cantidad
        total += subtotal  

        # Se agregan estos valores a la lista creada antes
        carrito_detalle.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })
    # Se retorna a renderizar el html de ver carrito con el detalle de carrito y su total
    return render(request, 'carrito/ver_carrito.html', {
        'carrito': carrito_detalle,
        'total': total  
    })


@require_POST
def eliminar_del_carrito(request, producto_id):
# Se accede con el decorador @require.POST ya que se modificara el carrito
# Eliminar un articulo del carrito, se obtiene la sesion del carrito
    carrito = request.session.get('carrito', {})

# Se evalua si el id del producto se encuentra en el carrito
# Si es asi, se elimina, luego se vuelve a la sesion
# Se retorna a la vista del carrito con el producto eliminado
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]

    request.session['carrito'] = carrito
    return redirect('ver_carrito')


def pagado(request):
# Esta funcion simula el pago del producto
# Obtiene la sesion de usuario del carrito
# Vacia el carrito luego de pagado, y renderiza el html
    carrito = request.session.get('carrito', {})
    
    request.session['boleta_carrito'] = carrito
    request.session['carrito'] = {}
    return render(request, 'carrito/pagado.html')



def boleta(request):
# Funcion que obtiene la sesion de usuario en un diccionario 'boleta_carrito'
# Obtiene los productos consultando a la bd con filter
    carrito = request.session.get('boleta_carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    
    # Preparar los datos del carrito para la boleta
    carrito_detalle = []
    total = 0
    for producto in productos:
        cantidad = carrito[str(producto.id)]
        subtotal = producto.precio * cantidad
        total += subtotal
    
    # Se agregan las variables a la lista carrito_detalle
        carrito_detalle.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
            'categoria': producto.categoria.nombre if producto.categoria else "Sin categoría"
        })
    
    # Se obtiene la fecha actual de cuando se realizo la compra
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Se crea la direccion del template de la boleta, y se le da el contexto
    template_path = 'Boleta.html'
    context = {
        'carrito': carrito_detalle,
        'total': total,
        'fecha_actual': fecha_actual
    }

    # Renderizar el template de antes, y se le pasa el contexto o variables a rellenar
    template = get_template(template_path)
    html = template.render(context)

    # Crear la respuesta, diciendole al navegador que la respuesta sera mostrar un pdf con nombre definido
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="boleta_compra.pdf"'

    # Crear el PDF en base a Pisa de la libreria xhtml2pdf para convertir Html a PDF
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='UTF-8')

    if pisa_status.err:
        return HttpResponse('Error al generar PDF: %s' % pisa_status.err)
    return response

