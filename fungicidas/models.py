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

    def __str__(self):
        return str(self.nom_esp)
    
class Variedad(models.Model):
    especies_id = models.ForeignKey(Especies, on_delete=models.CASCADE)
    nom_var = models.TextField(max_length=20) #Nombre Variedad


    def __str__(self):
        return str(self.especies_id) + " - " + str(self.nom_var)
    
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


class Dia(models.Model): # Clase para la fecha de cada planilla
    dia_dia = models.DateField(db_index=True)

    def __str__(self):
        return str(self.dia_dia)
    

# ----------------------Tablas de Planillas---------------------------------- #



# Cloración Lineas de Proceso
class Cloracion(models.Model): # id_clo ()
    lineas_id = models.ForeignKey(Lineas, on_delete=models.CASCADE)
    turnos_id = models.ForeignKey(Turnos, on_delete=models.CASCADE)
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    sector_id = models.ForeignKey(Sector, on_delete=models.CASCADE)
    especies_id = models.ForeignKey(Especies, on_delete=models.CASCADE)
    dia_id = models.ForeignKey(Dia, on_delete=models.CASCADE)
    hor_clo = models.TimeField() # Hora 
    ppm_clo = models.IntegerField(null=True, blank=True) # PPM
    phe_clo = models.FloatField(null=True, blank=True) # PH cloración
    hcl_clo = models.IntegerField(null=True, blank=True) # Hipoclorito cloración
    aci_clo = models.IntegerField(null=True, blank=True) # Acido cloración
    loh_clo = models.IntegerField(null=True, blank=True) # Lote Hipoclorito
    loa_clo = models.IntegerField(null=True, blank=True) # Lote Acido
    obs_clo = models.TextField(max_length=200) # Observación

    def __str__(self):
        return str(self.lineas_id) + " - " + str(self.turnos_id) + " - " + str(self.trabajador_id) + " - " + str(self.sector_id) + " - " + str(self.especies_id) + " - " + str(self.dia_id) + " - " + str(self.hor_clo) + " - " + str(self.ppm_clo) + " - " + str(self.phe_clo) + " - " + str(self.hcl_clo) + " - " + str(self.aci_clo) + " - " + str(self.loh_clo) + " - " + str(self.loa_clo) + " - " + str(self.obs_clo)
    

    
# Control de Productos
class Productos(models.Model):
    lineas_id = models.ForeignKey(Lineas, on_delete=models.CASCADE)
    turnos_id = models.ForeignKey(Turnos, on_delete=models.CASCADE)
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    especies_id = models.ForeignKey(Especies, on_delete=models.CASCADE)
    variedad_id = models.ForeignKey(Variedad, on_delete=models.CASCADE)
    fungicidas_id = models.ForeignKey(Fungicidas, on_delete=models.CASCADE)
    dia_id = models.ForeignKey(Dia, on_delete=models.CASCADE)
    hor_pro = models.TimeField()
    cod_pro = models.IntegerField(null=False) 
    dof_pro = models.IntegerField(null=True, blank=True) # Dosificación Fungicida
    dor_pro = models.IntegerField(null=True, blank=True) # Dosificación Retard primafresh
    doa_pro = models.IntegerField(null=True, blank=True) # Dosificación Agua lts
    gas_pro = models.IntegerField(null=True, blank=True) # Gasto Litros * Hora
    kil_pro = models.IntegerField(null=True, blank=True) # Kilos de producción
    bin_pro = models.IntegerField(null=True, blank=True) # Numero de bins
    ren_pro = models.IntegerField(null=True, blank=True) # Rendimiento
    obs_pro = models.TextField(max_length=200) # Observación

    def __str__(self):
        return str(self.lineas_id) + " - " + str(self.turnos_id) + " - " + str(self.trabajador_id) + " - " + str(self.especies_id) + " - " + str(self.variedad_id) + " - " + str(self.fungicidas_id) + " - " + str(self.dia_id) + " - " + str(self.hor_pro) + " - " + str(self.cod_pro) + " - " + str(self.dof_pro) + " - " + str(self.dor_pro) + " - " + str(self.doa_pro) + " - " + str(self.gas_pro) + " - " + str(self.kil_pro) + " - " + str(self.bin_pro) + " - " + str(self.ren_pro) + " - " + str(self.obs_pro)


