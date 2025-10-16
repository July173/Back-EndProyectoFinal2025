from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_unassignment_to_instructor_email(email, name_instructor, name_apprentice):
    subject = 'Desvinculación De Una Asignación - SENA Sistema de Autogestión'
    from_email = settings.EMAILS_FROM_EMAIL if hasattr(settings, 'EMAILS_FROM_EMAIL') else 'no-reply@sena.edu.co'
    context = {
        'name_instructor': name_instructor,
        'name_apprentice': name_apprentice
    }
    html_content = render_to_string('DesvinculacionInstructor.html', context)
    msg = EmailMultiAlternatives(subject, '', from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
