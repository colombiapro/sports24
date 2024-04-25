from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import (home, eventos, exit, signup, create_event, delete_event, edit_event, 
                    rendimiento, inscripcion, actualizar_usuario_ins, listar_eventos, 
                    buscar_aspirante_aceptar, actualizar_aspirante, ins_seleccion,
                    perfil,leer_notificacion,borrar_notificacion, crear_equipo, equipos,
                    buscar_usuario_rendimiento,actualizar_rendimiento,campeonatos,crear_campeonato,lista_campeonatos,
                    inscribir_equipo_acampeonato,aceptar_equipo_acampeonato, inscribir_acampeonato,
                    actualizar_estado_equipo_campeonato,creacion_emparejamientos)

urlpatterns = [
    path('', home, name='home'),
    path('eventos/', eventos, name='eventos'),
    path('equipos/', equipos, name='equipos'),
    path('ins_seleccion/', ins_seleccion, name="ins_seleccion" ),
    path('logout/', exit, name='exit'),
    path('signup/', signup, name='signup'),
    path('new_event/', create_event, name='create_event'),
    path('new_team/', crear_equipo, name='create_team'),
    path('delete_event/<int:id>', delete_event, name="delete_event"),
    path('edit_event/<int:id>', edit_event, name="edit_event"),
    # path('cargar_user/<str:codigo>', cargar_user, name="cargar_user"),
    path('rendimiento/',rendimiento,name="rendimiento"),
    path('inscripcion/',inscripcion,name="inscripcion"),
    path('actualizar_usuario_ins/',actualizar_usuario_ins,name="actualizar_usuario_ins"),
    path('lista_eventos/', listar_eventos, name="lista_eventos"),
    path('buscar_aspirante_aceptarr/', buscar_aspirante_aceptar, name="buscar_aspirante_aceptarr"),
    path('actualizar_aspirantes/<str:codigo>', actualizar_aspirante, name="actualizar_aspirantes"),
    path('perfil/',perfil,name="perfil"),
    path('leer_notificacion/<int:id>',leer_notificacion,name="leer_notificacion"),
    path('borrar_notificacion/<int:id>', borrar_notificacion, name="borrar_notificacion"),
    path('buscar_usuario_rendimiento/',buscar_usuario_rendimiento,name="buscar_usuario_rendimiento"),
    path('actualizar_rendimiento/',actualizar_rendimiento,name="actualizar_rendimiento"),
    path('campeonatos/',campeonatos,name="campeonatos"),
    path('crear_campeonato',crear_campeonato,name="crear_campeonato"),
    path('lista_campeonatos',lista_campeonatos,name="lista_campeonatos"),
    path('inscribir_equipo_acampeonato/<int:id>',inscribir_equipo_acampeonato,name="inscribir_equipo_acampeonato"),
    path('actualizar_equipo/<int:id>',inscribir_acampeonato,name="actualizar_equipo"),
    path('aceptar_equipo_acampeonato/<int:id>',aceptar_equipo_acampeonato,name="aceptar_equipo_acampeonato"),
    path('actualizar_estado_equipo_campeonato/<int:id>',actualizar_estado_equipo_campeonato,name="actualizar_estado_equipo_campeonato"),
    path('creacion_emparejamientos/<int:id>',creacion_emparejamientos,name="creacion_emparejamientos"),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)