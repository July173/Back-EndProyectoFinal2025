from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import RoleFormPermission

class RoleFormPermissionRepository(BaseRepository):
    """
    Repository for RoleFormPermission model operations.
    """
    def __init__(self):
        super().__init__(RoleFormPermission)

    def get_menu(self, user_id: int):
        """
        Returns the menu structure for a given user.
        Uses the relationship User -> Role -> RoleFormPermission.
        """
        data = (
            RoleFormPermission.objects
            .filter(role__user__id=user_id, form__formmodule__module_id__active=True)
            .select_related("role", "form__formmodule__module_id", "form")
            .values(
                "role__type_role",                       # role name
                "form__formmodule__module_id__name",     # module name
                "form__name",                            # form name
                "form__path"                             # form path
            )
        )

        result = {}
        for d in data:
            role = d["role__type_role"]
            module = d["form__formmodule__module_id__name"]
            form_name = d["form__name"]
            form_path = d["form__path"]

            if role not in result:
                result[role] = {}

            if module not in result[role]:
                result[role][module] = []

            # avoid duplicates
            if not any(f["name"] == form_name for f in result[role][module]):
                result[role][module].append({
                    "name": form_name,
                    "path": form_path
                })

        # transform to a list of dictionaries as expected by the serializer
        menu = []
        for role, modules in result.items():
            module_forms = [
                {"name": m, "form": forms}
                for m, forms in modules.items()
            ]
            menu.append({
                "rol": role,
                "moduleForm": module_forms
            })

        return menu