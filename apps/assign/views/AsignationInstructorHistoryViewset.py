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
    
    def get_service(self):
        return AsignationInstructorHistoryService()

    def get_serializer(self, *args, **kwargs):
        return AsignationInstructorHistorySerializer(*args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Reasigna un instructor y guarda el historial automáticamente.",
        request_body=ReasignationInstructorSerializer,
        tags=["AsignationInstructorHistory"]
    )
    @action(detail=False, methods=['post'], url_path='reasignar-instructor')
    def reasignar_instructor(self, request):
        serializer = ReasignationInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asignation_instructor_id = serializer.validated_data['asignation_instructor_id']
        new_instructor_id = serializer.validated_data['new_instructor_id']
        message = serializer.validated_data['message']
        service = self.get_service()
        try:
            asignation_instructor = service.reasignar_instructor(
                asignation_instructor_id,
                new_instructor_id,
                message
            )
            return Response({"detail": "Reasignación realizada y guardada en historial."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
        operation_description="Obtiene el historial de reasignaciones para una asignación.",
        manual_parameters=[
            openapi.Parameter('asignation_instructor_id', openapi.IN_QUERY, description="ID de la asignación", type=openapi.TYPE_INTEGER)
        ],
        tags=["AsignationInstructorHistory"]
    )
    @action(detail=False, methods=['get'], url_path='list-history')
    def list_history(self, request):
        asignation_instructor_id = request.query_params.get('asignation_instructor_id')
        service = self.get_service()
        history = service.list_by_asignation(asignation_instructor_id)
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

