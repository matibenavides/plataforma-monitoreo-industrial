from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def iniciosesion(request):
    return render(request, "iniciosesion.html")


def muestramenu(request):
    return render(request, "menu.html")


def cloracion(request):
    return render(request, "cloracion.html")

def slide(request):   # Este es una vista para mostrar el slide.html y probar su funcionamiento ante un nuevo cambio de slide.
    return render(request, "slide.html")