# Dosificación de Fungicidas
class Dosificacion(models.Model):
    lineas_id = models.ForeignKey(Lineas, on_delete=models.CASCADE)
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    especies_id = models.ForeignKey(Especies, on_delete=models.CASCADE)
    variedad_id = models.ForeignKey(Variedad, on_delete=models.CASCADE)
    fungicidas_id = models.ForeignKey(Fungicidas, on_delete=models.CASCADE)
    dia_id = models.ForeignKey(Dia, on_delete=models.CASCADE)
    hor_dos = models.TimeField()
    pei_dos = models.IntegerField(null=True, blank=True) # Peso Inicial
    pef_dos = models.IntegerField(null=True, blank=True) # Peso Final
    ccp_dos = models.IntegerField(null=False) # cc de Producto
    agu_dos = models.IntegerField(null=True, blank=True) # Dilución en agua
    cer_dos = models.IntegerField(null=True, blank=True) # Dilución en cera
    obs_dos = models.TextField(max_length=200)

    def __str__(self):
        return str(self.lineas_id) + " - " + str(self.trabajador_id) + " - " + str(self.especies_id) + " - " + str(self.variedad_id) + " - " + str(self.fungicidas_id) + " - " + str(self.dia_id) + " - " + str(self.hor_dos) + " - " + str(self.pei_dos) + " - " + str(self.pef_dos) + " - " + str(self.ccp_dos) + " - " + str(self.agu_dos) + " - " + str(self.cer_dos) + " - " + str(self.obs_dos)
    
# Temperaturas
class Temperatura(models.Model):
    lineas_id = models.ForeignKey(Lineas, on_delete=models.CASCADE)
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    turnos_id = models.ForeignKey(Turnos, on_delete=models.CASCADE)
    dia_id = models.ForeignKey(Dia, on_delete=models.CASCADE)
    hor_tem = models.TimeField()
    pul_tem = models.FloatField(null=True, blank=True) # Pulpa entrada
    agu_tem = models.FloatField(null=True, blank=True) # Agua Vaciado
    amb_tem = models.FloatField(null=True, blank=True) # Ambiente Camara
    est_tem = models.FloatField(null=True, blank=True) # Estanque Fungicida
    obs_tem = models.TextField(max_length=200)

    def __str__(self):
        return str(self.lineas_id) + " - " + str(self.trabajador_id) + " - " + str(self.turnos_id) + " - " + str(self.dia_id) + " - " + str(self.hor_tem) + " - " + str(self.pul_tem) + " - " + str(self.agu_tem) + " - " + str(self.amb_tem) + " - " + str(self.est_tem) + " - " + str(self.obs_tem)
    

# Medición PPM
class PPM(models.Model):
    lineas_id = models.ForeignKey(Lineas, on_delete=models.CASCADE)
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    turnos_id = models.ForeignKey(Turnos, on_delete=models.CASCADE)
    dia_id = models.ForeignKey(Dia, on_delete=models.CASCADE)
    hor_ppm = models.TimeField()
    dat_ppm = models.IntegerField(null=True, blank=True)
    phe_ppm = models.FloatField()
    obs_ppm = models.TextField(max_length=200)

    def __str__(self):
        return str(self.lineas_id) + " - " + str(self.trabajador_id) + " - " + str(self.turnos_id) + " - " + str(self.dia_id) + " - " + str(self.hor_ppm) + " - " + str(self.dat_ppm) + " - " + str(self.phe_ppm) + " - " + str(self.obs_ppm)
