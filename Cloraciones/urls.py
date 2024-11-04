from django.urls import path
from . import views


# Gestion de rutas para App Cloraciones

urlpatterns = [
    path('cloracion/', views.mostrarCloracion),
    path('guarda_estanque', views.registrarEstanque),
    path('archivos/', views.mostrarlistaonce),
    
    path('guarda_cortapedicelo', views.registrarCortaPedicelo),

]
