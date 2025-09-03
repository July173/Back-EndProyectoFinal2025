from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def enviar_desactivacion_usuario(email_destino, nombre, fecha_desactivacion):
    asunto = "Cuenta desactivada"
    html_content = render_to_string(
        'DesactivacionUsuario.html',  # Debes crear esta plantilla
        {
            'nombre': nombre,
            'fecha_desactivacion': fecha_desactivacion,
        }
    )
    msg = EmailMultiAlternatives(
        asunto,
        '',  # Texto plano opcional
        settings.EMAIL_HOST_USER,
        [email_destino]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()