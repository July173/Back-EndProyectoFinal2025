from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.UserService import UserService
from apps.security.entity.serializers.UserSerializer import UserSerializer


class UserViewSet(BaseViewSet):
    service_class = UserService
    serializer_class = UserSerializer
