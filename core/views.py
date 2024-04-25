from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Usuario, Eventos, Deporte, Notificacion, Equipos, Rendimiento, Campeonato, EquiposCampeonato
from .forms import EventoForm, UsuarioForm
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages

# import matplotlib.pyplot as plt




f = False

# Create your views here.
def home(request):
    return render(request, 'core/home.html',{})

def ins_seleccion(request):
    return render(request, 'core/ins_seleccion.html')

@login_required
def eventos(request):
    eventos = Eventos.objects.all()  #recibir los objetos del modelo
    print(request.user)  # Verifica si el usuario está autenticado
    print(eventos)
    return render(request, 'core/eventos.html', {"user":request.user, "eventos":eventos})


@login_required
def equipos(request):
    equipos = Equipos.objects.all()  #recibir los objetos del modelo
    deportes = Deporte.objects.all()
    return render(request, 'core/equipos.html', {"user":request.user, "equipos":equipos, "deportes":deportes})

def create_event(request):
    if 'imagen' in request.FILES:
        evento = Eventos(
            nombre_ev = request.POST['nombre_ev'],  #lo que esta dentro de POST es lo mismo que se pone en el name del input en html
            fecha = request.POST['fecha'],
            hora = request.POST['hora'],
            lugar = request.POST['lugar'],
            descripcion = request.POST['descripcion'],
            estado = 'activo',
            imagen = request.FILES['imagen']
        )
    else:
        evento = Eventos(
        nombre_ev = request.POST['nombre_ev'],  #lo que esta dentro de POST es lo mismo que se pone en el name del input en html
        fecha = request.POST['fecha'],
        hora = request.POST['hora'],
        lugar = request.POST['lugar'],
        descripcion = request.POST['descripcion'],
        estado = 'activo',
        )

    evento.save()
    return redirect('eventos')

def crear_equipo(request):
    usuario_logueado = request.user
    deporteid = request.POST.get("idDeporte")
    if usuario_logueado.is_authenticated:
        lider_a = usuario_logueado.codigo
    if 'escudo' in request.FILES:
        equipo = Equipos(
            nombre_eq = request.POST['nombre_eq'],  #lo que esta dentro de POST es lo mismo que se pone en el name del input en html
            num_integrantes = request.POST['num_integrantes'],
            lider = lider_a,
            deporte = Deporte.objects.get(idDeporte=deporteid),
            escudo = request.FILES['escudo']
        )
    else:
        equipo = Equipos(
            nombre_eq = request.POST['nombre_eq'],  #lo que esta dentro de POST es lo mismo que se pone en el name del input en html
            num_integrantes = request.POST['num_integrantes'],
            lider = lider_a,
            deporte = Deporte.objects.get(idDeporte=deporteid)
        )

    equipo.save()
    return redirect('equipos')

def delete_event(request, id): #debe ir el id como parametro porque lo estamos capturando en el action del form
    if request.method == 'POST':
        # Obtener el usuario actual
        delete_event = Eventos.objects.get(id=id)
        delete_event.estado = 'eliminado'
        # Actualizar otros campos según sea necesario
        try:
            delete_event.save()
        except ValueError:
            print("jeje")
        # Redireccionar a alguna página de confirmación o a donde desees
        return redirect('eventos')
    else:
        # Manejar cualquier otro tipo de solicitud (GET, etc.)
        # Esto es opcional, dependiendo de tus necesidades
        return render(request, 'eventos.html')

def edit_event(request, id):
    edit_event = Eventos.objects.get(id=id)
    forms = EventoForm(request.POST or None, instance=edit_event)
    if forms.is_valid() and request.POST:
        forms.save()
        return redirect('eventos')
    return render(request, 'core/edit_event.html', {"user":request.user, "forms":forms})  

 
# def cargar_user(request, codigo):
#     cargar_user = Usuario.objects.get(codigo=codigo)
#     forms = UsuarioForm(request.POST or None, instance=cargar_user)
#     if forms.is_valid() and request.POST:
#         forms.save()
#         return redirect('')
#     return render(request, 'core/ins_seleccion.html', {"user":request.user, "forms":forms})

def exit(request):
    logout(request)
    return redirect('login')

@login_required
def rendimiento(request):
    rendimientos = Rendimiento.objects.filter(usuario=request.user)
    rendimientos.order_by("fecha")

    return render(request, 'core/rendimiento.html',{'rendimientos':rendimientos})

