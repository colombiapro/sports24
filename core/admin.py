from django.contrib import admin
from core.models import Usuario,Deporte,Campeonato,Eventos,Equipos,Desafios,Rendimiento,Notificacion

class UsuariosAdmin(admin.ModelAdmin):
    list_display=("codigo","nombre","edad","sexo","tipo")

class DeporteAdmin(admin.ModelAdmin):
    list_display=("idDeporte","nombre_dep")

class CampeonatoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Campeonato._meta.fields]

class EventosAdmin(admin.ModelAdmin):
    list_display=("nombre_ev","fecha","lugar","descripcion")

class EquiposAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Equipos._meta.fields]

class DesafiosAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Desafios._meta.fields]

class RendimientoAdmin(admin.ModelAdmin):
    llist_display = [field.name for field in Rendimiento._meta.fields]

class NotificacionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Notificacion._meta.fields]

admin.site.register(Usuario,UsuariosAdmin)
admin.site.register(Deporte,DeporteAdmin)
admin.site.register(Campeonato,CampeonatoAdmin)
admin.site.register(Eventos,EventosAdmin)
admin.site.register(Equipos,EquiposAdmin)
admin.site.register(Desafios,DesafiosAdmin)
admin.site.register(Rendimiento,RendimientoAdmin)
admin.site.register(Notificacion,NotificacionAdmin)

