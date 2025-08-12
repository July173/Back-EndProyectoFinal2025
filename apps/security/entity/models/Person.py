from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100, null=True, blank=True)
    first_last_name = models.CharField(max_length=100)
    second_last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    type_identification = models.CharField(max_length=20)
    number_identification = models.CharField(max_length=20)
    delete_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.first_last_name}"
