def is_soy_sena_email(email):
	"""Checks if the email ends with @soy.sena.edu.co."""
	if not email:
		return False
	return email.endswith('@soy.sena.edu.co')

def is_sena_email(email):
	"""Checks if the email ends with @sena.edu.co."""
	if not email:
		return False
	return email.endswith('@sena.edu.co')

def is_unique_email(email, user_model, exclude_user_id=None):
	"""Checks that the email is unique in the given model. Can exclude a user by id (for updates)."""
	if not email:
		return False
	queryset = user_model.objects.filter(email=email)
	if exclude_user_id:
		queryset = queryset.exclude(id=exclude_user_id)
	return not queryset.exists()

def is_unique_document_number(document_number, person_model, exclude_person_id=None):
	"""Checks that the document number is unique in the given model. Can exclude a person by id (for updates)."""
	if not document_number:
		return False
	queryset = person_model.objects.filter(number_identification=document_number)
	if exclude_person_id:
		queryset = queryset.exclude(id=exclude_person_id)
	return not queryset.exists()

def is_valid_phone_number(phone_number):
	"""Checks that the phone number has exactly 10 numeric digits."""
	if not phone_number:
		return False
	return str(phone_number).isdigit() and len(str(phone_number)) == 10

def validate_phone_number(value):
	"""Django Rest Framework validator for phone numbers."""
	from rest_framework import serializers
	if not is_valid_phone_number(value):
		raise serializers.ValidationError("El número de teléfono debe tener exactamente 10 dígitos numéricos")
	return value