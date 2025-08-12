from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.InstructorService import InstructorService
from apps.general.entity.serializers.InstructorSerializer import InstructorSerializer


class InstructorViewSet(BaseViewSet):
    service_class = InstructorService
    serializer_class = InstructorSerializer
