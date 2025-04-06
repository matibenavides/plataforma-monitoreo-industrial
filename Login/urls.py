from django.urls import path
from . import views

# Gestion de rutas para App Login

urlpatterns = [
    path('',views.iniciosesion, name='inicio'),
    path('logout', views.cerrarsesion, name='logout'),
    path('menu',views.muestramenu, name='menu'),
    path('registro/', views.registroUsuario, name='registro'),
    
    path('anio_disponible/', views.aniosDisponibles, name='anio_disponible'),
    # path('grafico_clora/', views.graficoCloracion, name='grafico_clora'),

    path('grafico_cloracion/', views.graficoCloroAcido, name='grafico_cloro'),
    path('grafico_temp/', views.graficoTemperatura, name='grafico_temp'),
    path('grafico_ppm/', views.graficoPPM, name='grafico_ppm'),
    path('grafico_kgs/', views.graficoKilogramos, name='grafico_kgs'),
    
]
