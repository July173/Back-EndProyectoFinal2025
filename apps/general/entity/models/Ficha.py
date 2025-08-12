from django.db import models


class Ficha(models.Model):
    numeroFicha = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ficha {self.numeroFicha}"
