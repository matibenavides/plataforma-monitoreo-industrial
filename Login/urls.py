from django.urls import path
from . import views

# Gestion de rutas para App Login

urlpatterns = [
    path('',views.iniciosesion),
    path('menu',views.muestramenu),
]
