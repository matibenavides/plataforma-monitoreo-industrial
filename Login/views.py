from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import formularioRegistro, TrabajadorForm

# Create your views here.


def iniciosesion(request):

    #verifica usuario
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['contraseña']

        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            messages.success(request, (f"Bienvenido {username}"))
            return redirect('menu')
        else:
            messages.success(request, "Hubo un error al iniciar sesión")
            return redirect('inicio')
    else:
        messages.success(request, "Debes iniciar sesión para acceder a este sitio")
        return render(request, "iniciosesion.html")
    

# Este metodo de @login_required funciona y al intentar viajar a /menu manualmente, me redirijirá al path con el nombre 'inicio'.
# El punto, es que no me enviará un mensaje como lo hace la función de abajo en caso de querer intentar ir hacia ese lugar,
# por lo tanto es eficaz en casos especificos por si deseo implementar un mensaje de error o no.

# @login_required(login_url='inicio')
# def muestramenu(request):
#     return render(request, "menu.html")


def muestramenu(request):
    if request.user.is_authenticated:
        return render(request, "menu.html")
    else:
        messages.success(request, "Debes iniciar sesión para acceder a este sitio")
    return redirect('inicio')

def cerrarsesion(request):
    logout(request)
    messages.success(request, "Has cerrado sesión")
    return redirect('inicio')

@login_required(login_url='inicio')
def registroUsuario(request):
    if request.method == 'POST':
        form = formularioRegistro(request.POST)
        formTrabajador = TrabajadorForm(request.POST)

        if form.is_valid() and formTrabajador.is_valid():
            usuario = form.save()
            trabajador = formTrabajador.save(commit=False)
            trabajador.user = usuario #asigno el usuario con el trabajador (sus datos)
            trabajador.save()

            #autentico y logeo
            nomUsuario = form.cleaned_data['username']
            contraseña = form.cleaned_data['password1']
            usuario = authenticate(username=nomUsuario, password=contraseña)
            login(request, usuario)
            messages.success(request, "Te has registrado correctamente")
            return redirect('menu')
    else:
        form = formularioRegistro()
        formTrabajador = TrabajadorForm()
        return render(request, 'registrousuario.html', {'form': form, 'formTrabajador': formTrabajador})


    return render(request, "registrousuario.html", {'form': form})