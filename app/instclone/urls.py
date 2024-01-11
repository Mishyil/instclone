from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
	path('', include('main.urls')),
	path('content/', include('content.urls')),
	path('admin/', admin.site.urls),
	path('notifications/', include('notifications.urls')),
    path('explore/', include('explore.urls')),
	path('p/<int:pk>/', include('userpost.urls')),
    path('tools/', include('tools.urls')),
    path('api/v1/', include('api.urls')),
	path('<str:username>/', include('userprofile.urls')),
]

if settings.DEBUG:
    import debug_toolbar	

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)