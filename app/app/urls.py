from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # ============= Accounts URL's ============= #
    path('accounts/api/v1/', include('accounts.apis.v1.urls')),
    path('', include('accounts.urls')),

    # ============= Notes URL's ============= #
    path('notes/api/v1/', include('note.apis.v1.urls')),
    path('notes/', include('note.urls')),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('silk/', include('silk.urls', namespace='silk'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
