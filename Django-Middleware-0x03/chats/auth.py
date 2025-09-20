# chats/auth.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that includes additional user validation
    """
    
    def authenticate(self, request):
        try:
            # Get the parent's authentication result
            auth_result = super().authenticate(request)
            if auth_result is None:
                return None
                
            user, token = auth_result
            
            # Add any additional user validation here
            if not user.is_active:
                raise AuthenticationFailed('User is not active')
                
            return (user, token)
            
        except Exception as e:
            raise AuthenticationFailed(str(e))
