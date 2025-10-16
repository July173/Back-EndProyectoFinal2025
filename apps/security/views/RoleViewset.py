from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.RoleService import RoleService
from apps.security.entity.serializers.RoleSerializer import RoleSerializer
from apps.security.entity.models import Role, User  # Asegúrate de importar User y Role



class RoleViewSet(BaseViewSet):
    @swagger_auto_schema(
        operation_description="Filters roles by status and role name search.",
        tags=["Role"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Role status (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search text (role name)", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de roles filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_roles(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        if active is not None:
            active = active.lower() in ['true', '1', 'yes']
        service = self.service_class()
        try:
            roles = service.get_filtered_roles(active, search)
            serializer = self.get_serializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({"detail": str(ve)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Error inesperado: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    service_class = RoleService
    serializer_class = RoleSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Gets a list of all registered roles."
        ),
        tags=["Role"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Creates a new role with the provided information."
        ),
        tags=["Role"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Gets the information of a specific role."
        ),
        tags=["Role"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Updates the complete information of a role."
        ),
        tags=["Role"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Updates only some fields of a role."
        ),
        tags=["Role"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Physically deletes a role from the database."
        ),
        tags=["Role"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Performs a logical (soft) delete of the specified role."
        ),
        tags=["Role"],
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
        operation_description="Lists roles with assigned user count.",
        tags=["Role"],
        responses={200: openapi.Response("Lista de roles con cantidad de usuarios")}
    )
    @action(detail=False, methods=['get'], url_path='roles-with-user-count')
    def roles_with_user_count(self, request):
        roles = Role.objects.all()
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
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='delete',
        operation_description="Activates if deactivated and deactivates if active the role and all linked users. Only the id is required in the URL.",
        responses={200: openapi.Response('Resultado de la operación')},
        tags=["Role"]
    )
    @action(detail=True, methods=['delete'], url_path='logical-delete-with-users')
    def logical_delete_with_users(self, request, pk=None):
        """
        Activates if deactivated and deactivates if active the role and all linked users. Only the id is required in the URL.
        """
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({'detail': 'Rol no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        new_state = not role.active
        try:
            result = self.service_class().set_active_role_and_users(pk, new_state)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({'detail': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Error inesperado: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
    