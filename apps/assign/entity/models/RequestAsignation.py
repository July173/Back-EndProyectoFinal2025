from django.db import models
from apps.general.entity.models import Apprentice
from apps.assign.entity.enums.request_state_enum import RequestState


class RequestAsignation(models.Model):
    apprentice_id = models.ForeignKey(
        Apprentice, on_delete=models.CASCADE, related_name='requests'
    )
    enterprise_id = models.ForeignKey(
        'assign.Enterprise', on_delete=models.CASCADE, related_name='requests'
    )
    modality_productive_stage_id = models.ForeignKey(
        'assign.ModalityProductiveStage', on_delete=models.CASCADE, related_name='requests'
    )
    request_date = models.DateField()
    date_start_production_stage = models.DateField()
    date_end_production_stage = models.DateField()
    pdf_request = models.FileField(upload_to='requests/', null=True, blank=True)
    request_state = models.CharField(
        max_length=50,
        choices=RequestState.choices,
        default=RequestState.SIN_ASIGNAR
    )
    rejection_message= models.TextField(max_length=500, null=True, blank=True)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} - {self.request_state}"
