from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, Http404
import os

def serve_frontend(request, path='index.html'):
    frontend_dir = os.path.join(settings.BASE_DIR.parent, 'frontend')
    
    # If path points to an actual file (like css/style.css, js/app.js)
    if path and path != 'index.html':
        filepath = os.path.join(frontend_dir, path)
        if os.path.exists(filepath) and os.path.isfile(filepath):
            content_type = 'text/html'
            if path.endswith('.css'):
                content_type = 'text/css'
            elif path.endswith('.js'):
                content_type = 'application/javascript'
            elif path.endswith('.png'):
                content_type = 'image/png'
            elif path.endswith('.jpg') or path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif path.endswith('.svg'):
                content_type = 'image/svg+xml'
            
            with open(filepath, 'rb') as f:
                return HttpResponse(f.read(), content_type=content_type)

    # Fallback to index.html for all SPA routes
    index_path = os.path.join(frontend_dir, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='text/html')
    raise Http404("Frontend index.html not found")

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('users.urls')),
    path('api/services/', include('services.urls')),
    path('api/tickets/', include('tickets.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/notifications/', include('notifications.urls')),
    
    # Frontend SPA Catch-all routes
    path('', lambda req: serve_frontend(req, 'index.html')),
    re_path(r'^(?P<path>.*)$', serve_frontend),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
