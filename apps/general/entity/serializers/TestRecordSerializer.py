from rest_framework import serializers
from apps.general.entity.models import TestRecord


class TestRecordSerializer(serializers.ModelSerializer):
    db = serializers.ChoiceField(
        choices=['default', 'postgresql', 'sqlserver'],
        write_only=True,
        required=False
    )

    class Meta:
        model = TestRecord
        fields = ['id', 'name', 'value', 'db']