from django.db import models


class TestRecord(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

    def _str_(self):
        return self.name