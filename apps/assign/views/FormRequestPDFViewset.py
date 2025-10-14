from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.assign.services.FormRequestPDFService import FormRequestService
from apps.assign.entity.serializers.form.FormPDFSerializer import FormPDFSerializer
   


class FormRequestPDFAPIView(APIView):
    """
    POST endpoint for uploading PDF files to a form request.
    All internal code, comments, and docstrings are in English. User-facing error messages and API documentation remain in Spanish.
    """
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=["FormRequest PDF"],
        manual_parameters=[
            openapi.Parameter('pdf_file', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
            openapi.Parameter('request_id', openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True)
        ],
        consumes=['multipart/form-data']
    )
    def post(self, request):
        """
        Upload a PDF to an existing form request.
        API documentation and user-facing messages remain in Spanish.
        """
        request_id = request.data.get('request_id')

        if not request_id:
            # Error message in Spanish for user-facing response
            return Response({'error': 'request_id requerido'}, status=400)

        serializer = FormPDFSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        result = FormRequestService().upload_pdf_to_request(int(request_id), serializer.validated_data)

        return Response(result, status=200 if result['success'] else 400)
