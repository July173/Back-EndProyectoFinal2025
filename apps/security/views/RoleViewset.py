from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.RoleService import RoleService
from apps.security.entity.serializers.RoleSerializer import RoleSerializer


class RoleViewSet(BaseViewSet):
    service_class = RoleService
    serializer_class = RoleSerializer
