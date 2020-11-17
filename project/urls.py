from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
# import service_settings


def ping_view(request):
    return JsonResponse(dict(code='OK'))


urlpatterns = [
    path('ping', ping_view),
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('api/', include('service.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        'media/', document_root=settings.MEDIA_ROOT
    )
