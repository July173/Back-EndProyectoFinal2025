from django.db import models


class HumanTalent(models.Model):
    enterprise_id = models.OneToOneField(
        'assign.Enterprise', on_delete=models.CASCADE, related_name='human_talent'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.BigIntegerField()
    active = models.BooleanField(default=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
