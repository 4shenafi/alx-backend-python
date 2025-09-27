from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from messaging_app.chats import auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # all API endpoints under /api/
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]


urlpatterns = [
    # JWT endpoints
    path("api/token/", auth.token_obtain_pair, name="token_obtain_pair"),
    path("api/token/refresh/", auth.token_refresh, name="token_refresh"),

    # Your app routes
    path("api/chats/", include("messaging_app.chats.urls")),
]

# For production, ensure proper handling of static and media files via web server

# and consider security best practices.

# End of file
