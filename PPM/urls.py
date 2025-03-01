from django.urls import path
from . import views


urlpatterns = [
    #----- Vista hacia plantilla PPM -----#
    #ppm, también lista registros
    path('ppm/<int:linea_id>', views.mostrarPPM, name="ppm"),
    path('registrar_ppm/<int:linea_id>', views.registrarPPM, name="registrarppm"),
    path('visualizar_ppm/<int:grupo_id>/', views.visualizarPPM, name="visualizarppm"),
    path('actualizar_ppm/<int:grupo_id>/', views.actualizarPPM, name="actualizarppm"),
    path('eliminar_ppm/<int:grupo_id>/', views.eliminarPPM, name="eliminarppm"),
    path('eliminarlista_ppm/<int:grupo_id>/', views.eliminarPPMLista, name="eliminarppmlista"),
    path('pdf_ppm/', views.DescargarPDFPPM, name="pdfppm"),

    path('archivos_ppm/', views.mostrarListaPPM, name="listappm"),
    
]


