from apps.assign.entity.models.RequestAsignation import RequestAsignation
from apps.assign.repositories.FormRequestPDFRepository import FormRequestRepository
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class FormRequestService:
    def error_response(self, detail, error_type="error"):
        """
        Returns a structured error response with 'detail' field.
        """
        return {
            'success': False,
            'error_type': error_type,
            'detail': str(detail),
            'data': None
        }
    """
    Service for handling PDF uploads to form requests.
    """
    def __init__(self):
        self.repository = FormRequestRepository()

    def upload_pdf_to_request(self, request_id, validated_data):
        """
        Uploads a PDF file to a form request, validates input, and returns a response.
        """
        try:
            logger.info(f"Iniciando carga de PDF para solicitud ID: {request_id}")  # User-facing log in Spanish

            pdf_file = validated_data['pdf_file']

            # BUSINESS VALIDATIONS

            # Validations for pdf_file 
            if not pdf_file:
                raise ValueError("No se proporcionó ningún archivo PDF")
            if not pdf_file.name.lower().endswith('.pdf'):
                raise ValueError("El archivo debe ser un PDF (.pdf)")
            if pdf_file.size > 1024 * 1024:
                raise ValueError("El archivo PDF no puede ser mayor a 1MB")

            # Validar request_id
            if not request_id or request_id <= 0:
                raise ValueError("ID de solicitud inválido")

            logger.info("Validaciones de negocio completadas exitosamente")  # User-facing log en español

            # ATOMIC TRANSACTION
            with transaction.atomic():
                # Delegate to repository (database only)
                updated_request = self.repository.update_request_pdf(request_id, pdf_file)

                if not updated_request:
                    raise ValueError(f"No se pudo actualizar la solicitud con ID {request_id}. Verifique que exista.")  # User-facing error in Spanish

                # Build response (presentation logic in service)
                response = {
                    'success': True,
                    'message': 'Archivo PDF cargado exitosamente',  # User-facing message in Spanish
                    'data': {
                        'request_id': updated_request.id,
                        'pdf_name': pdf_file.name,
                        'pdf_size': pdf_file.size,
                        'pdf_content_type': pdf_file.content_type,
                        'pdf_url': updated_request.pdf_request.url if updated_request.pdf_request else None,
                        'request_state': updated_request.request_state,
                        'updated_at': updated_request.request_date
                    }
                }

                logger.info(f"PDF cargado exitosamente para solicitud ID: {request_id}")  # User-facing log in Spanish
                return response

        except ValueError as e:
            logger.error(f"Error de validación en upload_pdf_to_request: {str(e)}")  # User-facing log in Spanish
            return {
                'success': False,
                'detail': str(e),
                'error_type': 'validation_error'
            }
        except Exception as e:
            logger.error(f"Error interno en upload_pdf_to_request: {str(e)}")  # User-facing log en Spanish
            return {
                'success': False,
                'detail': f'Error interno al cargar PDF: {str(e)}',  # User-facing message in Spanish
                'error_type': 'server_error'
            }


    def get_pdf_url(self, request_id):
        # Retrieve the PDF URL for a specific form request
        """
        Retrieves the PDF URL for a given form request.
        """
        try:
            solicitud = RequestAsignation.objects.get(pk=request_id)
            if solicitud.pdf_request:
                return {
                    'success': True,
                    'pdf_url': solicitud.pdf_request.url
                }
            else:
                return self.error_response('La solicitud no tiene PDF adjunto.', "no_pdf")
        except RequestAsignation.DoesNotExist:
            return self.error_response('Solicitud no encontrada.', "not_found")
        except Exception as e:
            return self.error_response(f"Error al obtener PDF: {e}", "get_pdf_url")