def buscar_usuario_rendimiento(request):
    busqueda_codigo = request.GET.get("codigo")
    usuario = None
    mensaje = "Debe ingresar un codigo"
    try:
        usuario = Usuario.objects.get(codigo=busqueda_codigo)
        if (usuario.seleccion != None) and (usuario.estado == 'aceptado'):
            mensaje = "Prueba jeje"
            request.session['codigo'] = busqueda_codigo
        else: 
            mensaje = f"El usuario con codigo {busqueda_codigo} no existe o no esta aceptado en la selección"
            usuario = None

    except Usuario.DoesNotExist:
        print ('lol')
    return render(request, 'core/rendimiento.html',{'usuario':usuario,'mensaje':mensaje})

def actualizar_rendimiento(request):
    codigo = request.session.get('codigo')  # Obtiene el código de la sesión
    campo1 = request.GET.get("campo1")
    campo2 = request.GET.get("campo2")
    campo3 = request.GET.get("campo3")
    campo4 = request.GET.get("campo4")
    campo5 = request.GET.get("campo5")
    fecha = request.GET.get("fecha")
    grasa = request.GET.get("grasa_corporal")
    masa = request.GET.get("masa_muscular")
    total = (int(campo1)+int(campo2)+int(campo3)+int(campo4)+int(campo5))/5
    try:
        usuario = Usuario.objects.get(codigo=codigo)
        re = Rendimiento(usuario=usuario,fecha=fecha,campo1=campo1,campo2=campo2,
                              campo3=campo3,campo4=campo4,campo5=campo5,grasa_corporal=grasa,masa_muscular=masa,rendimiento=total)
    except Usuario.DoesNotExist:
        mensaje = "Ocurrio un error al actualizar el rendimiento del jugador"
    try:
        re.save()
        mensaje = f"El rendimiento del estudiante {usuario.nombre} ha sido actualizado"
        info = f"!Se ha hecho una actualización de tu rendimiento en la selección de {usuario.seleccion} ¡"
        notificacion =  Notificacion(id_usuario=usuario,info=info)
        notificacion.save()

    except:
        print("je")
        mensaje = "Ocurrio un error al actualizar el rendimiento del jugador"

    return render(request, 'core/rendimiento.html',{'mensaje':mensaje})


def signup(request):
    print("asdasd")
    if request.method == 'POST':
        codigo = request.POST['username']
        password = request.POST['password']
        try:
            usuario = Usuario.objects.get(codigo=codigo, password=password)
            print("entro ")
            #Autenticación exitosa, redirigir a una página de éxito o realizar alguna acción
            #Por ejemplo, puedes redirigir al usuario a su página de perfil
            f =  True
            login(request, usuario)

            #return render(request,'core/home.html', {"user":request.user}) 
            return redirect("eventos")  
        except Usuario.DoesNotExist:
            print("codigo o clave incorrecto")
            mensaje_error = "Código o clave incorrectos. Por favor, inténtalo de nuevo."
            return render(request, 'registration/login.html', {'mensaje_error': mensaje_error}) 
    else:
        #Si la solicitud no es POST, mostrar el formulario de inicio de sesión
        print("asdasd")
        return render(request, 'core/home.html')
      
@login_required
def inscripcion(request):
    deportes = Deporte.objects.all()
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        # Obtener el usuario actual
        
        # Actualizar otros campos según sea necesario

        # Redireccionar a alguna página de confirmación o a donde desees
        return redirect('inscripcion')
    return render(request, 'core/ins_seleccion.html', {'deportes': deportes,'usuarios':usuarios})


@login_required
def actualizar_usuario_ins(request):
    if request.method == 'POST':
        # Obtener el usuario actual
        usuario = request.user
        # Actualizar los datos del usuario con los datos del formulario
        usuario.programa = request.POST.get('programa')
        usuario.semestre = request.POST.get('semestre')
        sele = request.POST.get('deporte')
        try:
            deporte = Deporte.objects.get(idDeporte=sele)
        except Deporte.DoesNotExist:
            return redirect("inscripcion")
        usuario.seleccion = deporte.nombre_dep
        usuario.estado = 'pendiente'
        # Actualizar otros campos según sea necesario
        try:
            usuario.save()
            mensaje = f"!Ha sido inscrito correctamente en la seleccion de {usuario.seleccion}, se le notificara si es aceptado!"
            notificacion =  Notificacion(id_usuario=request.user,info=mensaje)
            notificacion.save()
        except ValueError:
            print("jeje")
        # Redireccionar a alguna página de confirmación o a donde desees
        return redirect('inscripcion')
    else:
        # Manejar cualquier otro tipo de solicitud (GET, etc.)
        # Esto es opcional, dependiendo de tus necesidades
        return render(request, 'ins_seleccion.html')
    
