from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.AsignationInstructorHistoryService import AsignationInstructorHistoryService
from apps.assign.entity.serializers.AsignationInstructorHistorySerializer import AsignationInstructorHistorySerializer

class AsignationInstructorHistoryViewset(BaseViewSet):
    service_class = AsignationInstructorHistoryService
    serializer_class = AsignationInstructorHistorySerializer

    @swagger_auto_schema(
        operation_description="Crea un historial de reasignación de instructor.",
        request_body=AsignationInstructorHistorySerializer,
        tags=["AsignationInstructorHistory"]
    )
    @action(detail=False, methods=['post'], url_path='create-history')
    def create_history(self, request):
        asignation_instructor_id = request.data.get('asignation_instructor')
        old_instructor_id = request.data.get('old_instructor_id')
        message = request.data.get('message', '')
        user = request.user
        service = self.service_class()
        history = service.create_history(
            asignation_instructor=asignation_instructor_id,
            old_instructor_id=old_instructor_id,
            message=message,
            changed_by=user
        )
        serializer = self.serializer_class(history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        service = self.service_class()
        history = service.list_by_asignation(asignation_instructor_id)
        serializer = self.serializer_class(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
