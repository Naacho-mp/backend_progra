"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tienda.views import *
from carrito.views import *
from usuario.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView




urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    # Tienda URLs
    path('mostrar_productos/', mostrar_productos, name='mostrar_productos'),
    path('ver_producto/<int:producto_id>/', ver_producto, name='ver_producto'),
    path('agregar_producto/', agregar_producto, name='agregar_producto'),
    path('actualizar_producto/<int:producto_id>/', actualizar_producto, name='actualizar_producto'),
    path('eliminar_producto/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    ]

urlpatterns += [    
    # Carrito URLs
    path('agregar_al_carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('pagado/', pagado, name='pagado'),
    ]


urlpatterns += [
    # Categoría URLs
    path('mostrar_categorias/', mostrar_categorias, name='mostrar_categorias'),
    path('agregar_categoria/', agregar_categoria, name='agregar_categoria'),
    path('actualizar_categoria/<int:categoria_id>/', actualizar_categoria, name='actualizar_categoria'),
    path('eliminar_categoria/<int:categoria_id>/', eliminar_categoria, name='eliminar_categoria'),
    ]

urlpatterns += [
    # Login, Logout usuario URLs
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('agregar_usuario/', agregar_usuario, name='agregar_usuario'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_view, name='logout'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)