def listar_eventos(request):#Buscador de eventos
    busqueda = request.GET.get("buscar_evento")
    busqueda_fecha = request.GET.get("buscar_fecha")
    eventos = Eventos.objects.all()
    if busqueda:
        eventos = Eventos.objects.filter(
            Q(nombre_ev__icontains = busqueda) |
            Q(lugar__icontains = busqueda) |
            Q(descripcion__icontains = busqueda) 
        ).distinct()
    if busqueda_fecha:
        # Parsear la fecha ingresada en el formulario
        try:
            fecha = datetime.strptime(busqueda_fecha, '%Y-%m-%d')
            # Filtrar eventos que tengan la fecha especificada
            eventos = eventos.filter(fecha=fecha)
        except ValueError:
            # Manejar el caso en que la fecha ingresada no sea válida
            pass    
    
    return render(request, 'core/eventos.html', {'eventos':eventos})

def buscar_aspirante_aceptar(request):
    busqueda_codigo = request.GET.get("buscar_aspirante_aceptar_nombre")
    busqueda_deporte = request.GET.get("buscar_aspirante_aceptar_deporte")
    print(busqueda_deporte)
    usuarios = Usuario.objects.all()
    deportes = Deporte.objects.all()
    try:
        if busqueda_deporte != "":
            deporte = Deporte.objects.get(idDeporte=busqueda_deporte)
    except Deporte.DoesNotExist():
        print("")

    
    if busqueda_codigo:
        usuarios = Usuario.objects.filter(
            Q(codigo__icontains = busqueda_codigo) |
            Q(nombre__icontains = busqueda_codigo)
        ).distinct()
        
    if busqueda_deporte:
        usuarios = usuarios.filter(
            seleccion = deporte.nombre_dep
        ).distinct()    
    return render(request, 'core/ins_seleccion.html', {'usuarios':usuarios,'deportes':deportes})

def actualizar_aspirante(request, codigo): #debe ir el id como parametro porque lo estamos capturando en el action del form
    if request.method == 'POST':
        # Obtener el usuario actual
        actualizar_aspirante = Usuario.objects.get(codigo=codigo)
        if actualizar_aspirante.estado == 'pendiente':
            actualizar_aspirante.estado = 'aceptado'
            mensaje = f'!Felicidades, has sido aceptado a la selección de {actualizar_aspirante.seleccion}¡'
            notificacion = Notificacion(id_usuario=actualizar_aspirante,info=mensaje)
            notificacion.save()
        else:
            mensaje = f'!Lo lamentamos, has sido expulsado de la selección de {actualizar_aspirante.seleccion}¡'
            notificacion = Notificacion(id_usuario=actualizar_aspirante,info=mensaje)
            notificacion.save()
            actualizar_aspirante.estado = None
            actualizar_aspirante.seleccion = None

        # Actualizar otros campos según sea necesario
        try:
            actualizar_aspirante.save()
        except ValueError:
            print("jeje")
        # Redireccionar a alguna página de confirmación o a donde desees
        #return render(request, 'core/ins_seleccion.html')
        return redirect('inscripcion')
    else:
        # Manejar cualquier otro tipo de solicitud (GET, etc.)
        # Esto es opcional, dependiendo de tus necesidades
        return render(request, 'core/ins_seleccion.html')
    


@login_required
def perfil(request):
    notificaciones = Notificacion.objects.filter(id_usuario=request.user)

    return render(request, 'core/perfil.html', {'notificaciones':notificaciones})

def leer_notificacion(request, id):
    notificacion = Notificacion.objects.get(id=id)
    notificacion.leida = True
    notificacion.save()
    return redirect('perfil')

def borrar_notificacion(request, id): #debe ir el id como parametro porque lo estamos capturando en el action del form
    notificacion_event = Notificacion.objects.get(id=id)
    notificacion_event.delete()
    return redirect('perfil')

@login_required
def campeonatos(request):
    deportes = Deporte.objects.all()
    equipos = Equipos.objects.filter(lider=request.user.codigo) 
    equipo_campeonato = EquiposCampeonato.objects.all()
    campeonatos = Campeonato.objects.all()
    return render(request,'core/campeonatos.html',{'deportes':deportes,'campeonatos':campeonatos, 'equipos':equipos, 'equipos_camp':equipo_campeonato})

