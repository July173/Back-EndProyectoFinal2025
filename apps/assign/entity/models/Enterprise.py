from django.db import models


class Enterprise(models.Model):
    name_enterprise = models.CharField(max_length=100)
    locate = models.CharField(max_length=255)
    nit_enterprise = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    email_enterprise = models.EmailField(max_length=100)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name_enterprise
