
def is_soy_sena_email(email):
	"""Valida si el correo termina en @soy.sena.edu.co."""
	if not email:
		return False
	return email.endswith('@soy.sena.edu.co')

def is_sena_email(email):
	"""Valida si el correo termina en @sena.edu.co."""
	if not email:
		return False
	return email.endswith('@sena.edu.co')

def is_unique_email(email, user_model, exclude_user_id=None):
	"""Valida que el correo sea único en el modelo dado. Puede excluir un usuario por id (para updates)."""
	if not email:
		return False
	qs = user_model.objects.filter(email=email)
	if exclude_user_id:
		qs = qs.exclude(id=exclude_user_id)
	return not qs.exists()

def is_unique_document_number(number, person_model, exclude_person_id=None):
	"""Valida que el número de documento sea único en el modelo dado. Puede excluir una persona por id (para updates)."""
	if not number:
		return False
	qs = person_model.objects.filter(number_identification=number)
	if exclude_person_id:
		qs = qs.exclude(id=exclude_person_id)
	return not qs.exists()

def is_valid_phone_number(phone):
	"""Valida que el número de teléfono tenga exactamente 10 dígitos numéricos."""
	if not phone:
		return False
	return str(phone).isdigit() and len(str(phone)) == 10