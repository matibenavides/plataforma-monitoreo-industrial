from django.urls import path
from . import views


# Gestion de rutas para App Cloraciones

urlpatterns = [
    path('cloracion/', views.cloracion),
    path('slide/', views.slide),
    path('guarda_estanque', views.registrarEstanque)



]
