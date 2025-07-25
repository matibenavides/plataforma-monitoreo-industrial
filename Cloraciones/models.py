from django.db import models
import datetime
from django.contrib.auth.models import User

#-- Para hacer la relación polimorfica al historial y las demas tablas
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
                                                                                    
# Create your models here.


class Trabajador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    nom_tra = models.CharField(max_length=20, db_index=True) #Nombre Trabajador
    app_tra = models.CharField(max_length=20, db_index=True) # Apellido Paterno Trabajador
    apm_tra = models.CharField(max_length=20, db_index=True) # Apellido Materno Trabajador
    nac_tra = models.DateField() # Nacimiento Trabajador
    rut_tra = models.IntegerField(null=True, blank=True, unique=True, db_index=True) # Rut Trabajador ( Unico y permite quedarse en blanco por el momento)


    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'
        indexes = [
            models.Index(fields=['nom_tra', 'app_tra']),
            models.Index(fields=['user']),
        ]

    # Metodo para visualización panel admin
    def __str__(self):
        return str(self.user) + " - " + str(self.nom_tra) + " - " + str(self.app_tra) + " - " + str(self.apm_tra) + " - " + str(self.nac_tra) + " - " + str(self.rut_tra)


class Historial(models.Model):
    trabajador_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Trabajador", db_index=True)
    ACCION_CHOICES = [
        ('CREACIÓN', 'Creación'),
        ('EDICIÓN', 'Edición'),
        ('ELIMINACIÓN', 'Eliminación'),
        ('OTRO', 'Otro'),
    ]
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES, verbose_name="Acción Realizada", db_index=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=True)  # Hacia que tabla se hizo referencia
    object_id = models.PositiveIntegerField(db_index=True)  # Guarda la pk (id) del registro afectado
    content_object = GenericForeignKey('content_type', 'object_id')  # campo que permite acceder al objeto
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora", db_index=True)
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción Adicional")

    class Meta:
        verbose_name = 'Registro de Historial'
        verbose_name_plural = 'Registros de Historial'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['trabajador_id', 'timestamp']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['accion', 'timestamp']),
        ]

    def __str__(self):
        actor = self.trabajador_id.username if self.trabajador_id else "Sistema"
        if self.content_object:
            return f'{self.timestamp.strftime("%d-%m-%Y %H:%M")} - {actor} realizó "{self.get_accion_display()}" en {self.content_object}'
        return f'{self.timestamp.strftime("%d-%m-%Y %H:%M")} - {actor} realizó "{self.get_accion_display()}" en un objeto borrado'
    


class Especies(models.Model):
    nom_esp = models.CharField(max_length=20, db_index=True) # Nombre Especie

    class Meta:
        verbose_name = 'Especie'
        verbose_name_plural = 'Especies'

    def __str__(self):
        return str(self.nom_esp)
    
class Variedad(models.Model):
    especies_id = models.ForeignKey(Especies, on_delete=models.CASCADE, db_index=True)
    nom_var = models.CharField(max_length=20, db_index=True) #Nombre Variedad

    class Meta:
        verbose_name = 'Variedad'
        verbose_name_plural = 'Variedades'
        indexes = [
            models.Index(fields=['especies_id', 'nom_var']),
        ]

    def __str__(self):
        return str(self.especies_id) + " - " + str(self.nom_var)
    
# Tabla con futuras variaciones (Pensando en añadir valores $, a parte de solo nombre)
class Fungicidas(models.Model): 
    nom_fun = models.CharField(max_length=30, db_index=True) # Nombre Fungicida

    class Meta:
        verbose_name = 'Fungicida'
        verbose_name_plural = 'Fungicidas'

    def __str__(self):
        return str(self.nom_fun)
    
class Diluyentes(models.Model):
    nom_dil = models.CharField(max_length=30, db_index=True)  # Nombre Diluyente

    class Meta:
        verbose_name = 'Diluyente'
        verbose_name_plural = 'Diluyentes'
        indexes = [
            models.Index(fields=['nom_dil']),
        ]

    def __str__(self):
        return str(self.nom_dil)
    

class Turnos(models.Model):
    nom_tur = models.CharField(max_length=20, db_index=True) # Nombre Turno

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'

    def __str__(self):
        return str(self.nom_tur)
    

class Sector(models.Model):
    nom_sec = models.CharField(max_length=20, db_index=True) # Nombre Sector

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'

    def __str__(self):
        return str(self.nom_sec)
    
class Lineas(models.Model):
    num_lin = models.IntegerField(null=False, db_index=True) # Nombre Linea (Dato obligatorio, añadir linea operativa)

    class Meta:
        verbose_name = 'Linea'
        verbose_name_plural = 'Lineas'

    def __str__(self):
        return str(self.num_lin)


class Dia(models.Model): # Clase para la fecha de cada planilla
    dia_dia = models.DateField(db_index=True)

    class Meta:
        verbose_name = 'Dia'
        verbose_name_plural = 'Dias'
        indexes = [
            models.Index(fields=['dia_dia']),
        ]

    def __str__(self):
        return str(self.dia_dia)
    

