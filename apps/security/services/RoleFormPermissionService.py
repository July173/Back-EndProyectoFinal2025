from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.RoleFormPermissionRepository import RolFormPermissionRepository
from apps.security.entity.serializers.MenuSerializer import MenuSerializer
from django.db import transaction
from apps.security.entity.models import Role, Form, Permission, RolFormPermission


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

    def create_permissions_for_role(self, validated_data: dict):
        """Create a new Role and assign permissions per form.

        This endpoint is POST-only: it requires a `role` dict and does not accept `role_id`.

        validated_data format:
        {
            'role': { 'type_role': str, 'description': str, 'active': bool },
            'permissions': [ { 'form_id': int, 'permission_ids': [int, ...] } ]
        }
        """
        role_data = validated_data.get('role')
        permissions = validated_data.get('permissions', [])

        with transaction.atomic():
            # Disallow role_id in POST create
            if validated_data.get('role_id'):
                raise ValueError("'role_id' is not allowed in POST creation. Use PUT to modify an existing role.")

            if not role_data:
                raise ValueError("No role data provided to create")

            role = Role.objects.create(**role_data)

            to_create = []
            created_count = 0
            for item in permissions:
                form = Form.objects.filter(pk=item['form_id']).first()
                if not form:
                    raise ValueError(f"Form with id {item['form_id']} not found")
                for perm_id in item['permission_ids']:
                    perm = Permission.objects.filter(pk=perm_id).first()
                    if not perm:
                        raise ValueError(f"Permission with id {perm_id} not found")
                    # avoid duplicates
                    exists = RolFormPermission.objects.filter(role=role, form=form, permission=perm).exists()
                    if not exists:
                        to_create.append(RolFormPermission(role=role, form=form, permission=perm))
                        created_count += 1

            if to_create:
                RolFormPermission.objects.bulk_create(to_create)

            return {
                'role_id': role.id,
                'created_permissions': created_count
            }