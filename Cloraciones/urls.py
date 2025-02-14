from django.urls import path
from . import views


# Gestion de rutas para App Cloraciones

urlpatterns = [
    #----- Vista hacia plantilla Cloracion -----#
    path('cloracion/', views.mostrarCloracion, name="cloracion"),

    #----- Vista que guarda los registros de 'cloracion/' -----#
    path('guarda_estanque', views.registrarEstanque),
    path('guarda_cortapedicelo', views.registrarCortaPedicelo),
    path('guarda_retorno', views.registrarRetorno),

    #----- Vista hacia Listado de registros -----#
    path('archivos/', views.mostrarListaonce, name="archivos"),
    path('registro/<int:grupo_id>/', views.visualizarDatos, name="visualizar"),
    path('actualizar_registro/<int:grupo_id>/', views.actualizarRegistro, name="actualizar"),
    path('eliminar_registro/<int:grupo_id>/', views.eliminarRegistro, name="eliminar"),
    path('pdf/<int:grupo_id>/', views.DescargarPDF, name="pdf"),

]
