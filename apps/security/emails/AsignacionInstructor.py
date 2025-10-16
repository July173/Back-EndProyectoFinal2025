from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_assignment_to_instructor_email(email, name_apprentice, name_instructor):
    subject = 'Asignacion De Un Instructor De Seguimiento - SENA Sistema de Autogestión'
    from_email = settings.EMAILS_FROM_EMAIL if hasattr(settings, 'EMAILS_FROM_EMAIL') else 'no-reply@sena.edu.co'
    context = {
        'name_apprentice': name_apprentice,
        'name_instructor': name_instructor
    }
    html_content = render_to_string('AsignacionInstructorParaInstructor.html', context)
    msg = EmailMultiAlternatives(subject, '', from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_instructor_assignment_email(email, name_apprentice, name_instructor, document_number, email_apprentice):
    subject = 'Nueva Asignación de Seguimiento - SENA Sistema de Autogestión'
    from_email = settings.EMAILS_FROM_EMAIL if hasattr(settings, 'EMAILS_FROM_EMAIL') else 'no-reply@sena.edu.co'
    context = {
        'name_apprentice': name_apprentice,
        'name_instructor': name_instructor,
        'document_number': document_number,
        'email_apprentice': email_apprentice
    }
    html_content = render_to_string('AsignacionInstructor.html', context)
    msg = EmailMultiAlternatives(subject, '', from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
