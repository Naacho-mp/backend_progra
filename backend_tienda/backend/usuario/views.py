from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout


# Create your views here.

def agregar_usuario(request):
    if request.method == 'POST':
        usuario_form = UserCreationForm(request.POST)
        if usuario_form.is_valid():
            usuario_form.save()
            return redirect('login')  
    else:
        usuario_form = UserCreationForm()
    
    return render(request, 'agregar_usuario.html', {'usuario_form': usuario_form})

def logout_view(request):
    logout(request)

    return redirect('login')
   