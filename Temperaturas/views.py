from django.shortcuts import render

# Create your views here.



def mostrarTemperatura(request):
    return render(request, "temperaturas/base/temperatura.html")