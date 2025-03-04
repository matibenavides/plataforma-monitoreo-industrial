from django.urls import path
from . import views


urlpatterns = [
    path('fungicida/<int:linea_id>', views.mostrarFungicida, name="fungicida"),

    path('registrar_fungicida/<int:linea_id>', views.registrarFungicida, name="registrarfungicida")
]
