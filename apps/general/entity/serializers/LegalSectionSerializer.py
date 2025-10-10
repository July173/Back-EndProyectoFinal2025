from rest_framework import serializers
from apps.general.entity.models.LegalSection import LegalSection

class LegalSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalSection
        fields = ['id', 'documentId', 'parentId', 'order', 'code', 'title', 'content', 'active']