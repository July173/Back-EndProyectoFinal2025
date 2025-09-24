from django.db import models


class Ficha(models.Model):
    file_number = models.BigIntegerField(unique=True)
    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='fichas')
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ficha {self.file_number}"
