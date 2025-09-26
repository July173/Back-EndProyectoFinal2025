from django.db import models
from apps.assign.entity.models import AsignationInstructor
from apps.security.entity.models import User

class AsignationInstructorHistory(models.Model):
    def __str__(self):
        return f"Reasignación en {self.asignation_instructor.id} de instructor {self.old_instructor_id} el {self.date}"
    
    asignation_instructor = models.ForeignKey(
        AsignationInstructor, on_delete=models.CASCADE, related_name="history"
    )
    old_instructor_id = models.IntegerField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    