#-------------------------------Grupo control de datos------------------------#

class GrupoCloracion(models.Model):
    loh_gru = models.BigIntegerField(null=True, blank=True, db_index=True) # Lote Hipoclorito
    loa_gru = models.BigIntegerField(null=True, blank=True, db_index=True) # Lote Acido
    dia_id = models.ForeignKey(Dia, on_delete=models.CASCADE, db_index=True)
    lineas_id = models.ForeignKey(Lineas, on_delete=models.CASCADE, db_index=True)
    turnos_id = models.ForeignKey(Turnos, on_delete=models.CASCADE, db_index=True)
    sector_id = models.ForeignKey(Sector, on_delete=models.CASCADE, db_index=True)
    especies_id = models.ForeignKey(Especies, on_delete=models.CASCADE, db_index=True)
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE, db_index=True) 

    class Meta:
        verbose_name = 'Grupo Cloracion'
        indexes = [
            models.Index(fields=['dia_id', 'lineas_id', 'turnos_id']),
            models.Index(fields=['trabajador_id', 'dia_id']),
            models.Index(fields=['loh_gru', 'loa_gru']),
        ]

    def __str__(self):
        return str(self.loh_gru) + " - " + str(self.loa_gru) + " - " + str(self.dia_id) + " - " + str(self.lineas_id) + " - " + str(self.turnos_id) + " - " + str(self.sector_id) + " - " + str(self.especies_id) + " - " + str(self.trabajador_id)



class GrupoProductos(models.Model):
    obs_grp = models.CharField(max_length=200, db_index=True)
    dia_id = models.ForeignKey(Dia, on_delete=models.CASCADE, db_index=True)
    lineas_id = models.ForeignKey(Lineas, on_delete=models.CASCADE, db_index=True)
    turnos_id = models.ForeignKey(Turnos, on_delete=models.CASCADE, db_index=True)
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE, db_index=True)
    fungicidas_id = models.ForeignKey(Fungicidas, on_delete=models.CASCADE, db_index=True)

    class Meta:
        verbose_name = 'Grupo Producto'
        indexes = [
            models.Index(fields=['dia_id', 'lineas_id', 'turnos_id']),
            models.Index(fields=['trabajador_id', 'dia_id']),
        ]

    def __str__(self):
        return str(self.obs_grp) + " - " + str(self.dia_id) + " - " +str(self.lineas_id) + " - " + str(self.turnos_id) + " - " + str(self.trabajador_id) + " - " + str(self.fungicidas_id)



class GrupoTemperatura(models.Model):
    obs_grt = models.CharField(max_length=500, db_index=True)  # Mantener 500 para el lorem ipsum
    dia_id = models.ForeignKey(Dia, on_delete=models.CASCADE, db_index=True)
    lineas_id = models.ForeignKey(Lineas, on_delete=models.CASCADE, db_index=True)
    turnos_id = models.ForeignKey(Turnos, on_delete=models.CASCADE, db_index=True)
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE, db_index=True)

    class Meta:
        verbose_name = 'Grupo Temperatura'
        indexes = [
            models.Index(fields=['dia_id', 'lineas_id', 'turnos_id']),
            models.Index(fields=['trabajador_id', 'dia_id']),
        ]

    def __str__(self):
        return str(self.obs_grt) + " - " + str(self.dia_id) + " - " + str(self.lineas_id) + " - " + str(self.turnos_id) + " - " + str(self.trabajador_id)



# ----------------------Tablas de Planillas---------------------------------- #



# Cloración Lineas de Proceso
class Cloracion(models.Model): # id_clo ()
    grupoclo_id = models.ForeignKey(GrupoCloracion, on_delete=models.CASCADE)
    hor_clo = models.TimeField(blank=True, null=True, default=datetime.time(0, 0), db_index=True) # Hora 
    ppm_clo = models.IntegerField(null=True, blank=True, db_index=True) # PPM
    phe_clo = models.FloatField(null=True, blank=True, db_index=True) # PH cloración
    hcl_clo = models.IntegerField(null=True, blank=True, db_index=True) # Hipoclorito cloración
    aci_clo = models.IntegerField(null=True, blank=True, db_index=True) # Acido cloración
    obs_clo = models.CharField(max_length=200, blank=True, null=True) # Observación

    class Meta:
        verbose_name = 'Cloracion'
        verbose_name_plural = 'Cloraciones'

    def __str__(self):
        return str(self.grupoclo_id) + " - " + str(self.hor_clo) + " - " + str(self.ppm_clo) + " - " + str(self.phe_clo) + " - " + str(self.hcl_clo) + " - " + str(self.aci_clo) + str(self.obs_clo)
    

    
