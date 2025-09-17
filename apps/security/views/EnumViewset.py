from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.security.entity.enums.document_type_enum import DocumentType


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene todos los tipos de documento disponibles en el sistema",
    operation_summary="Lista de tipos de documento",
    tags=["Enums"],
    responses={
        200: openapi.Response(
            description="Lista de tipos de documento exitosa",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'value': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Código del tipo de documento"
                        ),
                        'label': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Descripción del tipo de documento"
                        )
                    }
                )
            ),
            examples={
                'application/json': [
                    {'value': 'CC', 'label': 'Cédula de Ciudadanía'},
                    {'value': 'TI', 'label': 'Tarjeta de Identidad'},
                    {'value': 'CE', 'label': 'Cédula de Extranjería'}
                ]
            }
        )
    }
)
@api_view(['GET'])
def get_document_types(request):
    """
    Endpoint para obtener todos los tipos de documento disponibles.
    Retorna los valores del enum DocumentType en formato adecuado para selects del frontend.
    """
    try:
        document_types = [
            {
                'value': doc_type.name,
                'label': doc_type.value
            }
            for doc_type in DocumentType
        ]
        return Response(document_types, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Error al obtener tipos de documento', 'detalle': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )