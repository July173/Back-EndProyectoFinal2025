from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import User
from apps.security.entity.serializers.UserSerializer import UserSerializer


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def create_user(self, data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return user, serializer.data, None
        return None, None, serializer.errors

    def delete_user(self, user):
        user.delete()
    
