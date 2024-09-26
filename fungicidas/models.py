from django.db import models

# Create your models here.


class Trabajador(models.Model):
    nom_tra = models.TextField(max_length=20) #Nombre Trabajador
    app_tra = models.TextField(max_length=20) # Apellido Paterno Trabajador
    apm_tra = models.TextField(max_length=20) # Apellido Materno Trabajador
    nac_tra = models.DateField() # Nacimiento Trabajador
    rut_tra = models.IntegerField(null=True, blank=True, unique=True) # Rut Trabajador ( Unico y permite quedarse en blanco por el momento)

    # Metodo para visualización panel admin
    def __str__(self):
        return str(self.nom_tra) + " - " + str(self.app_tra) + " - " + str(self.apm_tra) + " - " + str(self.nac_tra) + " - " + str(self.rut_tra)


class Especies(models.Model):
    nom_esp = models.TextField(max_length=20) # Nombre Especie
    var_esp = models.TextField(max_length=20)  # Variedad Especie

    def __str__(self):
        return str(self.nom_esp) + " - " + str(self.var_esp)
    
# Tabla con futuras variaciones (Pensando en añadir valores $, a parte de solo nombre)
class Fungicidas(models.Model): 
    nom_fun = models.TextField(max_length=30) # Nombre Fungicida

    def __str__(self):
        return str(self.nom_fun)
    

class Turnos(models.Model):
    nom_tur = models.TextField(max_length=20) # Nombre Turno

    def __str__(self):
        return str(self.nom_tur)
    

class Sector(models.Model):
    nom_sec = models.TextField(max_length=20) # Nombre Sector

    def __str__(self):
        return str(self.nom_sec)
    
class Lineas(models.Model):
    num_lin = models.IntegerField(null=False) # Nombre Linea (Dato obligatorio, añadir linea operativa)

    def __str__(self):
        return str(self.num_lin)


class Dia(models.Model):
    dia_dia = models.DateField()

    def __str__(self):
        return str(self.dia_dia)
# ----------------------Tablas de Planillas---------------------------------- #


# Plantilla Cloración Proceso 
# / borrar esto y nombres para control productos ( Productos )
# Cloracion proceso ( Cloracion )
# Dosificación fungicidas ( Fungicidas) este ya tengo uno que se llama asi lo cambio mñn
# Temperaturas asi tal cual
# Medicion ppm como -> Ppm 


class Cloracion(models.Model): # id_clo ()
    lineas = models.ForeignKey(Lineas, on_delete=models.CASCADE)
    turnos = models.ForeignKey(Turnos, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    especies = models.ForeignKey(Especies, on_delete=models.CASCADE)
    hor_clo = models.TimeField()