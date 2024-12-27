from django.urls import path
from . import views

urlpatterns = [
    #----- Vista hacia plantilla Temperatura -----#
    path('temperatura/', views.mostrarTemperatura),
]
