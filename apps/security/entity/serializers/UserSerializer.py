from apps.security.entity.models import User
from rest_framework import serializers
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from apps.security.entity.serializers.RoleSerializer import RoleSerializer

class UserSerializer(serializers.ModelSerializer):

    person = PersonSerializer(read_only=True)
    role = RoleSerializer(read_only=True)

 
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'person', 'role', 'is_active', 'registered']
        ref_name = "UserModelSerializer"
       
