from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.RoleFormPermissionService import RoleFormPermissionService
from apps.security.entity.serializers.RolFormPermission.RoleFormPermissionSerializer import RoleFormPermissionSerializer
from apps.security.entity.serializers.RolFormPermission.CreateRoleWithPermissionsSerializer import CreateRoleWithPermissionsSerializer



class RoleFormPermissionViewSet(BaseViewSet):
    service_class = RoleFormPermissionService
    serializer_class = RoleFormPermissionSerializer

    @swagger_auto_schema(
        operation_description="Gets the permission matrix by role, form, and permission type.",
        tags=["RoleFormPermission"],
        responses={200: openapi.Response("Matriz de permisos por rol")}
    )
    @action(detail=False, methods=['get'], url_path='permission-matrix')
    def permission_matrix(self, request):
            try:
                matrix = self.service.get_permission_matrix()
                return Response(matrix, status=status.HTTP_200_OK)
            except ValueError as ve:
                return Response({'detail': str(ve)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'detail': f'Error inesperado: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='get',
        operation_description="Gets a role with its assigned forms and permissions by ID.",
        tags=["RoleFormPermission"],
        responses={200: CreateRoleWithPermissionsSerializer}
    )
    @action(detail=True, methods=['get'], url_path='get-role-with-permissions')
    def get_role_with_permissions(self, request, pk=None):
        from apps.security.entity.models import Role, RolFormPermission
        from apps.security.entity.serializers.RolFormPermission.CreateRoleWithPermissionsSerializer import CreateRoleWithPermissionsSerializer
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({'detail': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)
        rfp_qs = RolFormPermission.objects.filter(role=role)
        form_map = {}
        for rfp in rfp_qs:
            form_id = rfp.form.id
            if form_id not in form_map:
                form_map[form_id] = {'form_id': form_id, 'permission_ids': []}
            form_map[form_id]['permission_ids'].append(rfp.permission.id)
        data = {
            'type_role': role.type_role,
            'description': role.description,
            'active': role.active,
            'forms': list(form_map.values())
        }
        serializer = CreateRoleWithPermissionsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='put',
        request_body=CreateRoleWithPermissionsSerializer,
        operation_description="Updates a role and its permissions by form.",
        tags=["RoleFormPermission"],
        responses={200: openapi.Response("Rol y permisos actualizados correctamente.")}
    )
    @action(detail=True, methods=['put'], url_path='update-role-with-permissions')
    def update_role_with_permissions(self, request, pk=None):
        serializer = CreateRoleWithPermissionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.service.update_role_with_permissions(pk, serializer.validated_data)
        return Response(result, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='post',
        request_body=CreateRoleWithPermissionsSerializer,
        operation_description="Creates a new role and assigns one or more permissions to one or more forms.",
        tags=["RoleFormPermission"],
        responses={201: openapi.Response("Rol y permisos creados correctamente.")}
    )
    @action(detail=False, methods=['post'], url_path='create-role-with-permissions')
    def create_role_with_permissions(self, request):
        serializer = CreateRoleWithPermissionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.service.create_role_with_permissions(serializer.validated_data)
        return Response(result, status=status.HTTP_201_CREATED)

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Gets a list of all registered form permissions by role."
        ),
        tags=["RoleFormPermission"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        request_body=RoleFormPermissionSerializer,
        operation_description="Creates a new form permission for a role.",
        tags=["RoleFormPermission"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Gets the information of a specific form permission by role."
        ),
        tags=["RoleFormPermission"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Updates the complete information of a form permission by role."
        ),
        tags=["RoleFormPermission"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Updates only some fields of a form permission by role."
        ),
        tags=["RoleFormPermission"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Physically deletes a form permission by role from the database."
        ),
        tags=["RoleFormPermission"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Performs a logical (soft) delete of the specified form permission by role."
        ),
        tags=["RoleFormPermission"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
            try:
                deleted = self.service_class().soft_delete(pk)
                if deleted:
                    return Response({"detail": "Eliminado lógicamente correctamente."}, status=status.HTTP_204_NO_CONTENT)
                return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
            except ValueError as ve:
                return Response({"detail": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"detail": f"Error inesperado: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Gets the menu for the specified user.",
        tags=["RoleFormPermission"],
        responses={
            200: openapi.Response("Menú obtenido correctamente."),
            404: openapi.Response("No se encontró menú para este usuario.")
        }
    )
    @action(detail=True, methods=['get'], url_path='get-menu')
    def get_menu(self, request, pk=None):
        menu = self.service.get_menu(pk)
        if not menu:
            return Response(
                {"detail": "No menu found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(menu, status=status.HTTP_200_OK)
