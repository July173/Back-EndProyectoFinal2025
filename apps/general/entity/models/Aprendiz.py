from django.db import models
from apps.security.entity.models import Person


class Aprendiz(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='aprendices')
    ficha = models.ForeignKey('Ficha', on_delete=models.CASCADE, related_name='aprendices')
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Aprendiz {self.id}"
