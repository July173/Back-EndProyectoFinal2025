# apps/security/services/role_service.py
from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.RoleRepository import RoleRepository


class RoleService(BaseService):
    def set_active_role_and_users(self, role_id, active):
        """
        Activa o desactiva el rol y todos los usuarios vinculados a ese rol.
        """
        from apps.security.entity.models import User, Role
        from django.db import transaction
        with transaction.atomic():
            role = Role.objects.get(pk=role_id)
            role.active = active
            role.save()
            users = User.objects.filter(role_id=role_id)
            users.update(is_active=active)
        estado = "activados" if active else "desactivados"
        return {"detail": f"Rol y usuarios {estado} correctamente."}
   
    def __init__(self):
        self.repository = RoleRepository()