def crear_campeonato(request):
    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        # Convierte la cadena de texto a una fecha
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        # Obtiene la fecha actual y agrega 7 días
        fecha_actual_mas_7_dias = timezone.now().date() + timedelta(days=7)

        if fecha_inicio < fecha_actual_mas_7_dias :
            messages.error(request, "La fecha de inicio del campeonato debe tener una anticipación de minimo 7 dias a la actual.")
            return redirect('crear_campeonato')
        else:
            deporteid = request.POST.get("idDeporte")
            deporte = Deporte.objects.get(idDeporte=deporteid)
            nombre = request.POST.get("nombre")
            tipo = request.POST.get("tipo")
            descripcion = request.POST.get("descripcion")
            campeonato = Campeonato(idDeporte=deporte,nombre=nombre,tipo=tipo,cupos_disponibles=tipo,descripcion=descripcion,fecha_inicio=fecha_inicio_str)
            print(campeonato)
            if Campeonato.objects.filter(nombre=nombre).exists():
                messages.error(request, "No se pueden repetir los nombres entre campeonatos.")
                return redirect('crear_campeonato')

            campeonato.save()    
    return redirect('campeonatos')

def lista_campeonatos(request):
    deportes = Deporte.objects.all()
    campeonatos = Campeonato.objects.all()
    equipos = Equipos.objects.filter(lider=request.user.codigo) 
    equipo_campeonato = EquiposCampeonato.objects.all()
    busqueda = request.GET.get("buscar_evento")
    busqueda_fecha = request.GET.get("buscar_fecha")
    busqueda_deporte = request.GET.get("buscar_deporte")
    print(busqueda_deporte)
    if busqueda:
        campeonatos = Campeonato.objects.filter(
            Q(nombre__icontains = busqueda) 
        ).distinct()
    if busqueda_deporte:
        campeonatos = campeonatos.filter(idDeporte=busqueda_deporte)
    if busqueda_fecha:
        # Parsear la fecha ingresada en el formulario
        try:
            fecha = datetime.strptime(busqueda_fecha, '%Y-%m-%d')
            # Filtrar eventos que tengan la fecha especificada
            campeonatos = campeonatos.filter(fecha_inicio=fecha)
        except ValueError:
            # Manejar el caso en que la fecha ingresada no sea válida
            pass    

    return render(request,'core/campeonatos.html',{'deportes':deportes,'campeonatos':campeonatos, 'equipos':equipos, 'equipos_camp':equipo_campeonato})

def inscribir_acampeonato(request, id):
    id_equipo_actualizar = request.POST.get('equipo')
    equipo = Equipos.objects.get(id=id_equipo_actualizar)
    if request.method == 'POST':
        campeonato_sele = Campeonato.objects.get(id=id)
        id_camp = campeonato_sele.id
        print(campeonato_sele)
        if campeonato_sele.idDeporte == equipo.deporte:
            estado = "pendiente"
            equipos_campeonato = EquiposCampeonato(campeonato=campeonato_sele, equipo=equipo, estado=estado)
            equipos_campeonato.save()
        else:
            print("los deportes no coinciden")    
    return redirect('campeonatos')
                
def inscribir_equipo_acampeonato(request, id):
    equipos = Equipos.objects.filter(lider=request.user.codigo) 
    campeonato_sele = Campeonato.objects.get(id=id)
    equipo_campeonato = EquiposCampeonato.objects.all()
    equipo_inscrito = EquiposCampeonato.objects.filter(
        campeonato=campeonato_sele, 
        equipo__in=equipos
        
    ).exists()
    
    if equipo_inscrito:
        # Redireccionar a alguna página o mostrar un mensaje de que ya está inscrito
        return redirect('eventos')
    else:
        # Si no está inscrito, mostrar el formulario para inscribirse al campeonato
        return render(request, 'campeonatos/InsCampeonato.html', {'campeonato': campeonato_sele, 'equipos': equipos})
    #return render(request,'campeonatos/InsCampeonato.html',{'equipos':equipos,"campeonato":campeonato_sele, 'equipos_camp':equipo_campeonato})

def aceptar_equipo_acampeonato(request, id):
    campeonato_sele = Campeonato.objects.get(id=id)
    equipos = EquiposCampeonato.objects.filter(campeonato=campeonato_sele)
    
    return render(request,'campeonatos/AceptarEquipos.html',{"equipos":equipos,"campeonato":campeonato_sele,"idd":id})

