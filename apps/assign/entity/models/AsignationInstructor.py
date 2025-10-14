from django.db import models
from apps.general.entity.models import Instructor


class AsignationInstructor(models.Model):
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="asignations")
    request_asignation_id = models.OneToOneField('assign.RequestAsignation', on_delete=models.CASCADE, related_name="asignation_instructor")
    date_asignation = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Asignation {self.id} - {self.date_asignation}"
