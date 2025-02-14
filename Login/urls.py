from django.urls import path
from . import views

# Gestion de rutas para App Login

urlpatterns = [
    path('',views.iniciosesion, name='inicio'),
    path('logout', views.cerrarsesion, name='logout'),
    path('menu',views.muestramenu, name='menu'),
    
]