# def actualizar_estado_equipodfadasd(request, campeonato_id, equipo_id):
#     if request.method == 'POST':
#         actualizar_Equipo = Equipos.objects.get(id=equipo_id)
#         campeonato = Campeonato.objects.get(id=campeonato_id)
#         usuario = Usuario.objects.get(codigo=actualizar_Equipo.lider)
#         seleccion = EquiposCampeonato.objects.get(campeonato=campeonato,equipo=actualizar_Equipo)
#     if seleccion.estado == 'pendiente' or seleccion.estado == "" or seleccion.estado == None:
#         seleccion = 'aceptado'
#         mensaje = f'!Felicidades, tu equipo ha sido aceptado en el campeonato de {campeonato.nombre}¡'
#         notificacion = Notificacion(id_usuario=usuario,info=mensaje)
#         notificacion.save()
#         try:
#             seleccion.save()
#         except ValueError:
#             print("nada")
#     return redirect('aceptar_equipo_acampeonato', campeonato_id=campeonato_id)

def actualizar_estado_equipo_campeonato(request, id):
    if request.method == 'POST':
        actualizar_estado_equipo = EquiposCampeonato.objects.get(id=id)
        if actualizar_estado_equipo.estado == "pendiente":
            actualizar_estado_equipo.estado = "aceptado"
            actualizar_estado_equipo.campeonato.cupos_disponibles -= 1
            actualizar_estado_equipo.campeonato.save()  # Guardar el campeonato después de actualizar los cupos

            usuario = Usuario.objects.get(codigo=actualizar_estado_equipo.equipo.lider)
            mensaje = f'!Felicidades, tu equipo ha sido aceptado en el campeonato de {actualizar_estado_equipo.campeonato.nombre}¡'
            notificacion = Notificacion(id_usuario=usuario,info=mensaje)
            notificacion.save()
        elif actualizar_estado_equipo.estado == "aceptado":
            actualizar_estado_equipo.estado = "pendiente"
            actualizar_estado_equipo.campeonato.cupos_disponibles += 1
            actualizar_estado_equipo.campeonato.save()  # Guardar el campeonato después de actualizar los cupos

            usuario = Usuario.objects.get(codigo=actualizar_estado_equipo.equipo.lider)
            mensaje = f'!Tu equipo ha sido rechazado de participar en el campeonato de {actualizar_estado_equipo.campeonato.nombre}¡'
            notificacion = Notificacion(id_usuario=usuario,info=mensaje)
            notificacion.save()   
        try:
            actualizar_estado_equipo.save()
        except ValueError:
            print("jeje")
        # Redireccionar a alguna página de confirmación o a donde desees
        #return render(request, 'core/ins_seleccion.html')
        return redirect('aceptar_equipo_acampeonato', id=actualizar_estado_equipo.campeonato.id)
    else:
        # Manejar cualquier otro tipo de solicitud (GET, etc.)
        # Esto es opcional, dependiendo de tus necesidades
        return render(request, 'campeonatos/AceptarEquipos.html')


def creacion_emparejamientos(request,id):
    campeonato = Campeonato.objects.get(id=id)
    campeonato.estado = 'creado'
    lista = [1,2,3,4]
    cuatro = lista
    try:
        campeonato.save()
    except:
        print("lol")
    equipos_camp = EquiposCampeonato.objects.filter(campeonato=id)
    return render(request,'campeonatos/creacion_emparejamientos.html',{"equipos_camp":equipos_camp,"campeonato":campeonato,"cuatro":cuatro,"ocho":8,"16":16})


# def grafica_rendimiento(request):
#     # Obtener todos los objetos de rendimiento ordenados por fecha
#     rendimientos = Rendimiento.objects.filter(usuario=request.user)
#     rendimientos.order_by('fecha')

#     # Extraer las fechas y los valores de rendimiento
#     fechas = [rendimiento.fecha for rendimiento in rendimientos]
#     valores = [rendimiento.rendimiento for rendimiento in rendimientos]

#     # Crear la gráfica de líneas
#     plt.figure(figsize=(10, 6))
#     plt.plot(fechas, valores, marker='o', linestyle='-')
#     plt.title('Rendimiento Total a lo largo del tiempo')
#     plt.xlabel('Fecha')
#     plt.ylabel('Rendimiento Total')
#     plt.grid(True)
#     plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mejor legibilidad
#     plt.tight_layout()

#     # Guardar la gráfica como imagen o mostrarla en el navegador
#     # Puedes elegir una de las siguientes opciones:
#     # plt.savefig('rendimiento_total.png')  # Guardar la gráfica como imagen
#     plt.show()  # Mostrar la gráfica en el navegador

#     # Renderizar la plantilla con la gráfica
#     return render(request, 'grafica_rendimiento.html')