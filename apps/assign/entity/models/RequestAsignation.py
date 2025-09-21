from django.db import models
from apps.general.entity.models import Aprendiz


class RequestAsignation(models.Model):
    aprendiz = models.ForeignKey(
        Aprendiz, on_delete=models.CASCADE, related_name='requests'
    )
    enterprise = models.ForeignKey(
        'assign.Enterprise', on_delete=models.CASCADE, related_name='requests'
    )
    modality_productive_stage = models.ForeignKey(
        'assign.ModalityProductiveStage', on_delete=models.CASCADE, related_name='requests'
    )
    request_date = models.DateField()
    date_start_production_stage = models.DateField()
    date_end_production_stage = models.DateField()
    pdf_request = models.FileField(upload_to='requests/', null=True, blank=True)
    request_state = models.CharField(max_length=50)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} - {self.request_state}"
