from django.db import models

class DocumentType(models.Model):
    name = models.CharField(max_length=100)
    acronyms = models.CharField(max_length=20)
    image = models.ImageField(upload_to='documentTypeImages/', null=True, blank=True)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name