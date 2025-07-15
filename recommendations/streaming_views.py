from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .streaming_processor import UserEvent
from .ab_testing import ExperimentConfig
from datetime import datetime
import redis

# Create Redis client
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Import components
from .streaming_processor import RealTimeEventProcessor
from .ab_testing import ABTestingFramework
from .performance_monitor import PerformanceMonitor, RealTimeAnalytics

# Initialize components
streaming_config = {'redis_host': 'localhost', 'redis_port': 6379}
stream_processor = RealTimeEventProcessor(streaming_config)
ab_framework = ABTestingFramework(redis_client, streaming_config)
performance_monitor = PerformanceMonitor(redis_client)
realtime_analytics = RealTimeAnalytics(redis_client)

class StreamingEventAPIView(APIView):
    def post(self, request):
        """Process real-time user events"""
        try:
            event_data = request.data
            
            # Create UserEvent object
            user_event = UserEvent(
                user_id=event_data.get('user_id'),
                product_id=event_data.get('product_id'),
                event_type=event_data.get('event_type'),
                timestamp=datetime.now(),
                session_id=event_data.get('session_id', ''),
                device_type=event_data.get('device_type', 'web'),
                source=event_data.get('source', 'direct'),
                context=event_data.get('context', {}),
                experiment_id=event_data.get('experiment_id'),
                variant=event_data.get('variant')
            )
            
            # Process event
            result = stream_processor.track_event(user_event)
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ABTestCreateAPIView(APIView):
    def post(self, request):
        """Create A/B test experiment"""
        try:
            data = request.data
            
            # Create experiment config
            experiment_config = ExperimentConfig(
                experiment_id=data.get('experiment_id'),
                name=data.get('name'),
                description=data.get('description'),
                variants=data.get('variants'),
                traffic_allocation=data.get('traffic_allocation'),
                start_date=datetime.fromisoformat(data.get('start_date')),
                end_date=datetime.fromisoformat(data.get('end_date')),
                success_metrics=data.get('success_metrics'),
                minimum_sample_size=data.get('minimum_sample_size', 1000)
            )
            
            # Create experiment
            result = ab_framework.create_experiment(experiment_config)
            
            return Response(result, status=status.HTTP_200_OK if result['success'] else status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PerformanceMetricsAPIView(APIView):
    def get(self, request):
        """Get real-time performance metrics"""
        try:
            # Get performance summary
            performance_summary = performance_monitor.get_performance_summary()
            
            # Get real-time analytics
            realtime_metrics = realtime_analytics.get_realtime_metrics()
            
            # Get daily stats
            daily_stats = realtime_analytics.get_daily_stats()
            
            return Response({
                'performance': performance_summary,
                'realtime': realtime_metrics,
                'daily': daily_stats,
                'timestamp': datetime.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)