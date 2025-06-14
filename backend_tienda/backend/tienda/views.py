from django.shortcuts import redirect, render, get_object_or_404
from tienda.models import Producto, Categoria
from tienda.forms import ProductoForm, CategoriaForm
from django.forms import modelform_factory
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import messages

ProductoForm = modelform_factory(Producto, exclude=[])
CategoriaForm = modelform_factory(Categoria, exclude=[])


########################## CRUD PRODUCTO ###################################

def mostrar_productos(request):
    # Funcion que se encarga de obtener todos los productos y categorias de la bd y el id de categoria
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria_id')

    # Se evalua si existe el id de una categoria, y se filtran los productos segun ello
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # Se dividen la cantidad de productos que se pueden ver por pagina a 12 productos
    items_por_pagina = request.GET.get('paginador', 12)
    page_number = request.GET.get('page')
    paginador = Paginator(productos, items_por_pagina)
    page_obj = paginador.get_page(page_number)
    
    # Se entrega un diccionario como contexto y luego renderiza
    context = {
        'categorias': categorias,
        'page_obj': page_obj,
        'categoria_id': categoria_id,  
    }

    return render(request, 'tienda/mostrar_productos.html', context)



def ver_producto(request, producto_id):
# Funcion que se encarga de buscar un producto en la bd segun el Id que se le entrega
# Luego se renderiza el html segun el producto que se encontró.
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'tienda/ver_producto.html', {'producto': producto})


def agregar_producto(request):
# Funcion que agrega un producto a la bd, verificando que sea en metodo POST
# Se utiliza el forms de Producto para verificar que lo se manda calza con el modelo
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES)
    
    # Se verifica que el formato sea valido
        if producto_form.is_valid():
            imagen = request.FILES.get('imagen')
            
            # Se verifica que la imagen sea con extension Jpeg o Png, sino es asi, lanza un error
            if imagen and imagen.content_type not in ['image/jpeg', 'image/png']:
                messages.error(request, "Error: Solo se permiten imágenes JPEG o PNG.")
                return render(request, 'tienda/agregar_producto.html', {'producto_form': producto_form})

            precio = producto_form.cleaned_data.get('precio')
            stock = producto_form.cleaned_data.get('stock')

            # Verificar que el precio y el stock a ingresar sean positivos, sino lanzar error
            # El mensaje se guarda en messages para luego mostrar en el html
            if precio< 0 or stock < 0:
                messages.error(request, "Error: el precio y el stock deben ser positivos.")
            else:
                producto_form.save()
                messages.success(request, "¡Producto Agregado exitosamente!")
                return redirect('mostrar_productos')
        else:
            messages.error(request, "Formulario inválido. Verifica los datos.")
    else:
        producto_form = ProductoForm()

    # Se renderiza el html de agregar producto
    return render(request, "tienda/agregar_producto.html", {'producto_form': producto_form})



def actualizar_producto(request, producto_id):
    # Funcion que obtiene un producto segun un id en la bd, sino lanzar un error 404
    producto = get_object_or_404(Producto, id=producto_id)

    # Se verifica que sea en metodo POST
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES, instance=producto)

        # Si es valido verificar las condiciones similares a la funcion anterior
        if producto_form.is_valid():
            imagen = request.FILES.get('imagen')
            if imagen and imagen.content_type not in ['image/jpeg', 'image/png']:
                messages.error(request, "Error: Solo se permiten imágenes JPEG o PNG.")
                return render(request, 'tienda/actualizar_producto.html', {'producto_form': producto_form})

            precio = producto_form.cleaned_data.get('precio')
            stock = producto_form.cleaned_data.get('stock')

            # Se verifica el precio y stock que sean positivos, sino lanzar error en el html
            if precio < 0 or stock < 0:
                messages.error(request, "Error: el precio y el stock deben ser positivos.")

            else:
                producto_form.save()
                messages.success(request, "¡Producto Actualizado exitosamente!")
                return redirect('mostrar_productos')
    else:
        producto_form = ProductoForm(instance=producto)

    data = {'producto_form': producto_form}

    # Se renderiza el html de actualizar producto
    return render(request, 'tienda/actualizar_producto.html', data)


def eliminar_producto(request, producto_id):
    # Funcion que se encarga de eliminar un producto segun un id entregado
    producto = get_object_or_404(Producto, pk=producto_id) 

    producto.delete()
    return redirect('mostrar_productos')

def productos_por_categoria(request, categoria_id):
    # Funcion que busca las categorias segun un id
    # Si encuentra productos filtrados segun la categoria, guardarlos
    # Luego estos se renderizan segun la categoria que se llama

    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)

    return render(request, 'tienda/productos_filtrados.html', {
        'categoria': categoria,
        'productos': productos
    })





########################## CRUD CATEGORIA ####################################

def mostrar_categorias(request):
    # Funcion que obtiene todas las categorias de la bd
    # Luego las renderiza y muestra en el html
    categorias = Categoria.objects.all()
    data = {"categorias":categorias}

    return render (request, "categoria/mostrar_categorias.html", data)

def agregar_categoria(request):
    # Funcion que se encarga de agregar una categoria nueva
    # Se verifica que sea en metodo POST

    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST, request.FILES)
    # Se verifica el forms segun lo especificado en forms.py, y lanza msjes segun messages
        if categoria_form.is_valid():
            categoria_form.save()
            messages.success(request, "¡Categoria agregada Exitosamente!")
            return redirect('mostrar_categorias')

    else:
        categoria_form = CategoriaForm()
        
    data = {'categoria_form':categoria_form}
    # Se renderiza el html de agregar categorias
    return render(request, "categoria/agregar_categoria.html", data)


def actualizar_categoria(request, categoria_id):
    # Funcion que actualiza una categoria segun un id en particular
    # Se verifica que el id exista, y se guarda en categoria
    categoria = Categoria.objects.get(id=categoria_id)

    # Se verifica que el metodo sea POST
    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST, request.FILES, instance=categoria)

    # Se valida el forms y lanza un msje capturado y mostrado en el html
        if categoria_form.is_valid():
            categoria_form.save()
            messages.success(request, "¡Categoria actualizada Exitosamente!")
            return redirect('mostrar_categorias')

    else:
        categoria_form = CategoriaForm(instance=categoria)

    data = {'categoria_form': categoria_form}
    # Se renderiza el html de actualizar categoria
    return render(request, 'categoria/actualizar_categoria.html', data)



def eliminar_categoria(request, categoria_id):
    #Funcion que se encarga de eliminar una categoria dado un id en particular
    categoria = get_object_or_404(Categoria, pk=categoria_id) 

    categoria.delete()
    return redirect('mostrar_categorias')

