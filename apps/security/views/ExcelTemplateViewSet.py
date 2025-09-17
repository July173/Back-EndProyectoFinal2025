from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from django.http import HttpResponse
from apps.security.services.ExcelTemplateService import ExcelTemplateService


class ExcelTemplateViewSet(ViewSet):
    """
    ViewSet para generar y descargar plantillas de Excel para el registro masivo
    de instructores y aprendices.
    """
    
    service = ExcelTemplateService()

    @swagger_auto_schema(
        operation_description=(
            "Descarga la plantilla de Excel para el registro masivo de instructores. "
            "La plantilla incluye todos los campos necesarios y hojas auxiliares con "
            "datos actualizados de la base de datos (áreas de conocimiento, tipos de contrato, etc.)."
        ),
        tags=["Plantillas Excel"],
        responses={
            200: openapi.Response(
                "Archivo Excel descargado exitosamente",
                content={
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': {
                        'schema': {
                            'type': 'string',
                            'format': 'binary'
                        }
                    }
                }
            ),
            500: openapi.Response("Error interno del servidor")
        }
    )
    @action(detail=False, methods=['get'], url_path='instructor-template')
    def download_instructor_template(self, request):
        """
        Genera y descarga la plantilla de Excel para instructores.
        Incluye datos actualizados de áreas de conocimiento, tipos de contrato, etc.
        """
        try:
            # El servicio ya retorna un HttpResponse, así que lo devolvemos directamente
            return self.service.generate_instructor_template()
        except Exception as e:
            return Response(
                {"error": f"Error al generar la plantilla de instructores: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description=(
            "Descarga la plantilla de Excel para el registro masivo de aprendices. "
            "La plantilla incluye todos los campos necesarios y hojas auxiliares con "
            "datos actualizados de la base de datos (programas, fichas, etc.)."
        ),
        tags=["Plantillas Excel"],
        responses={
            200: openapi.Response(
                "Archivo Excel descargado exitosamente",
                content={
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': {
                        'schema': {
                            'type': 'string',
                            'format': 'binary'
                        }
                    }
                }
            ),
            500: openapi.Response("Error interno del servidor")
        }
    )
    @action(detail=False, methods=['get'], url_path='aprendiz-template')
    def download_aprendiz_template(self, request):
        """
        Genera y descarga la plantilla de Excel para aprendices.
        Incluye datos actualizados de programas, fichas, etc.
        """
        try:
            # El servicio ya retorna un HttpResponse, así que lo devolvemos directamente
            return self.service.generate_aprendiz_template()
        except Exception as e:
            return Response(
                {"error": f"Error al generar la plantilla de aprendices: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description=(
            "Obtiene información sobre las plantillas disponibles y sus características."
        ),
        tags=["Plantillas Excel"],
        responses={
            200: openapi.Response(
                "Información de plantillas obtenida exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'instructor_template': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                'fields': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                                'download_url': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        ),
                        'aprendiz_template': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                'fields': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                                'download_url': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    }
                )
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='template-info')
    def get_template_info(self, request):
        """
        Proporciona información sobre las plantillas disponibles.
        """
        try:
            info = {
                "instructor_template": {
                    "name": "Plantilla de Instructores",
                    "description": "Plantilla para registro masivo de instructores del SENA",
                    "fields": [
                        "Primer Nombre*", "Segundo Nombre", "Primer Apellido*", "Segundo Apellido",
                        "Tipo Identificación*", "Número Identificación*", "Teléfono*",
                        "Email Institucional*", "Tipo de Contrato*", "Fecha Inicio Contrato*",
                        "Fecha Fin Contrato*", "Área de Conocimiento*", "Contraseña Temporal*"
                    ],
                    "download_url": "/api/excel-templates/instructor-template/",
                    "additional_sheets": [
                        "Áreas de Conocimiento", "Tipos de Contrato", 
                        "Tipos de Identificación", "Instrucciones"
                    ]
                },
                "aprendiz_template": {
                    "name": "Plantilla de Aprendices",
                    "description": "Plantilla para registro masivo de aprendices del SENA",
                    "fields": [
                        "Primer Nombre*", "Segundo Nombre", "Primer Apellido*", "Segundo Apellido",
                        "Tipo Identificación*", "Número Identificación*", "Teléfono*",
                        "Email Institucional*", "Código Programa*", "Número Ficha*", "Contraseña Temporal*"
                    ],
                    "download_url": "/api/excel-templates/aprendiz-template/",
                    "additional_sheets": [
                        "Programas", "Fichas", "Tipos de Identificación", "Instrucciones"
                    ]
                }
            }
            
            return Response(info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Error al obtener información de plantillas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description=(
            "Procesa un archivo Excel con datos de instructores para registro masivo. "
            "Los usuarios creados quedan activos automáticamente. "
            "Retorna un resumen detallado de registros exitosos y errores."
        ),
        tags=["Registro Masivo"],
        manual_parameters=[
            openapi.Parameter(
                'file',
                openapi.IN_FORM,
                description="Archivo Excel con datos de instructores (.xlsx o .xls)",
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
        responses={
            201: openapi.Response(
                "Archivo procesado exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        ),
                        'errors': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        ),
                        'total_processed': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'successful_registrations': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: openapi.Response("Error en el archivo o datos"),
            500: openapi.Response("Error interno del servidor")
        }
    )
    @action(detail=False, methods=['post'], url_path='upload-instructor-excel')
    def upload_instructor_excel(self, request):
        """
        Procesa archivo Excel con datos de instructores para registro masivo.
        Los usuarios creados quedan activos automáticamente.
        """
        try:
            # Verificar que se envió un archivo
            if 'file' not in request.FILES:
                return Response(
                    {'error': 'No se encontró el archivo en la petición'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            excel_file = request.FILES['file']
            
            # Validar que es un archivo Excel
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                return Response(
                    {'error': 'El archivo debe ser de formato Excel (.xlsx o .xls)'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Procesar el archivo
            results = self.service.process_instructor_excel(excel_file)
            
            # Determinar el status code basado en los resultados
            if results['successful_registrations'] > 0:
                response_status = status.HTTP_201_CREATED
            elif results['total_processed'] == 0:
                response_status = status.HTTP_400_BAD_REQUEST
            else:
                response_status = status.HTTP_207_MULTI_STATUS
            
            return Response(results, status=response_status)
            
        except Exception as e:
            return Response(
                {'error': f'Error procesando archivo: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description=(
            "Procesa un archivo Excel con datos de aprendices para registro masivo. "
            "Los usuarios creados quedan activos automáticamente. "
            "Retorna un resumen detallado de registros exitosos y errores."
        ),
        tags=["Registro Masivo"],
        manual_parameters=[
            openapi.Parameter(
                'file',
                openapi.IN_FORM,
                description="Archivo Excel con datos de aprendices (.xlsx o .xls)",
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
        responses={
            201: openapi.Response(
                "Archivo procesado exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        ),
                        'errors': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        ),
                        'total_processed': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'successful_registrations': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: openapi.Response("Error en el archivo o datos"),
            500: openapi.Response("Error interno del servidor")
        }
    )
    @action(detail=False, methods=['post'], url_path='upload-aprendiz-excel')
    def upload_aprendiz_excel(self, request):
        """
        Procesa archivo Excel con datos de aprendices para registro masivo.
        Los usuarios creados quedan activos automáticamente.
        """
        try:
            # Verificar que se envió un archivo
            if 'file' not in request.FILES:
                return Response(
                    {'error': 'No se encontró el archivo en la petición'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            excel_file = request.FILES['file']
            
            # Validar que es un archivo Excel
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                return Response(
                    {'error': 'El archivo debe ser de formato Excel (.xlsx o .xls)'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Procesar el archivo
            results = self.service.process_aprendiz_excel(excel_file)
            
            # Determinar el status code basado en los resultados
            if results['successful_registrations'] > 0:
                response_status = status.HTTP_201_CREATED
            elif results['total_processed'] == 0:
                response_status = status.HTTP_400_BAD_REQUEST
            else:
                response_status = status.HTTP_207_MULTI_STATUS
            
            return Response(results, status=response_status)
            
        except Exception as e:
            return Response(
                {'error': f'Error procesando archivo: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )