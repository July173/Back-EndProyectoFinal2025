from rest_framework import serializers

class PermissionByFormSerializer(serializers.Serializer):
    form_id = serializers.IntegerField()
    permission_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

class RoleFormPermissionCreateSerializer(serializers.Serializer):
    # For POST (creation) we require a role object and disallow role_id.
    # Use the PUT/update endpoint to assign permissions to existing roles via role_id.
    role_id = serializers.IntegerField(required=False)
    role = serializers.DictField(required=False)
    permissions = PermissionByFormSerializer(many=True)

    def validate(self, data):
        # For creation endpoint, require 'role' and do not accept 'role_id'
        if data.get('role_id'):
            raise serializers.ValidationError("'role_id' is not allowed in POST creation. Use the PUT endpoint to modify an existing role.")
        if not data.get('role'):
            raise serializers.ValidationError("Provide 'role' object to create a new role.")
        return data