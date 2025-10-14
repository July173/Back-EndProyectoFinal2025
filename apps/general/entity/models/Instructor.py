from django.db import models
from apps.security.entity.models import Person
from apps.general.entity.models.KnowledgeArea import KnowledgeArea


class Instructor(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='instructor')  # Relación 1:1
    contractType = models.ForeignKey('TypeContract', on_delete=models.PROTECT, related_name='instructors')
    contractStartDate = models.DateField()
    contractEndDate = models.DateField()
    knowledgeArea = models.ForeignKey(KnowledgeArea, on_delete=models.PROTECT, related_name='instructors')

    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)
    assigned_learners = models.IntegerField(null=True, blank=True)
    max_assigned_learners = models.IntegerField(null=True, blank=True, default=80)
    is_followup_instructor = models.BooleanField(default=False)

    def __str__(self):
        return f"Instructor {self.id} - {self.knowledgeArea.name}"
