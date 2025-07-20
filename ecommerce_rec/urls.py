from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def health_check(request):
    """Health check endpoint for Railway"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'AI E-Commerce API is running',
        'version': '1.0.0'
    })

urlpatterns = [
    path('', health_check, name='health_check'),  # Root health check
    path('health/', health_check, name='health'),  # Alternative health check
    path('admin/', admin.site.urls),
    path('api/', include('recommendations.urls_basic')),
]