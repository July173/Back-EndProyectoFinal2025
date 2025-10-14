from .Form import Form
from .Module import Module
from django.db import models


class FormModule(models.Model):
    class Meta:
        db_table = 'form_module'
    
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
