from django.db import models
from apps.assign.entity.models import AsignationInstructor


class VisitFollowing(models.Model):
    visit_number = models.IntegerField()
    observations = models.TextField(null=True, blank=True)
    state_visit = models.CharField(max_length=50)
    scheduled_date = models.DateField()
    date_visit_made = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)
    name_visit = models.CharField(max_length=100)
    observation_state_visit = models.TextField(null=True, blank=True)

    asignation_instructor = models.ForeignKey(
        AsignationInstructor, on_delete=models.CASCADE, related_name='visits'
    )

    def __str__(self):
        return f"Visit {self.id} - {self.name_visit}"
