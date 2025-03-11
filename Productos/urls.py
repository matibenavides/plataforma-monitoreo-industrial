from django.urls import path
from . import views

urlpatterns = [
    path('producto/<int:linea_id>', views.mostrarProducto, name="producto"),
    path('registrar_producto/<int:linea_id>', views.registrarProducto, name="registrarproducto"),

]
