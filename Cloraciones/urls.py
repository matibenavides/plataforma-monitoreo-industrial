from django.urls import path
from . import views


# Gestion de rutas para App Cloraciones

urlpatterns = [
    #----- Vista hacia plantilla Cloracion -----#
    path('cloracion/', views.mostrarCloracion),

    #----- Vista que guarda los registros de 'cloracion/' -----#
    path('guarda_estanque', views.registrarEstanque),
    path('guarda_cortapedicelo', views.registrarCortaPedicelo),
    path('guarda_retorno', views.registrarRetorno),

    #----- Vista hacia Listado de registros -----#
    path('archivos/', views.mostrarlistaonce),

]
