from django.db import models
from apps.security.entity.models import Person


class Apprentice(models.Model):
    
    class Meta:
        db_table = 'apprentice'
    
    person_id = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='apprentice')
    ficha_id = models.ForeignKey('Ficha', on_delete=models.CASCADE, related_name='aprendices', null=True, blank=True)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Aprendiz {self.id}"
