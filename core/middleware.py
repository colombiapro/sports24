from .models import Notificacion

class ValidarNotificacionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        notificaciones = Notificacion.objects.filter(id_usuario=request.user)
        tiene_notificaciones = False

        if notificaciones.exists():
            tiene_notificaciones = True
            numero = notificaciones.count()
            i = 0
            for notificacion in notificaciones:
                if notificacion.leida:
                    i = i +1
            if numero == i:
                tiene_notificaciones = False



        request.tiene_notificaciones = tiene_notificaciones

        response = self.get_response(request)
        return response