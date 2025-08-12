from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.PermissionService import PermissionService
from apps.security.entity.serializers.PermissionSerializer import PermissionSerializer


class PermissionViewSet(BaseViewSet):
    service_class = PermissionService
    serializer_class = PermissionSerializer
