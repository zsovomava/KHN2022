from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', include('main.urls')),
    path('', include('accounts.urls')),
    path('', include('groups.urls')),
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('favicon.ico'))),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
