from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.RoleFormPermissionService import RolFormPermissionService
from apps.security.entity.serializers.RoleFormPermissionSerializer import RolFormPermissionSerializer


class RolFormPermissionViewSet(BaseViewSet):
    service_class = RolFormPermissionService
    serializer_class = RolFormPermissionSerializer
