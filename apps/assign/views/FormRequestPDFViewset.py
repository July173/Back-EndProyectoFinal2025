from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.assign.services.FormRequestPDFService import FormRequestService
from apps.assign.entity.serializers.form.FormPDFSerializer import FormPDFSerializer
   

class FormRequestPDFViewset(viewsets.ViewSet):
    """
    ViewSet para cargar archivos PDF en una solicitud.
    """
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=["FormRequest PDF"],
        manual_parameters=[
            openapi.Parameter('pdf_file', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
            openapi.Parameter('request_id', openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True)
        ],
        consumes=['multipart/form-data']
    )
    def create(self, request):
        request_id = request.data.get('request_id')
        if not request_id:
              return Response("request_id requerido", status=status.HTTP_400_BAD_REQUEST)
        serializer = FormPDFSerializer(data=request.data)
        if not serializer.is_valid():
            # Mostrar solo el primer error como texto plano
            first_error = next(iter(serializer.errors.values()))
            error_msg = first_error[0] if isinstance(first_error, list) else str(first_error)
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        result = FormRequestService().upload_pdf_to_request(int(request_id), serializer.validated_data)
        if result.get('detail'):
            return Response(result['detail'], status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Obtiene la URL del PDF de la solicitud.",
        tags=["FormRequest PDF"],
        responses={
            200: openapi.Response("URL del PDF obtenida correctamente."),
            404: openapi.Response("Error: {'success': False, 'error_type': 'not_found', 'message': 'Solicitud no encontrada', 'data': None}")
        }
    )
    @action(detail=True, methods=['get'], url_path='form-request-pdf-url')
    def get_pdf_url(self, request, pk=None):
        """
        Get the PDF URL for a form request.
        API documentation and user-facing messages remain in Spanish.
        """
        result = FormRequestService().get_pdf_url(pk)
        if result.get('detail'):
            return Response(result['detail'], status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_200_OK)
        