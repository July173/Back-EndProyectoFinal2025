from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_rejection_email(email, name_apprentice, message_rejection):
	subject = 'Solicitud rechazada - SENA Sistema de Autogestión'
	from_email = 'no-reply@sena.edu.co'
	context = {
		'name_apprentice': name_apprentice,
		'message_rejection': message_rejection
	}
	html_content = render_to_string('SolicitudRechazada.html', context)
	msg = EmailMultiAlternatives(subject, '', from_email, [email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
