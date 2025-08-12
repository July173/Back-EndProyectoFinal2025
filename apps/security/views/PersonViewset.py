from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.PersonService import PersonService
from apps.security.entity.serializers.PersonSerializer import PersonSerializer


class PersonViewSet(BaseViewSet):
    service_class = PersonService
    serializer_class = PersonSerializer
