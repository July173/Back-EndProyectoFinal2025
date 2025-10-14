from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from apps.security.services.excel.ExcelInstructorTemplateService import ExcelInstructorTemplateService
from apps.security.services.excel.ExcelAprendizTemplateService import ExcelAprendizTemplateService



class ExcelTemplateViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.instructor_service = ExcelInstructorTemplateService()
        self.apprentice_service = ExcelAprendizTemplateService()

    @swagger_auto_schema(
        operation_description=(
            "Downloads the Excel template for bulk instructor registration. "
            "The template includes all required fields and auxiliary sheets with "
            "up-to-date data from the database (knowledge areas, contract types, etc.)."
        ),
        tags=["Excel Templates"],
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
        Generates and downloads the Excel template for instructors.
        Includes up-to-date data for knowledge areas, contract types, etc.
        """
        try:
            response = self.instructor_service.generate_instructor_template()
            if isinstance(response, HttpResponse):
                return response
            else:
                return Response(
                    {"error": "Error generando la plantilla"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            return Response(
                {"error": f"Error al generar la plantilla de instructores: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description=(
            "Downloads the Excel template for bulk apprentice registration. "
            "The template includes all required fields and auxiliary sheets with "
            "up-to-date data from the database (programs, fichas, etc.)."
        ),
        tags=["Excel Templates"],
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
    def download_apprentice_template(self, request):
        """
        Generates and downloads the Excel template for apprentices.
        Includes up-to-date data for programs, fichas, etc.
        """
        try:
            response = self.apprentice_service.generate_apprentice_template()
            if isinstance(response, HttpResponse):
                return response
            else:
                return Response(
                    {"error": "Error generando la plantilla"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            return Response(
                {"error": f"Error al generar la plantilla de aprendices: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description=(
            "Gets information about available templates and their features."
        ),
        tags=["Excel Templates"],
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
                        'apprentice_template': openapi.Schema(
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
        Provides information about available templates.
        """
        try:
            info = {
                "instructor_template": {
                    "name": "Instructor Template",
                    "description": "Template for bulk registration of SENA instructors",
                    "fields": [
                        "Tipo Identificación*", "Número Identificación*", "Primer Nombre*", "Segundo Nombre",
                        "Primer Apellido*", "Segundo Apellido", "Correo Institucional*", "Número de Celular*",
                        "Área de Conocimiento*", "Tipo de Contrato*", "Fecha Inicio Contrato*",
                        "Fecha de Terminación de Contrato*", "Regional*", "Centro de Formación*", "Sede de Formación*"
                    ],
                    "download_url": "/api/excel-templates/instructor-template/",
                    "additional_sheets": [
                        "Áreas de Conocimiento", "Tipos de Contrato", "Tipos de Identificación", 
                        "Regionales", "Centros de Formación", "Sedes", "Instrucciones"
                    ]
                },
                "apprentice_template": {
                    "name": "Apprentice Template",
                    "description": "Template for bulk registration of SENA apprentices",
                    "fields": [
                        "Tipo Identificación*", "Número Identificación*", "Primer Nombre*", "Segundo Nombre",
                        "Primer Apellido*", "Segundo Apellido", "Correo Institucional*", "Número de Celular*"
                    ],
                    "download_url": "/api/excel-templates/aprendiz-template/",
                    "additional_sheets": [
                        "Tipos de Identificación", "Instrucciones"
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
            "Processes an Excel file with instructor data for bulk registration. "
            "Created users are automatically activated. "
            "Returns a detailed summary of successful registrations and errors."
        ),
        tags=["Bulk Registration"],
        manual_parameters=[
            openapi.Parameter(
                'file',
                openapi.IN_FORM,
                description="Excel file with instructor data (.xlsx or .xls)",
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
        responses={
            201: openapi.Response(
                "Archivo procesado exitosamente"
            ),
            207: openapi.Response(
                "Procesado parcialmente - algunos registros fallaron"
            ),
            400: openapi.Response("Error en el archivo o datos"),
            500: openapi.Response("Error interno del servidor")
        }
    )
    @action(detail=False, methods=['post'], url_path='upload-instructor-excel', parser_classes=[MultiPartParser, FormParser])
    def upload_instructor_excel(self, request):
        """
        Processes Excel file with instructor data for bulk registration.
        Created users are automatically activated.
        """
        try:
            if 'file' not in request.FILES:
                return Response(
                    {'error': 'No se encontró el archivo en la petición'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            excel_file = request.FILES['file']
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                return Response(
                    {'error': 'El archivo debe ser de formato Excel (.xlsx o .xls)'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            results = self.instructor_service.process_instructor_excel(excel_file)
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
            "Processes an Excel file with apprentice data for bulk registration. "
            "Created users are automatically activated. "
            "Returns a detailed summary of successful registrations and errors."
        ),
        tags=["Bulk Registration"],
        manual_parameters=[
            openapi.Parameter(
                'file',
                openapi.IN_FORM,
                description="Excel file with apprentice data (.xlsx or .xls)",
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
        responses={
            201: openapi.Response(
                "Archivo procesado exitosamente"
            ),
            207: openapi.Response(
                "Procesado parcialmente - algunos registros fallaron"
            ),
            400: openapi.Response("Error en el archivo o datos"),
            500: openapi.Response("Error interno del servidor")
        }
    )
    @action(detail=False, methods=['post'], url_path='upload-aprendiz-excel', parser_classes=[MultiPartParser, FormParser])
    def upload_apprentice_excel(self, request):
        """
        Processes Excel file with apprentice data for bulk registration.
        Created users are automatically activated.
        """
        try:
            if 'file' not in request.FILES:
                return Response(
                    {'error': 'No se encontró el archivo en la petición'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            excel_file = request.FILES['file']
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                return Response(
                    {'error': 'El archivo debe ser de formato Excel (.xlsx o .xls)'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            results = self.apprentice_service.process_apprentice_excel(excel_file)
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