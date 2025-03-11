from django.urls import path
from . import views

urlpatterns = [
    path('producto/<int:linea_id>', views.mostrarProducto, name="producto"),
    path('registrar_producto/<int:linea_id>', views.registrarProducto, name="registrarproducto"),

    path('archivos_producto/', views.mostrarListaProducto, name="listaproducto"),
    path('visualizar_producto/<int:grupo_id>/', views.visualizarProducto, name="visualizarproducto"),
    path('actualizar_producto/<int:grupo_id>/', views.actualizarProducto, name="actualizarproducto"),
    path('eliminar_producto/<int:grupo_id>/', views.eliminarProducto, name="eliminarproducto"),
    path('pdf_producto/<int:grupo_id>/', views.PDFProducto, name="pdfproducto")
]
