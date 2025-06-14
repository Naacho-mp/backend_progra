from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout


# Create your views here.

def agregar_usuario(request):
    # Funcion que se encarga de agregar un usuario en django admin
    # Esto en base al formulario UserCreationForm de la clase User de django
    # Se verifica que el metodo sea POST
    if request.method == 'POST':
        usuario_form = UserCreationForm(request.POST)
        if usuario_form.is_valid():
            usuario_form.save()
            return redirect('login')  
    else:
        usuario_form = UserCreationForm()
    
    # Se renderiza el html de agregar usuario
    return render(request, 'agregar_usuario.html', {'usuario_form': usuario_form})

def logout_view(request):
    # Funcion que se encarga de cerrar la sesion de un usuario de django
    # Utiliza la función logout() de Django para invalidar la sesión.
    logout(request)

    # Luego se redirecciona al login por defecto de django
    return redirect('login')
   