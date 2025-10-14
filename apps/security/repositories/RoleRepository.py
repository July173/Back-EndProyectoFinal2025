from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import User, Role
from django.db import transaction


class RoleRepository(BaseRepository):
    """
    Repository for Role model operations.
    """
    def __init__(self):
        super().__init__(Role)

    def get_filtered_roles(self, active=None, search=None):
        """
        Get roles with optional filters for active status and search by type_role.
        """
        queryset = self.model.objects.all()
        if active is not None:
            queryset = queryset.filter(active=active)
        if search:
            queryset = queryset.filter(type_role__icontains=search)
        return list(queryset)

    def list_roles(self):
        """
        Return all roles.
        """
        return self.model.objects.all()

    def set_active_role_and_users(self, role_id, active):
        """
        Activate or deactivate the role and all users linked to that role.
        """
        with transaction.atomic():
            role = Role.objects.get(pk=role_id)
            role.active = active
            role.save()
            users = User.objects.filter(role_id=role_id)
            users.update(is_active=active)
        status_text = "activados" if active else "desactivados"
        return {"detail": f"Rol y usuarios {status_text} correctamente."}  # User-facing message in Spanish

    def roles_with_user_count(self):
        """
        List roles with the count of active users assigned to each role.
        """
        roles = self.model.objects.all()
        data = []
        for role in roles:
            user_count = User.objects.filter(role=role, is_active=True).count()
            data.append({
                "id": role.id,
                "name": role.type_role,
                "description": role.description,
                "active": role.active,
                "user_count": user_count
            })
        return data
    
