from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from apps.assign.entity.serializers.AsignationFormSerializer import AsignationFormSerializer
from apps.assign.services.AsignationFormService import AsignationFormService

from rest_framework import viewsets
from rest_framework.response import Response

class AsignationFormViewset(viewsets.ViewSet):
	parser_classes = [MultiPartParser, FormParser]

	def create(self, request):
		"""
		Endpoint POST para crear el formulario de asignación.
		"""
		serializer = AsignationFormSerializer(data=request.data)
		if serializer.is_valid():
			result = AsignationFormService.create_form(serializer.validated_data)
			return Response({"message": "Formulario creado exitosamente", "id": result.id}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	"""
	ViewSet básico para AsignationForm. Personaliza según tu modelo y lógica.
	"""
	def list(self, request):
		return Response({"message": "Listado de AsignationForm"})
