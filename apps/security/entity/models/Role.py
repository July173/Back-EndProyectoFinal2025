from django.db import models


class Role(models.Model):
    type_role = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.type_role
