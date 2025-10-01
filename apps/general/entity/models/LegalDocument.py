from django.db import models

class LegalDocument(models.Model):
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    effective_date = models.DateField()
    last_update = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.type})"
