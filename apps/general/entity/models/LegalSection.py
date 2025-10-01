from django.db import models
from .LegalDocument import LegalDocument

class LegalSection(models.Model):
    documentId = models.OneToOneField(LegalDocument, on_delete=models.CASCADE, related_name='section')
    parentId = models.OneToOneField('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child')
    order = models.IntegerField()
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.title}"