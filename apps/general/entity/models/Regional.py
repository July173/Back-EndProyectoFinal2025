from django.db import models


class Regional(models.Model):
    name = models.CharField(max_length=100)
    codeRegional = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    active = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.codeRegional})"
