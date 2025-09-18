from apps.assign.repositories.AsignationFormRepository import AsignationFormRepository

class AsignationFormService:
	@staticmethod
	def create_form(validated_data):
		"""
		Orquesta la lógica de negocio para la creación del formulario de asignación.
		Llama al repository y retorna el resultado para el ViewSet.
		"""
		# Aquí puedes agregar validaciones extra, lógica de negocio, etc.
		result = AsignationFormRepository.create_form(validated_data)
		return result
