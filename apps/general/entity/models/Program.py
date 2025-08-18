from django.db import models


class Program(models.Model):
    codeProgram = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    typeProgram = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.codeProgram})"
