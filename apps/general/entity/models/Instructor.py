from django.db import models


class Instructor(models.Model):
    contractType = models.CharField(max_length=50)
    contractStartDate = models.DateField()
    contractEndDate = models.DateField()
    knowledgeArea = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Instructor {self.id} - {self.knowledgeArea}"
