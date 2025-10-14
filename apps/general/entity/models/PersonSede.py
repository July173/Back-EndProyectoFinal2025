from django.db import models


class PersonSede(models.Model):
    sede_id = models.ForeignKey('Sede', on_delete=models.CASCADE)
    person_id = models.ForeignKey('security.Person', on_delete=models.CASCADE)
    delete_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'general_personsede'
        verbose_name = 'Person Sede'
        verbose_name_plural = 'Person Sedes'
