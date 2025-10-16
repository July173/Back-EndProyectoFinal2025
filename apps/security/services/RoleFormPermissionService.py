from apps.security.entity.serializers.RolFormPermission.MenuSerializer import MenuSerializer
from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.RoleFormPermissionRepository import RoleFormPermissionRepository
from apps.security.entity.models import Role, Form, Permission, RoleFormPermission


class RoleFormPermissionService(BaseService):
    def __init__(self):
        self.repository = RoleFormPermissionRepository()

    def get_permission_matrix(self):
        try:
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
            if not matrix:
                raise ValueError("No se encontró matriz de permisos.")
            return matrix
        except Exception as e:
            raise ValueError(f"Error al obtener la matriz de permisos: {str(e)}")

    def get_menu(self, user_id: int):
        try:
            menu_data = self.repository.get_menu(user_id)
            if not menu_data:
                raise ValueError("No se encontró menú para este usuario.")
            serializer = MenuSerializer(menu_data, many=True)
            return serializer.data
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"Error al obtener el menú: {str(e)}")

    def update_role_with_permissions(self, pk, data):
        try:
            role = Role.objects.get(pk=pk)
            role.type_role = data['type_role']
            role.description = data.get('description', '')
            role.active = data.get('active', True)
            role.save()
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
        except Role.DoesNotExist:
            raise ValueError("No se encontró el rol especificado.")
        except Exception as e:
            raise ValueError(f"No se pudo actualizar el rol y sus permisos: {str(e)}")

    def create_role_with_permissions(self, data):
        try:
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
        except Exception as e:
            raise ValueError(f"No se pudo crear el rol y sus permisos: {str(e)}")


