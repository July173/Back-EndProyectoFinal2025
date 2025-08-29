from django.db import models


class AsignationInstructor(models.Model):
    date_asignation = models.DateField()
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Asignation {self.id} - {self.date_asignation}"
