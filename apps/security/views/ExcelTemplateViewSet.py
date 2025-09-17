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