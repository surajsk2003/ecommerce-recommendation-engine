from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.conf import settings
try:
    from .recommendation_engine import RecommendationEngine
except ImportError:
    # Fallback to simple engine if ML dependencies not available
    from .simple_engine import RecommendationEngine
try:
    from .enhanced_engine import EnhancedRecommendationEngine
    from .streaming_processor import RealTimeEventProcessor, UserEvent
    from .ab_testing import ABTestingFramework, ExperimentConfig, ExperimentStatus
    from .performance_monitor import PerformanceMonitor, RealTimeAnalytics
except ImportError:
    # Create dummy classes for missing ML components
    class EnhancedRecommendationEngine:
        pass
    class RealTimeEventProcessor:
        pass
    class UserEvent:
        pass
    class ABTestingFramework:
        pass
    class ExperimentConfig:
        pass
    class ExperimentStatus:
        pass
    class PerformanceMonitor:
        pass
    class RealTimeAnalytics:
        pass
from .models import UserBehavior, Product, DatasetUpload, ModelTraining
import logging
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

recommendation_engine = RecommendationEngine()
enhanced_engine = EnhancedRecommendationEngine()

# Initialize streaming and A/B testing components
streaming_config = {
    'redis_host': 'localhost',
    'redis_port': 6379
}

# Create Redis client
import redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

try:
    stream_processor = RealTimeEventProcessor(streaming_config)
    ab_framework = ABTestingFramework(redis_client, streaming_config)
    performance_monitor = PerformanceMonitor(redis_client)
    realtime_analytics = RealTimeAnalytics(redis_client)
except:
    # Use dummy instances if initialization fails
    stream_processor = RealTimeEventProcessor()
    ab_framework = ABTestingFramework()
    performance_monitor = PerformanceMonitor()
    realtime_analytics = RealTimeAnalytics()

class RecommendationsAPIView(APIView):
    def get(self, request, user_id):
        """Get personalized recommendations for user"""
        try:
            user = get_object_or_404(User, id=user_id)
            num_recommendations = int(request.query_params.get('count', 10))
            
            recommendations = recommendation_engine.get_recommendations(
                user_id=user_id,
                num_recommendations=num_recommendations
            )
            
            return Response({
                'user_id': user_id,
                'recommendations': recommendations,
                'count': len(recommendations)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in recommendations API: {str(e)}")
            return Response({
                'error': 'Failed to get recommendations'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InteractionAPIView(APIView):
    def post(self, request):
        """Record user interaction"""
        try:
            user_id = request.data.get('user_id')
            product_id = request.data.get('product_id')
            interaction_type = request.data.get('interaction_type')
            
            if not all([user_id, product_id, interaction_type]):
                return Response({
                    'error': 'Missing required fields'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = get_object_or_404(User, id=user_id)
            product = get_object_or_404(Product, id=product_id)
            
            recommendation_engine.record_interaction(
                user_id=user_id,
                product_id=product_id,
                interaction_type=interaction_type
            )
            
            return Response({
                'message': 'Interaction recorded successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error recording interaction: {str(e)}")
            return Response({
                'error': 'Failed to record interaction'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TrainModelsAPIView(APIView):
    def post(self, request):
        """Trigger basic model training"""
        try:
            success = recommendation_engine.train_models()
            
            if success:
                return Response({
                    'message': 'Basic models trained successfully'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Failed to train models'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error training models: {str(e)}")
            return Response({
                'error': 'Failed to train models'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductSearchAPIView(APIView):
    def get(self, request):
        """Search products with recommendations"""
        try:
            query = request.query_params.get('q', '')
            user_id = request.query_params.get('user_id')
            
            products = Product.objects.filter(
                name__icontains=query
            )[:20]
            
            results = []
            for product in products:
                product_data = {
                    'id': product.id,
                    'name': product.name,
                    'category': product.category,
                    'price': float(product.price),
                    'description': product.description
                }
                
                if user_id:
                    try:
                        cf_score = recommendation_engine.cf_model.predict_user_preferences(
                            int(user_id), [product.id]
                        )[0]
                        product_data['personalization_score'] = float(cf_score)
                    except:
                        product_data['personalization_score'] = 0.5
                
                results.append(product_data)
            
            if user_id:
                results.sort(key=lambda x: x.get('personalization_score', 0), reverse=True)
            
            return Response({
                'products': results,
                'count': len(results)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in product search: {str(e)}")
            return Response({
                'error': 'Search failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DatasetUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        """Upload dataset for training"""
        try:
            uploaded_file = request.FILES.get('file')
            dataset_type = request.data.get('dataset_type')
            user_id = request.data.get('user_id', 1)
            
            if not uploaded_file:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not dataset_type:
                return Response({'error': 'Dataset type required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Save file
            file_path = default_storage.save(
                f'datasets/{dataset_type}_{uploaded_file.name}',
                uploaded_file
            )
            
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            # Process dataset
            result = enhanced_engine.upload_dataset(full_path, dataset_type, user_id)
            
            return Response(result, status=status.HTTP_200_OK if result['success'] else status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EnhancedTrainModelsAPIView(APIView):
    def post(self, request):
        """Train models on uploaded data"""
        try:
            dataset_ids = request.data.get('dataset_ids', [])
            config = request.data.get('config', {})
            
            if not dataset_ids:
                return Response({'error': 'Dataset IDs required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Start training
            result = enhanced_engine.train_on_uploaded_data(dataset_ids, config)
            
            return Response(result, status=status.HTTP_200_OK if result['success'] else status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ModelMetricsAPIView(APIView):
    def get(self, request):
        """Get model metrics and performance"""
        try:
            metrics = enhanced_engine.get_model_metrics()
            
            return Response(metrics, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RetrainModelsAPIView(APIView):
    def post(self, request):
        """Retrain models with new data"""
        try:
            incremental = request.data.get('incremental', True)
            
            result = enhanced_engine.retrain_with_new_data(incremental)
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EnhancedRecommendationsAPIView(APIView):
    def get(self, request, user_id):
        """Get enhanced recommendations"""
        try:
            user = get_object_or_404(User, id=user_id)
            num_recommendations = int(request.query_params.get('count', 10))
            
            recommendations = enhanced_engine.get_recommendations(user_id, num_recommendations)
            
            return Response({
                'user_id': user_id,
                'recommendations': recommendations,
                'count': len(recommendations),
                'algorithm': 'hybrid_ensemble' if enhanced_engine.is_trained else 'popularity_fallback'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DatasetListAPIView(APIView):
    def get(self, request):
        """List uploaded datasets"""
        try:
            datasets = DatasetUpload.objects.filter(is_active=True).order_by('-uploaded_at')
            
            dataset_list = []
            for dataset in datasets:
                dataset_list.append({
                    'id': dataset.id,
                    'type': dataset.dataset_type,
                    'uploaded_at': dataset.uploaded_at.isoformat(),
                    'metadata': dataset.metadata
                })
            
            return Response({
                'datasets': dataset_list,
                'count': len(dataset_list)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)