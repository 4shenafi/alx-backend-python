from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# These can be used in urls.py
token_obtain_pair = TokenObtainPairView.as_view()
token_refresh = TokenRefreshView.as_view()
# to provide JWT authentication endpoints.
# You can include these views in your URL patterns to enable JWT authentication.
