from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import User
from apps.security.entity.serializers.User.UserSerializer import UserSerializer
from apps.security.entity.serializers.User.UserSimpleSerializer import UserSimpleSerializer


class UserRepository(BaseRepository):
    """
    Repository for User model operations.
    """
    def __init__(self):
        super().__init__(User)

    def get_queryset(self):
        """
        Include related models to optimize queries.
        """
        return User.objects.select_related('person', 'role')

    def create_user(self, data):
        """
        Create a new User instance using the simple serializer.
        """
        serializer = UserSimpleSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return user, serializer.data, None
        return None, None, serializer.errors

    def delete_user(self, user):
        """
        Delete a User instance.
        """
        user.delete()
    
