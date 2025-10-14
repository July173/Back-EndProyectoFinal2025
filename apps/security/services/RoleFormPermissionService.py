from apps.security.entity.serializers.RolFormPermission.MenuSerializer import MenuSerializer
from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.RoleFormPermissionRepository import RoleFormPermissionRepository
from apps.security.entity.models import Role, Form, Permission, RoleFormPermission


class RoleFormPermissionService(BaseService):
    def __init__(self):
        self.repository = RoleFormPermissionRepository()

    def get_permission_matrix(self):
        roles = Role.objects.all()
        forms = Form.objects.all()
        permissions = Permission.objects.all()
        matrix = []
        for role in roles:
            for form in forms:
                row = {
                    'role': role.type_role,
                    'form': form.name,
                }
                for perm in permissions:
                    exists = RoleFormPermission.objects.filter(role=role, form=form, permission=perm).exists()
                    row[perm.type_permission] = exists
                matrix.append(row)
        return matrix

    def get_menu(self, user_id: int):
        # Calls the repository to get raw data
        menu_data = self.repository.get_menu(user_id)

        # Validation: if there is no menu
        if not menu_data:
            return None

        # Serializes the list of menus with their forms
        serializer = MenuSerializer(menu_data, many=True)
        return serializer.data

    def update_role_with_permissions(self, pk, data):
        role = Role.objects.get(pk=pk)
        role.type_role = data['type_role']
        role.description = data.get('description', '')
        role.active = data.get('active', True)
        role.save()
        # Remove all current permissions for this role
        RoleFormPermission.objects.filter(role=role).delete()
        total_created = 0
        for form_perm in data.get('forms', []):
            form_id = form_perm.get('form_id')
            permission_ids = form_perm.get('permission_ids', [])
            form = Form.objects.get(pk=form_id)
            for perm_id in permission_ids:
                perm = Permission.objects.get(pk=perm_id)
                RoleFormPermission.objects.create(role=role, form=form, permission=perm)
                total_created += 1
        return {
            'role_id': role.id,
            'updated_permissions': total_created
        }

    def create_role_with_permissions(self, data):
        role = Role.objects.create(
            type_role=data['type_role'],
            description=data.get('description', ''),
            active=data.get('active', True)
        )
        total_created = 0
        for form_perm in data.get('forms', []):
            form_id = form_perm.get('form_id')
            permission_ids = form_perm.get('permission_ids', [])
            form = Form.objects.get(pk=form_id)
            for perm_id in permission_ids:
                perm = Permission.objects.get(pk=perm_id)
                RoleFormPermission.objects.create(role=role, form=form, permission=perm)
                total_created += 1
        return {
            'role_id': role.id,
            'created_permissions': total_created
        }


