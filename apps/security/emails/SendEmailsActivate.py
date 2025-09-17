from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def enviar_activacion_usuario(email_destino, nombre, email_usuario, password_temporal):
    import random, string
    # Agregar un carácter aleatorio al final de la contraseña temporal
    random_char = random.choice(string.ascii_letters + string.digits)
    password_temporal_mod = str(password_temporal) + random_char
    asunto = "Cuenta Activada - Credenciales de Acceso"
    html_content = render_to_string(
        'ActivacionUsuario.html',
        {
            'nombre': nombre,
            'email_usuario': email_usuario,
            'password_temporal': password_temporal_mod,
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
