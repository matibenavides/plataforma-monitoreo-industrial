from django.urls import path
from . import views

urlpatterns = [
    #----- Vista hacia plantilla Temperatura -----#
    path('temperatura/<int:linea_id>', views.mostrarTemperatura, name="temperatura"),

    #----- Vista que guarda los registros de 'temperatura/' -----#
    path('guarda_temperatura', views.registrarTemperatura),

     #----- Vista hacia Listado de registros -----#
    path('archivos_temperatura/', views.mostrarListaTemperatura, name="listatemperatura"),
]
