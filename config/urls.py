from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import FileResponse
from pathlib import Path

from core.views import HomeView


BASE_DIR = Path(__file__).resolve().parent.parent


def google_verification(request):
    file_path = BASE_DIR / "googlef9b51c033c088346.html"
    return FileResponse(
        open(file_path, "rb"),
        content_type="text/html",
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),

    path(
        'googlef9b51c033c088346.html',
        google_verification,
        name='google-verification',
    ),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Uploaded files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)