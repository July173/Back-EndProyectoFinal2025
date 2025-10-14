from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:
    """
    Service for authentication operations.
    """
    def login(self, email, password):
        user = authenticate(email=email, password=password)
        if not user:
            return None
        refresh = RefreshToken.for_user(user)
        # Get the person field, assuming user.person exists
        person = None
        if hasattr(user, 'person'):
            # If it's a relation, you can serialize the object or just the id
            try:
                person = user.person.id
            except Exception:
                person = None
                print('user:', user, 'person:', person)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role.id if hasattr(user, 'role') else None,
                'person': person
            }
        }
    