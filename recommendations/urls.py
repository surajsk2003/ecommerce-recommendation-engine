from django.urls import path
from . import views
from . import streaming_views
from . import views_advanced

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
    
    # Streaming and real-time endpoints
    path('streaming-event/', streaming_views.StreamingEventAPIView.as_view(), name='streaming_event'),
    path('ab-test/create/', streaming_views.ABTestCreateAPIView.as_view(), name='ab_test_create'),
    path('performance-metrics/', streaming_views.PerformanceMetricsAPIView.as_view(), name='performance_metrics'),
    
    # Next-Generation AI Features
    path('multimodal-recommendations/', views_advanced.MultiModalRecommendationAPIView.as_view(), name='multimodal_recommendations'),
    path('conversational-ai/', views_advanced.ConversationalRecommendationAPIView.as_view(), name='conversational_ai'),
    path('user-persona/', views_advanced.UserPersonaAPIView.as_view(), name='user_persona'),
    path('privacy-compliance/', views_advanced.PrivacyComplianceAPIView.as_view(), name='privacy_compliance'),
    path('advanced-analytics/', views_advanced.AdvancedAnalyticsAPIView.as_view(), name='advanced_analytics'),
    path('voice-recommendations/', views_advanced.VoiceRecommendationAPIView.as_view(), name='voice_recommendations'),
    path('realtime-personalization/', views_advanced.RealtimePersonalizationAPIView.as_view(), name='realtime_personalization'),
]