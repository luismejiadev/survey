from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Survey App Admin"
admin.site.site_title = "Survey App"
admin.site.index_title = "Welcome to Survey App"

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),
    path('', include('surveys.urls')),
]


if settings.DEBUG:
    # Read: Serving static files during development
    # https://docs.djangoproject.com/en/2.2/howto/static-files/#serving-static-files-during-development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Read: Serving files uploaded by a user during development
    # https://docs.djangoproject.com/en/2.2/howto/static-files/#serving-files-uploaded-by-a-user-during-development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)