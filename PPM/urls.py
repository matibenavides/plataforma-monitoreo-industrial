from django.urls import path
from . import views


urlpatterns = [
    #----- Vista hacia plantilla PPM -----#
    path('ppm/<int:linea_id>', views.mostrarPPM, name="ppm"),
    path('registrar_ppm/<int:linea_id>', views.registrarPPM, name="registrarppm"),
    # path('archivos_ppm/', views.mostrar)
]