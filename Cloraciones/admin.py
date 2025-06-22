from django.contrib import admin

# Register your models here.

from Cloraciones.models import *

class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom_tra', 'app_tra', 'apm_tra', 'nac_tra', 'rut_tra']
    search_fields = ['nom_tra', 'app_tra', 'apm_tra', 'nac_tra', 'rut_tra']

class EspeciesAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom_esp']
    search_fields = ['nom_esp']

class VariedadAdmin(admin.ModelAdmin):
    list_display = ['id', 'especies_id', 'nom_var']
    search_fields = ['especies_id', 'nom_var']

class FungicidasAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom_fun']
    search_fields = ['nom_fun']

class DiluyentesAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom_dil']
    search_fields = ['nom_dil']

class TurnosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom_tur']
    search_fields = ['nom_tur']

class SectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom_sec']
    search_fields = ['nom_sec']

class LineasAdmin(admin.ModelAdmin):
    list_display = ['id', 'num_lin']
    search_fields = ['num_lin']

class DiaAdmin(admin.ModelAdmin):
    list_display = ['dia_dia']
    search_fields = ['dia_dia']

#--------------------------- Grupo control de datos ---------------------------#

class GrupoCloracionAdmin(admin.ModelAdmin):
    list_display = ['id', 'loh_gru', 'loa_gru', 'dia_id', 'lineas_id', 'turnos_id', 'sector_id', 'especies_id', 'trabajador_id']
    search_fields = ['loh_gru', 'loa_gru', 'dia_id', 'lineas_id', 'turnos_id', 'sector_id', 'especies_id', 'trabajador_id']

class GrupoProductosAdmin(admin.ModelAdmin):
    list_display = ['id', 'obs_grp', 'dia_id', 'lineas_id', 'turnos_id',  'trabajador_id',  'fungicidas_id']
    search_fields = ['obs_grp', 'dia_id', 'lineas_id', 'turnos_id',  'trabajador_id',  'fungicidas_id']

class GrupoTemperaturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'obs_grt', 'dia_id', 'lineas_id', 'turnos_id', 'trabajador_id']
    search_fields = ['obs_grt', 'dia_id', 'lineas_id', 'turnos_id', 'trabajador_id']

#--------------------------- Tablas de Planillas  ---------------------------#

class CloracionAdmin(admin.ModelAdmin):
    list_display =['grupoclo_id', 'hor_clo', 'ppm_clo', 'phe_clo', 'hcl_clo', 'aci_clo', 'obs_clo']
    search_fields=['grupoclo_id', 'hor_clo', 'ppm_clo', 'phe_clo', 'hcl_clo', 'aci_clo', 'obs_clo']

class ProductosAdmin(admin.ModelAdmin):
    list_display = ['grupopro_id','especies_id', 'variedad_id', 'hor_pro', 'cod_pro', 'dof_pro', 'dor_pro', 'doa_pro', 'gas_pro', 'kil_pro', 'bin_pro', 'ren_pro']
    search_fields = ['grupopro_id','especies_id', 'variedad_id', 'hor_pro', 'cod_pro', 'dof_pro', 'dor_pro', 'doa_pro', 'gas_pro', 'kil_pro', 'bin_pro', 'ren_pro']

class DosificionAdmin(admin.ModelAdmin):
    list_display = ['lineas_id', 'trabajador_id', 'especies_id', 'variedad_id', 'fungicidas_id', 'dia_id', 'hor_dos', 'pei_dos', 'pef_dos', 'ccp_dos', 'agu_dos', 'cer_dos', 'obs_dos']
    search_fields = ['lineas_id', 'trabajador_id', 'especies_id', 'variedad_id', 'fungicidas_id', 'dia_id', 'hor_dos', 'pei_dos', 'pef_dos', 'ccp_dos', 'agu_dos', 'cer_dos', 'obs_dos']

class TemperaturaAdmin(admin.ModelAdmin):
    list_display = ['grupotem_id', 'hor_tem', 'pul_tem', 'agu_tem', 'amb_tem', 'est_tem']
    search_fields = ['grupotem_id', 'hor_tem', 'pul_tem', 'agu_tem', 'amb_tem', 'est_tem']

class PPMAdmin(admin.ModelAdmin):
    list_display = ['lineas_id', 'trabajador_id', 'turnos_id', 'dia_id', 'hor_ppm', 'dat_ppm', 'phe_ppm', 'obs_ppm']
    search_fields = ['lineas_id', 'trabajador_id', 'turnos_id', 'dia_id', 'hor_ppm', 'dat_ppm', 'phe_ppm', 'obs_ppm']

#--------------------------- Historial de Registros  ---------------------------#

class HistorialAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'trabajador_id', 'accion', 'content_object')
    list_filter = ('timestamp', 'accion', 'content_type', 'trabajador_id')
    search_fields = ('descripcion', 'trabajador_id__username')

#----------------------------------------------------------------------------#

admin.site.register(Trabajador, TrabajadorAdmin)
admin.site.register(Especies, EspeciesAdmin)
admin.site.register(Variedad, VariedadAdmin)
admin.site.register(Fungicidas, FungicidasAdmin)
admin.site.register(Diluyentes, DiluyentesAdmin)
admin.site.register(Turnos, TurnosAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Lineas, LineasAdmin)
admin.site.register(Dia, DiaAdmin)


admin.site.register(GrupoCloracion, GrupoCloracionAdmin)
admin.site.register(GrupoProductos, GrupoProductosAdmin)
admin.site.register(GrupoTemperatura, GrupoTemperaturaAdmin)

admin.site.register(Cloracion, CloracionAdmin)
admin.site.register(Productos, ProductosAdmin)
admin.site.register(Dosificacion, DosificionAdmin)
admin.site.register(Temperatura, TemperaturaAdmin)
admin.site.register(PPM, PPMAdmin)

admin.site.register(Historial, HistorialAdmin)


