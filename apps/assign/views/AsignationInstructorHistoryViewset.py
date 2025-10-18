from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from apps.assign.services.AsignationInstructorHistoryService import AsignationInstructorHistoryService
from apps.assign.entity.serializers.AsignationInstructor.AsignationInstructorHistorySerializer import AsignationInstructorHistorySerializer
from apps.assign.entity.serializers.AsignationInstructor.ReasignationInstructorSerializer import ReasignationInstructorSerializer



class AsignationInstructorHistoryViewset(ViewSet):
    """
    ViewSet for managing instructor reassignment history.
    All internal code and comments are in English. User-facing messages and API documentation remain in Spanish.
    """

    def get_service(self):
        """Return the service instance for instructor history operations."""
        return AsignationInstructorHistoryService()

    def get_serializer(self, *args, **kwargs):
        """Return the serializer for instructor history objects."""
        return AsignationInstructorHistorySerializer(*args, **kwargs)


    # Create reassignment and save history
    @swagger_auto_schema(
        operation_description="Reasigna un instructor y guarda el historial automáticamente.",
        request_body=ReasignationInstructorSerializer,
        tags=["AsignationInstructorHistory"],
        responses={
            200: openapi.Response("Reasignación realizada correctamente."),
            400: openapi.Response("Error: {'status': 'error', 'type': 'not_found', 'message': 'No existe la asignación'}")
        }
    )
    @action(detail=False, methods=['post'], url_path='reasignar-instructor')
    def reasignar_instructor(self, request):
        """
        Reassign an instructor and automatically save the history.
        """
        serializer = ReasignationInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asignation_instructor_id = serializer.validated_data['asignation_instructor_id']
        new_instructor_id = serializer.validated_data['new_instructor_id']
        message = serializer.validated_data['message']
        service = self.get_service()
        result = service.reasignar_instructor(
            asignation_instructor_id,
            new_instructor_id,
            message
        )
        if isinstance(result, dict) and result.get('status') == 'error':
            # Return error response in Spanish as required
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        # Success message in Spanish for user-facing response
        return Response({"detail": "Reasignación realizada y guardada en historial."}, status=status.HTTP_200_OK)


    # List All history AsignationInstructor
    @swagger_auto_schema(
        operation_description="Obtiene el historial de reasignaciones para una asignación.",
        manual_parameters=[
            openapi.Parameter('asignation_instructor_id', openapi.IN_QUERY, description="ID de la asignación", type=openapi.TYPE_INTEGER)
        ],
        tags=["AsignationInstructorHistory"],
        responses={
            200: openapi.Response("Historial obtenido correctamente."),
            400: openapi.Response("Error: {'status': 'error', 'type': 'list_by_asignation', 'message': 'No se pudo obtener el historial: ...'}")
        }
    )
    @action(detail=False, methods=['get'], url_path='list-history')
    def list_history(self, request):
        """
        Get the reassignment history for a given instructor assignment.
        """
        asignation_instructor_id = request.query_params.get('asignation_instructor_id')
        service = self.get_service()
        history = service.list_by_asignation(asignation_instructor_id)
        if isinstance(history, dict) and history.get('status') == 'error':
            # Return error response in Spanish as required
            return Response(history, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # Retrieve history by ID
    @swagger_auto_schema(
        operation_description="Obtiene el historial de reasignación por id.",
        tags=["AsignationInstructorHistory"],
        responses={
            200: AsignationInstructorHistorySerializer(),
            404: "No existe el historial."
        }
    )
    def retrieve(self, request, pk=None):
        """
        Get reassignment history by id.
        """
        service = self.get_service()
        result = service.get_by_id(pk)
        if isinstance(result, dict) and result.get('status') == 'error':
            return Response(result.get('detail', 'No encontrado'), status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
