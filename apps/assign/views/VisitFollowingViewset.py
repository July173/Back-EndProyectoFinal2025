from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from apps.assign.entity.serializers.VisitFollowingSerializer import VisitFollowingSerializer
from apps.assign.services.VisitFollowingService import VisitFollowingService

class VisitFollowingViewset(viewsets.ViewSet):
    """
    ViewSet para listar, obtener por id, crear y actualizar visitas de seguimiento.
    """

    # List all VisitFollowing
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las visitas de seguimiento.",
        tags=["VisitFollowing"],
        responses={200: VisitFollowingSerializer(many=True)}
    )
    def list(self, request):
        queryset = VisitFollowingService().get()
        serializer = VisitFollowingSerializer(queryset, many=True)
        return Response(serializer.data)


    # Retrieve VisitFollowing by id
    @swagger_auto_schema(
        operation_description="Obtiene el detalle de una visita de seguimiento por id.",
        tags=["VisitFollowing"],
        responses={200: VisitFollowingSerializer()}
    )
    def retrieve(self, request, pk=None):
        result = VisitFollowingService().get_by_id(pk)
        if isinstance(result, dict) and result.get('status') == 'error':
            return Response(result.get('detail', 'No encontrado'), status=status.HTTP_404_NOT_FOUND)
        serializer = VisitFollowingSerializer(result)
        return Response(serializer.data)


    # Create a new VisitFollowing
    @swagger_auto_schema(
        operation_description="Crea una nueva visita de seguimiento.",
        request_body=VisitFollowingSerializer,
        tags=["VisitFollowing"],
        responses={201: VisitFollowingSerializer()}
    )
    def create(self, request):
        serializer = VisitFollowingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = VisitFollowingService().create(serializer.validated_data)
        if isinstance(result, dict) and result.get('status') == 'error':
            return Response(result.get('detail', 'Error'), status=status.HTTP_400_BAD_REQUEST)
        out = VisitFollowingSerializer(result)
        return Response(out.data, status=status.HTTP_201_CREATED)


    # Update partially an existing VisitFollowing
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente una visita de seguimiento.",
        request_body=VisitFollowingSerializer,
        tags=["VisitFollowing"],
        responses={200: VisitFollowingSerializer()}
    )
    def partial_update(self, request, pk=None):
        serializer = VisitFollowingSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = VisitFollowingService().update(pk, serializer.validated_data)
        if isinstance(result, dict) and result.get('status') == 'error':
            return Response(result.get('detail', 'No encontrado'), status=status.HTTP_404_NOT_FOUND)
        out = VisitFollowingSerializer(result)
        return Response(out.data, status=status.HTTP_200_OK)
