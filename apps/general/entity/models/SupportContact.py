from django.db import models

class SupportContact(models.Model):
    type = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    extra_info = models.TextField(blank=True, null=True, default=None)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.label}: {self.value} ({self.type})"
