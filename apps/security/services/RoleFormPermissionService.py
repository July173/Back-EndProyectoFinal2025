from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.RoleFormPermissionRepository import RolFormPermissionRepository
from apps.security.entity.serializers.MenuSerializer import MenuSerializer


class RolFormPermissionService(BaseService):
    def __init__(self):
        self.repository = RolFormPermissionRepository()


    def get_menu(self, user_id: int):
        # Llama al repository para obtener la data cruda
        menu_data = self.repository.get_menu(user_id)

        # Validación: si no hay menú
        if not menu_data:
            return None

        # Serializa la lista de menús con sus formularios
        serializer = MenuSerializer(menu_data, many=True)
        return serializer.data