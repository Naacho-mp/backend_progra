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
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria_id')

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    items_por_pagina = request.GET.get('paginador', 12)

    page_number = request.GET.get('page')

    paginador = Paginator(productos, items_por_pagina)
    page_obj = paginador.get_page(page_number)
    
    context = {
        'categorias': categorias,
        'page_obj': page_obj,
        'categoria_id': categoria_id,  
    }

    return render(request, 'tienda/mostrar_productos.html', context)



def ver_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'tienda/ver_producto.html', {'producto': producto})


def agregar_producto(request):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES)

        if producto_form.is_valid():
            imagen = request.FILES.get('imagen')
            if imagen and imagen.content_type not in ['image/jpeg', 'image/png']:
                messages.error(request, "Error: Solo se permiten imágenes JPEG o PNG.")
                return render(request, 'tienda/actualizar_producto.html', {'producto_form': producto_form})

            precio = producto_form.cleaned_data.get('precio')
            stock = producto_form.cleaned_data.get('stock')

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

    return render(request, "tienda/agregar_producto.html", {'producto_form': producto_form})



def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES, instance=producto)

        if producto_form.is_valid():
            imagen = request.FILES.get('imagen')
            if imagen and imagen.content_type not in ['image/jpeg', 'image/png']:
                messages.error(request, "Error: Solo se permiten imágenes JPEG o PNG.")
                return render(request, 'tienda/actualizar_producto.html', {'producto_form': producto_form})

            precio = producto_form.cleaned_data.get('precio')
            stock = producto_form.cleaned_data.get('stock')

            if precio < 0 or stock < 0:
                messages.error(request, "Error: el precio y el stock deben ser positivos.")

            else:
                producto_form.save()
                messages.success(request, "¡Producto Actualizado exitosamente!")
                return redirect('mostrar_productos')
    else:
        producto_form = ProductoForm(instance=producto)

    data = {'producto_form': producto_form}
    return render(request, 'tienda/actualizar_producto.html', data)


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id) 

    producto.delete()
    return redirect('mostrar_productos')

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)

    return render(request, 'tienda/productos_filtrados.html', {
        'categoria': categoria,
        'productos': productos
    })





########################## CRUD CATEGORIA ####################################

def mostrar_categorias(request):
    categorias = Categoria.objects.all()
    data = {"categorias":categorias}

    return render (request, "categoria/mostrar_categorias.html", data)

def agregar_categoria(request):
    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST, request.FILES)

        if categoria_form.is_valid():
            categoria_form.save()
            return redirect('mostrar_categorias')

    else:
        categoria_form = CategoriaForm()
        
    data = {'categoria_form':categoria_form}
    return render(request, "categoria/agregar_categoria.html", data)


def actualizar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)

    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST, request.FILES, instance=categoria)

        if categoria_form.is_valid():
            categoria_form.save()
            return redirect('mostrar_categorias')

    else:
        categoria_form = CategoriaForm(instance=categoria)

    data = {'categoria_form': categoria_form}
    return render(request, 'categoria/actualizar_categoria.html', data)



def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id) 

    categoria.delete()
    return redirect('mostrar_categorias')

