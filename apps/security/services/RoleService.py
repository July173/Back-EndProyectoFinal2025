# apps/security/services/role_service.py
from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.RoleRepository import RoleRepository



class RoleService(BaseService):
    def __init__(self):
        self.repository = RoleRepository()

    def get_filtered_roles(self, active=None, search=None):
        try:
            roles = self.repository.get_filtered_roles(active, search)
            if not roles.exists():
                raise ValueError("No se encontraron roles con los filtros proporcionados.")
            return roles
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")

    def set_active_role_and_users(self, role_id, active):
        try:
            result = self.repository.set_active_role_and_users(role_id, active)
            if not result:
                raise ValueError("No se pudo cambiar el estado del rol y sus usuarios.")
            return result
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")

    def list_roles(self):
        """
        Delegate listing to the repository.
        """
        return self.repository.list_roles()

    def roles_with_user_count(self):
        """
        Delegate user count to the repository.
        """
        return self.repository.roles_with_user_count()
    