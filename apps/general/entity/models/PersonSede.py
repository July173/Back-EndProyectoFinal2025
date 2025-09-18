from django.db import models


class PersonSede(models.Model):
    SedeId = models.ForeignKey('Sede', on_delete=models.CASCADE)
    PersonId = models.ForeignKey('security.Person', on_delete=models.CASCADE)
    DeleteAt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'general_personsede'
        verbose_name = 'Person Sede'
        verbose_name_plural = 'Person Sedes'
