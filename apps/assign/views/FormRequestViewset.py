from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.assign.services.FormRequestService import FormRequestService
from apps.assign.entity.serializers.FormRequestSerializer import FormRequestSerializer


class FormRequestAPIView(APIView):
    """
    ViewSet para manejar solicitudes de formulario.
    Solo expone endpoints POST y GET sin lógica adicional.
    """
    service_class = FormRequestService
    serializer_class = FormRequestSerializer
    
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crear una nueva solicitud de formulario",
        tags=["FormRequest"],
        request_body=FormRequestSerializer,
        responses={
            201: openapi.Response(
                description="Solicitud creada exitosamente",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Solicitud creada exitosamente",
                        "data": {
                            "person": {"id": 1, "full_name": "Juan Pérez"},
                            "aprendiz": {"id": 1, "ficha_id": 2475899},
                            "enterprise": {"id": 1, "name": "Empresa XYZ"},
                            "boss": {"id": 1, "name": "María González"},
                            "human_talent": {"id": 1, "name": "Carlos López"}
                        }
                    }
                }
            ),
            400: "Error en validación de datos"
        }
    )
    def post(self, request, *args, **kwargs):
        """Crear nueva solicitud de formulario"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Error en los datos de entrada',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        result = self.service_class().create_form_request(serializer.validated_data)
        
        if result['success']:
            return Response(result, status=status.HTTP_201_CREATED)
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
                        "data": [
                            {
                                "person": {
                                    "id": 1,
                                    "full_name": "Juan Pérez",
                                    "email": "juan@email.com",
                                    "identification": "1234567890"
                                },
                                "aprendiz": {
                                    "id": 1,
                                    "ficha_id": 2475899,
                                    "programa_formacion": "ADSI"
                                },
                                "enterprise": {
                                    "id": 1,
                                    "name": "Empresa XYZ",
                                    "nit": 900123456
                                }
                            }
                        ]
                    }
                }
            ),
            500: "Error interno del servidor"
        }
    )
    def get(self, request, *args, **kwargs):
        """Obtener lista de solicitudes de formulario"""
        result = self.service_class().list_form_requests()
        
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
