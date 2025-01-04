from django.urls import path
from . import views

urlpatterns = [
    #----- Vista hacia plantilla Temperatura -----#
    path('temperatura/', views.mostrarTemperatura),

    #----- Vista que guarda los registros de 'temperatura/' -----#
    path('guarda_temperatura', views.registrarTemperatura),
]
