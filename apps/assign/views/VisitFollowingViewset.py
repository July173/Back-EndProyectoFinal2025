from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from apps.assign.entity.serializers.VisitFollowingSerializer import VisitFollowingSerializer
from apps.assign.services.VisitFollowingService import VisitFollowingService

class VisitFollowingViewset(APIView):
    """
    APIView for listing visit following records only.
    """
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las visitas de seguimiento.",
        tags=["VisitFollowing"]
    )
    def get(self, request, *args, **kwargs):
        """Return a list of all visit following records."""
        queryset = VisitFollowingService().get()
        serializer = VisitFollowingSerializer(queryset, many=True)
        return Response(serializer.data)
