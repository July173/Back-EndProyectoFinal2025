from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.general.entity.serializers.TestRecordSerializer import TestRecordSerializer
from apps.general.services.TestRecordService import TestRecordService


db_param = openapi.Parameter(
    'db',
    openapi.IN_QUERY,
    description="Base de datos: default, postgresql o sqlserver",
    type=openapi.TYPE_STRING,
    required=False,
    enum=['default', 'postgresql', 'sqlserver']
)


class TestRecordMultiDBViewset(ViewSet):
    serializer_class = TestRecordSerializer
    service = TestRecordService()

    @swagger_auto_schema(
        manual_parameters=[db_param],
        responses={200: TestRecordSerializer(many=True)}
    )
    def list(self, request):
        db = request.query_params.get('db', 'default')
        queryset = self.service.list(db=db)
        serializer = TestRecordSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=TestRecordSerializer,
        responses={201: TestRecordSerializer()}
    )
    def create(self, request):
        db = request.data.get('db', 'default')
        serializer = TestRecordSerializer(data=request.data)
        if serializer.is_valid():
            obj = self.service.create(serializer.validated_data, db=db)
            response_serializer = TestRecordSerializer(obj)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[db_param],
        responses={200: TestRecordSerializer()}
    )
    def retrieve(self, request, pk=None):
        db = request.query_params.get('db', 'default')
        obj = self.service.retrieve(pk, db=db)
        serializer = TestRecordSerializer(obj)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=TestRecordSerializer,
        responses={200: TestRecordSerializer()}
    )
    def update(self, request, pk=None):
        db = request.data.get('db', 'default')
        serializer = TestRecordSerializer(data=request.data)
        if serializer.is_valid():
            obj = self.service.update(pk, serializer.validated_data, db=db)
            response_serializer = TestRecordSerializer(obj)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[db_param]
    )
    def destroy(self, request, pk=None):
        db = request.query_params.get('db', 'default')
        self.service.delete(pk, db=db)
        return Response(status=status.HTTP_204_NO_CONTENT)