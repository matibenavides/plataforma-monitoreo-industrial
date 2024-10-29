from django.shortcuts import render

# Create your views here.


def iniciosesion(request):
    return render(request, "iniciosesion.html")

def muestramenu(request):
    return render(request, "menu.html")