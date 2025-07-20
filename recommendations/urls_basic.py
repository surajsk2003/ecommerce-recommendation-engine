from django.urls import path
from django.http import JsonResponse
from . import views

def api_list(request):
    """List all available API endpoints"""
    endpoints = {
        'message': 'AI E-Commerce Recommendation API',
        'endpoints': {
            'recommendations': '/api/recommendations/<user_id>/',
            'interaction': '/api/interaction/',
            'train': '/api/train/',
            'search': '/api/search/',
            'upload_dataset': '/api/upload-dataset/',
            'enhanced_train': '/api/enhanced-train/',
            'model_metrics': '/api/model-metrics/',
            'retrain': '/api/retrain/',
            'enhanced_recommendations': '/api/enhanced-recommendations/<user_id>/',
            'datasets': '/api/datasets/',
        }
    }
    return JsonResponse(endpoints)

urlpatterns = [
    # API list endpoint
    path('', api_list, name='api_list'),
    
    # Basic endpoints (working without ML dependencies)
    path('recommendations/<int:user_id>/', views.RecommendationsAPIView.as_view(), name='recommendations'),
    path('interaction/', views.InteractionAPIView.as_view(), name='interaction'),
    path('train/', views.TrainModelsAPIView.as_view(), name='train'),
    path('search/', views.ProductSearchAPIView.as_view(), name='search'),
    
    # Enhanced ML endpoints (basic versions)
    path('upload-dataset/', views.DatasetUploadAPIView.as_view(), name='upload_dataset'),
    path('enhanced-train/', views.EnhancedTrainModelsAPIView.as_view(), name='enhanced_train'),
    path('model-metrics/', views.ModelMetricsAPIView.as_view(), name='model_metrics'),
    path('retrain/', views.RetrainModelsAPIView.as_view(), name='retrain'),
    path('enhanced-recommendations/<int:user_id>/', views.EnhancedRecommendationsAPIView.as_view(), name='enhanced_recommendations'),
    path('datasets/', views.DatasetListAPIView.as_view(), name='dataset_list'),
]