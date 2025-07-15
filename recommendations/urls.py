from django.urls import path
from . import views

urlpatterns = [
    # Basic endpoints
    path('recommendations/<int:user_id>/', views.RecommendationsAPIView.as_view(), name='recommendations'),
    path('interaction/', views.InteractionAPIView.as_view(), name='interaction'),
    path('train/', views.TrainModelsAPIView.as_view(), name='train'),
    path('search/', views.ProductSearchAPIView.as_view(), name='search'),
    
    # Enhanced ML endpoints
    path('upload-dataset/', views.DatasetUploadAPIView.as_view(), name='upload_dataset'),
    path('enhanced-train/', views.EnhancedTrainModelsAPIView.as_view(), name='enhanced_train'),
    path('model-metrics/', views.ModelMetricsAPIView.as_view(), name='model_metrics'),
    path('retrain/', views.RetrainModelsAPIView.as_view(), name='retrain'),
    path('enhanced-recommendations/<int:user_id>/', views.EnhancedRecommendationsAPIView.as_view(), name='enhanced_recommendations'),
    path('datasets/', views.DatasetListAPIView.as_view(), name='dataset_list'),
]