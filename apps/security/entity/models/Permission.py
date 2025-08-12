from django.db import models


class Permission(models.Model):
    type_permission = models.CharField(max_length=50)
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.type_permission
