from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.RequestAsignationService import RequestAsignationService
from apps.assign.entity.serializers.form.RequestAsignationSerializer import RequestAsignationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.assign.entity.serializers.form.FormRequestSerializer import FormRequestSerializer

class RequestAsignationViewset(BaseViewSet):
    """
    ViewSet for managing request assignments and form requests.
    All internal code, comments, and docstrings are in English. User-facing messages and API documentation remain in Spanish.
    """
    service_class = RequestAsignationService
    serializer_class = RequestAsignationSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_serializer(self, *args, **kwargs):
        # Use FormRequestSerializer only for specific actions
        if hasattr(self, 'action') and self.action in [
            'create_form_request', 'list_form_requests', 'form_request_detail', 'reject_form_request', 'get_pdf_url'
        ]:
            return FormRequestSerializer(*args, **kwargs)
        return self.serializer_class(*args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene la información detallada de una solicitud de formulario por su ID.",
        tags=["FormRequest"],
        responses={
            200: openapi.Response("Solicitud encontrada con todos los datos detallados."),
            404: openapi.Response("Error: {'success': False, 'error_type': 'not_found', 'message': 'Solicitud no encontrada', 'data': None}")
        }
    )
    @action(detail=True, methods=['get'], url_path='form-request-detail')
    def form_request_detail(self, request, pk=None):
        """
        Get detailed information for a form request by its ID.
        API documentation and user-facing messages remain in Spanish.
        """
        result = self.service_class().get_form_request_by_id(pk)
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_404_NOT_FOUND)

    
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las solicitudes de asignación.",
        tags=["RequestAsignation"]
    )
    def list(self, request, *args, **kwargs):
        """Return a list of all request assignments."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea una nueva solicitud de asignación.",
        tags=["RequestAsignation"]
    )
    def create(self, request, *args, **kwargs):
        """Create a new request assignment."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene la información de una solicitud específica.",
        tags=["RequestAsignation"]
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve information for a specific request assignment."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza la información completa de una solicitud.",
        tags=["RequestAsignation"]
    )
    def update(self, request, *args, **kwargs):
        """Update all information for a request assignment."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de una solicitud.",
        tags=["RequestAsignation"]
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update fields of a request assignment."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina físicamente una solicitud de la base de datos.",
        tags=["RequestAsignation"]
    )
    def destroy(self, request, *args, **kwargs):
        """Physically delete a request assignment from the database."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) de la solicitud especificada.",
        tags=["RequestAsignation"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Perform a logical (soft) delete of the specified request assignment.
        User-facing messages remain in Spanish.
        """
        deleted = self.service_class().soft_delete(pk)
        if deleted:
            # Success message in Spanish for user-facing response
            return Response(
                {"detail": "Eliminado lógicamente correctamente."},
                status=status.HTTP_204_NO_CONTENT
            )
        # Error message in Spanish for user-facing response
        return Response(
            {"detail": "No encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )


    
   

    @swagger_auto_schema(
        operation_description="Crear una nueva solicitud de formulario (sin PDF)",
        tags=["FormRequest"],
        request_body=FormRequestSerializer,
        responses={
            201: openapi.Response("Solicitud creada exitosamente"),
            400: openapi.Response("Error: {'success': False, 'error_type': 'not_found', 'message': 'Entidad no encontrada', 'data': None}")
        }
    )
    @action(detail=False, methods=['post'], url_path='form-request')
    def create_form_request(self, request):
        """
        Create a new form request (without PDF).
        API documentation and user-facing messages remain in Spanish.
        """
        serializer = FormRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Error en los datos de entrada',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        result = self.service_class().create_form_request(serializer.validated_data)
        if result['success']:
            request_id = result['data']['request_asignation']['id'] if result['data'] and 'request_asignation' in result['data'] else None
            return Response({"id": request_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Obtener lista de todas las solicitudes de formulario",
        tags=["FormRequest"],
        responses={
            200: openapi.Response(
                description="Lista obtenida exitosamente",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Se encontraron 5 solicitudes",
                        "count": 5,
                        "data": []
                    }
                }
            ),
            500: openapi.Response("Error: {'success': False, 'error_type': 'list_form_requests', 'message': 'Error al obtener las solicitudes', 'data': None}")
        }
    )
    @action(detail=False, methods=['get'], url_path='form-request-list')
    def list_form_requests(self, request):
        """
        Get a list of all form requests.
        API documentation and user-facing messages remain in Spanish.
        """
        result = self.service_class().list_form_requests()
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        result = self.service_class().get_pdf_url(pk)
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        
        
    @swagger_auto_schema(
        method='patch',
        operation_description="Rechaza una solicitud de formulario, cambiando el estado y guardando el mensaje de rechazo.",
        tags=["FormRequest"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["rejectionMessage"],
            properties={
                "rejectionMessage": openapi.Schema(type=openapi.TYPE_STRING, description="Motivo del rechazo")
            }
        ),
        responses={
            200: openapi.Response("Solicitud rechazada correctamente."),
            404: openapi.Response("Error: {'success': False, 'error_type': 'not_found', 'message': 'Solicitud no encontrada', 'data': None}")
        }
    )
    @action(detail=True, methods=['patch'], url_path='form-request-reject')
    def reject_form_request(self, request, pk=None):
        """
        Reject a form request, changing its state and saving the rejection message.
        API documentation and user-facing messages remain in Spanish.
        """
        rejection_message = request.data.get('rejectionMessage')
        if not rejection_message:
            return Response({
                'success': False,
                'message': 'Debes proporcionar el motivo del rechazo.'
            }, status=status.HTTP_400_BAD_REQUEST)
        result = self.service_class().reject_request(pk, rejection_message)
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_description="Obtiene información del dashboard del aprendiz autenticado (solicitud activa, instructor asignado, estado).",
        tags=["RequestAsignation"],
        manual_parameters=[
            openapi.Parameter(
                'apprentice_id',
                openapi.IN_QUERY,
                description="ID del aprendiz",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Información del dashboard del aprendiz"),
            404: openapi.Response("Aprendiz no encontrado")
        }
    )
    @action(detail=False, methods=['get'], url_path='apprentice-dashboard')
    def apprentice_dashboard(self, request):
        """
        Get dashboard information for the authenticated apprentice (active request, assigned instructor, state).
        API documentation and user-facing messages remain in Spanish.
        """
        apprentice_id = request.query_params.get('apprentice_id')
        if not apprentice_id:
            return Response({
                'success': False,
                'message': 'Se requiere el ID del aprendiz'
            }, status=status.HTTP_400_BAD_REQUEST)

        result = self.service_class().get_apprentice_dashboard(apprentice_id)
        if result.get('success', True):
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_description="Filtra solicitudes de formulario por búsqueda, estado o programa",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Buscar por nombre o número de documento", type=openapi.TYPE_STRING),
            openapi.Parameter('request_state', openapi.IN_QUERY, description="Filtrar por estado de solicitud", type=openapi.TYPE_STRING),
            openapi.Parameter('program_id', openapi.IN_QUERY, description="Filtrar por ID de programa", type=openapi.TYPE_INTEGER),
        ],
        tags=["FormRequest"],
    )
    @action(detail=False, methods=['get'], url_path='form-request-filtered')
    def filter_form_requests(self, request):
        """
        Filter form requests by search, state, or program.
        API documentation and user-facing messages remain in Spanish.
        """
        search = request.query_params.get('search')
        request_state = request.query_params.get('request_state')
        program_id = request.query_params.get('program_id')

        result = self.service_class().filter_form_requests(search, request_state, program_id)
        return Response(result, status=status.HTTP_200_OK if result['success'] else status.HTTP_400_BAD_REQUEST)
