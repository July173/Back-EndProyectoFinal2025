from django.db import models


class Sede(models.Model):
    name = models.CharField(max_length=100)
    codeSede = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phoneSede = models.CharField(max_length=20)
    emailContact = models.EmailField(max_length=100)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.codeSede})"
