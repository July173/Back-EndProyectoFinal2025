from django.db import models


class PersonSede(models.Model):

    class Meta:
        db_table = 'person_sede'
    
    sede_id = models.ForeignKey('Sede', on_delete=models.CASCADE)
    person_id = models.ForeignKey('security.Person', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"PersonSede: {self.person_id} - Sede: {self.sede_id}"