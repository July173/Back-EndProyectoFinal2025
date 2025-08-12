from django.db import models


class Aprendiz(models.Model):
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Aprendiz {self.id}"
