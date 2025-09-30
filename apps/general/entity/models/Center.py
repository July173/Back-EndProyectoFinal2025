from django.db import models

class Center(models.Model):
    name = models.CharField(max_length=100)
    codeCenter = models.BigIntegerField()
    address = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)
    regional = models.ForeignKey('Regional', on_delete=models.CASCADE, related_name='centers')

    def __str__(self):
        return f"{self.name} ({self.codeCenter})"
