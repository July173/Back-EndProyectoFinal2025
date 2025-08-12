from .Role import Role
from .Form import Form
from .Permission import Permission
from django.db import models


class RolFormPermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
