from django.db import models
from apps.security.entity.models import Person


class Instructor(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='instructores')  # <-- Relación agregada
    contractType = models.CharField(max_length=50)
    contractStartDate = models.DateField()
    contractEndDate = models.DateField()
    knowledgeArea = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Instructor {self.id} - {self.knowledgeArea}"