# Control de Productos
class Productos(models.Model):
    grupopro_id = models.ForeignKey(GrupoProductos, on_delete=models.CASCADE)
    especies_id = models.ForeignKey(Especies, on_delete=models.SET_NULL, null=True, blank=True)
    variedad_id = models.ForeignKey(Variedad, on_delete=models.SET_NULL, null=True, blank=True)
    hor_pro = models.TimeField(blank=True, null=True, default=datetime.time(0, 0))
    cod_pro = models.CharField(max_length=20, null=False, blank=True)
    dof_pro = models.IntegerField(null=True, blank=True, db_index=True) # Dosificación Fungicida
    dor_pro = models.IntegerField(null=True, blank=True, db_index=True) # Dosificación Retard primafresh
    doa_pro = models.IntegerField(null=True, blank=True, db_index=True) # Dosificación Agua lts
    gas_pro = models.FloatField(null=True, blank=True, db_index=True) # Gasto Litros * Hora
    kil_pro = models.FloatField(null=True, blank=True, db_index=True) # Kilos de producción
    bin_pro = models.IntegerField(null=True, blank=True, db_index=True) # Numero de bins
    ren_pro = models.FloatField(null=True, blank=True, db_index=True) # Rendimiento
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return str(self.grupopro_id) + " - " + str(self.especies_id) + " - " + str(self.variedad_id) + " - " + str(self.hor_pro) + " - " + str(self.cod_pro) + " - " + str(self.dof_pro) + " - " + str(self.dor_pro) + " - " + str(self.doa_pro) + " - " + str(self.gas_pro) + " - " + str(self.kil_pro) + " - " + str(self.bin_pro) + " - " + str(self.ren_pro)


# Dosificación de Fungicidas
class Dosificacion(models.Model):
    lineas_id = models.ForeignKey(Lineas, on_delete=models.CASCADE)
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    especies_id = models.ForeignKey(Especies, on_delete=models.CASCADE)
    variedad_id = models.ForeignKey(Variedad, on_delete=models.CASCADE)
    fungicidas_id = models.ForeignKey(Fungicidas, on_delete=models.CASCADE)
    # diluyentes_id = models.ForeignKey(Diluyentes, on_delete=models.SET_NULL, null=True, blank=True) Necesario solo si existieran más diluciones, por ahora nop, En caso de mantenerlo, agregar el str(self.) 
    dia_id = models.ForeignKey(Dia, on_delete=models.CASCADE)
    hor_dos = models.TimeField(blank=True, null=True, default=datetime.time(0, 0), db_index=True)
    pei_dos = models.IntegerField(null=True, blank=True) # Peso Inicial
    pef_dos = models.IntegerField(null=True, blank=True) # Peso Final
    ccp_dos = models.IntegerField(null=False, db_index=True) # cc de Producto
    agu_dos = models.IntegerField(null=True, blank=True, db_index=True) # Dilución en agua
    cer_dos = models.IntegerField(null=True, blank=True, db_index=True) # Dilución en cera
    obs_dos = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Dosificacion'
        verbose_name_plural = 'Dosificaciones'

    def __str__(self):
        return str(self.lineas_id) + " - " + str(self.trabajador_id) + " - " + str(self.especies_id) + " - " + str(self.variedad_id) + " - " + str(self.fungicidas_id) + " - " + str(self.dia_id) + " - " + str(self.hor_dos) + " - " + str(self.pei_dos) + " - " + str(self.pef_dos) + " - " + str(self.ccp_dos) + " - " + str(self.agu_dos) + " - " + str(self.cer_dos) + " - " + str(self.obs_dos)
    
# Temperaturas
class Temperatura(models.Model):
    grupotem_id = models.ForeignKey(GrupoTemperatura, on_delete=models.CASCADE)
    hor_tem = models.TimeField(blank=True, null=True, default=datetime.time(0, 0), db_index=True)
    pul_tem = models.FloatField(null=True, blank=True, db_index=True) # Pulpa entrada
    agu_tem = models.FloatField(null=True, blank=True, db_index=True) # Agua Vaciado
    amb_tem = models.FloatField(null=True, blank=True, db_index=True) # Ambiente Camara
    est_tem = models.FloatField(null=True, blank=True, db_index=True) # Estanque Fungicida

    class Meta:
        verbose_name = 'Temperatura'
        verbose_name_plural = 'Temperaturas'
    

    def __str__(self):
        return str(self.grupotem_id) + " - " + str(self.hor_tem) + " - " + str(self.pul_tem) + " - " + str(self.agu_tem) + " - " + str(self.amb_tem) + " - " + str(self.est_tem)
    

# Medición PPM
class PPM(models.Model):
    lineas_id = models.ForeignKey(Lineas, on_delete=models.CASCADE)
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    turnos_id = models.ForeignKey(Turnos, on_delete=models.CASCADE)
    dia_id = models.ForeignKey(Dia, on_delete=models.CASCADE)
    hor_ppm = models.TimeField(blank=True, null=True, default=datetime.time(0, 0), db_index=True)
    dat_ppm = models.IntegerField(null=True, blank=True, db_index=True)
    phe_ppm = models.FloatField(null=True, blank=True, db_index=True)
    obs_ppm = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'PPM'

    def __str__(self):
        return str(self.lineas_id) + " - " + str(self.trabajador_id) + " - " + str(self.turnos_id) + " - " + str(self.dia_id) + " - " + str(self.hor_ppm) + " - " + str(self.dat_ppm) + " - " + str(self.phe_ppm) + " - " + str(self.obs_ppm)
