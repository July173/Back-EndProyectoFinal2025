from rest_framework import serializers
from apps.general.entity.models.SupportContact import SupportContact

class SupportContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportContact
        fields = '__all__'
