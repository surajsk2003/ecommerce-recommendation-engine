import time
import threading
from functools import wraps
import logging
from typing import Dict, Any, List
import json
from datetime import datetime

logger = logging.getLogger(__name__)

# Simple metrics tracking without Prometheus dependency
class MetricsCollector:
    def __init__(self):
        self.metrics = {
            'recommendation_requests_total': 0,
            'recommendation_latency_sum': 0.0,
            'recommendation_latency_count': 0,
            'active_users': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'memory_usage_bytes': 0,
            'cpu_usage_percent': 0.0
        }
        self.lock = threading.Lock()
    
    def increment_counter(self, metric_name: str, value: float = 1.0):
        with self.lock:
            self.metrics[metric_name] = self.metrics.get(metric_name, 0) + value
    
    def set_gauge(self, metric_name: str, value: float):
        with self.lock:
            self.metrics[metric_name] = value
    
    def observe_histogram(self, metric_name: str, value: float):
        with self.lock:
            sum_key = f"{metric_name}_sum"
            count_key = f"{metric_name}_count"
            self.metrics[sum_key] = self.metrics.get(sum_key, 0) + value
            self.metrics[count_key] = self.metrics.get(count_key, 0) + 1
    
    def get_metrics(self) -> Dict[str, Any]:
        with self.lock:
            # Calculate averages for histograms
            calculated_metrics = self.metrics.copy()
            
            # Calculate average latency
            if calculated_metrics.get('recommendation_latency_count', 0) > 0:
                calculated_metrics['recommendation_latency_avg'] = (
                    calculated_metrics['recommendation_latency_sum'] / 
                    calculated_metrics['recommendation_latency_count']
                )
            
            # Calculate cache hit rate
            total_cache_requests = calculated_metrics.get('cache_hits', 0) + calculated_metrics.get('cache_misses', 0)
            if total_cache_requests > 0:
                calculated_metrics['cache_hit_rate'] = calculated_metrics.get('cache_hits', 0) / total_cache_requests
            
            return calculated_metrics

class PerformanceMonitor:
    """Real-time performance monitoring"""
    
    def __init__(self, redis_client=None):
        self.redis_client = redis_client
        self.metrics_collector = MetricsCollector()
        
        # Start background monitoring
        threading.Thread(target=self._monitor_system_metrics, daemon=True).start()
    
    def _monitor_system_metrics(self):
        """Monitor system metrics"""
        while True:
            try:
                # Simple system monitoring without psutil dependency
                import os
                
                # Get memory usage (simplified)
                try:
                    with open('/proc/meminfo', 'r') as f:
                        meminfo = f.read()
                        for line in meminfo.split('\n'):
                            if 'MemAvailable:' in line:
                                mem_available = int(line.split()[1]) * 1024  # Convert KB to bytes
                                self.metrics_collector.set_gauge('memory_usage_bytes', mem_available)
                                break
                except:
                    # Fallback for non-Linux systems
                    pass
                
                # Update cache hit rate
                metrics = self.metrics_collector.get_metrics()
                if self.redis_client:
                    # Store metrics in Redis
                    metrics_key = f"performance_metrics:{datetime.now().strftime('%Y%m%d_%H%M')}"
                    self.redis_client.setex(metrics_key, 3600, json.dumps(metrics))
                
            except Exception as e:
                logger.error(f"Error monitoring system metrics: {e}")
            
            time.sleep(10)  # Update every 10 seconds
    
    def track_cache_hit(self):
        """Track cache hit"""
        self.metrics_collector.increment_counter('cache_hits')
    
    def track_cache_miss(self):
        """Track cache miss"""
        self.metrics_collector.increment_counter('cache_misses')
    
    def track_active_user(self, user_id: str):
        """Track active user"""
        if self.redis_client:
            # Use Redis to track unique active users
            active_users_key = f"active_users:{datetime.now().strftime('%Y%m%d_%H')}"
            self.redis_client.sadd(active_users_key, user_id)
            self.redis_client.expire(active_users_key, 3600)  # Expire after 1 hour
            
            # Update gauge
            active_count = self.redis_client.scard(active_users_key)
            self.metrics_collector.set_gauge('active_users', active_count)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        metrics = self.metrics_collector.get_metrics()
        
        return {
            'total_requests': metrics.get('recommendation_requests_total', 0),
            'average_latency_ms': metrics.get('recommendation_latency_avg', 0) * 1000,
            'cache_hit_rate': metrics.get('cache_hit_rate', 0),
            'active_users': metrics.get('active_users', 0),
            'timestamp': datetime.now().isoformat()
        }

def monitor_performance(monitor: PerformanceMonitor):
    """Decorator to monitor function performance"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                monitor.metrics_collector.increment_counter('recommendation_requests_total')
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                monitor.metrics_collector.observe_histogram('recommendation_latency', duration)
        
        return wrapper
    return decorator

class RealTimeAnalytics:
    """Real-time analytics for recommendations"""
    
    def __init__(self, redis_client):
        self.redis_client = redis_client
    
    def track_recommendation_served(self, user_id: str, product_ids: List[str], 
                                  algorithm: str, experiment_id: str = None):
        """Track when recommendations are served"""
        
        event = {
            'user_id': user_id,
            'product_ids': product_ids,
            'algorithm': algorithm,
            'experiment_id': experiment_id,
            'timestamp': datetime.now().isoformat(),
            'event_type': 'recommendation_served'
        }
        
        # Store in Redis stream
        self.redis_client.xadd('recommendation_events', event)
        
        # Update daily counters
        date_key = datetime.now().strftime('%Y%m%d')
        self.redis_client.hincrby(f'daily_stats:{date_key}', 'recommendations_served', 1)
        self.redis_client.hincrby(f'daily_stats:{date_key}', f'algorithm_{algorithm}', 1)
        
        if experiment_id:
            self.redis_client.hincrby(f'daily_stats:{date_key}', f'experiment_{experiment_id}', 1)
    
    def track_recommendation_click(self, user_id: str, product_id: str, 
                                 position: int, experiment_id: str = None):
        """Track when user clicks on recommendation"""
        
        event = {
            'user_id': user_id,
            'product_id': product_id,
            'position': position,
            'experiment_id': experiment_id,
            'timestamp': datetime.now().isoformat(),
            'event_type': 'recommendation_click'
        }
        
        # Store in Redis stream
        self.redis_client.xadd('recommendation_events', event)
        
        # Update daily counters
        date_key = datetime.now().strftime('%Y%m%d')
        self.redis_client.hincrby(f'daily_stats:{date_key}', 'recommendation_clicks', 1)
        
        if experiment_id:
            self.redis_client.hincrby(f'daily_stats:{date_key}', f'clicks_experiment_{experiment_id}', 1)
    
    def get_daily_stats(self, date: str = None) -> Dict[str, Any]:
        """Get daily statistics"""
        
        if not date:
            date = datetime.now().strftime('%Y%m%d')
        
        stats_key = f'daily_stats:{date}'
        raw_stats = self.redis_client.hgetall(stats_key)
        
        # Convert to proper types
        stats = {}
        for key, value in raw_stats.items():
            try:
                stats[key] = int(value)
            except:
                stats[key] = value
        
        # Calculate derived metrics
        recommendations_served = stats.get('recommendations_served', 0)
        recommendation_clicks = stats.get('recommendation_clicks', 0)
        
        if recommendations_served > 0:
            stats['click_through_rate'] = recommendation_clicks / recommendations_served
        else:
            stats['click_through_rate'] = 0
        
        return stats
    
    def get_realtime_metrics(self) -> Dict[str, Any]:
        """Get real-time metrics from the last hour"""
        
        # Get events from the last hour
        end_time = int(time.time() * 1000)
        start_time = end_time - (60 * 60 * 1000)  # 1 hour ago
        
        events = self.redis_client.xrange('recommendation_events', 
                                        min=start_time, max=end_time)
        
        # Process events
        served_count = 0
        click_count = 0
        algorithms = {}
        experiments = {}
        
        for event_id, event_data in events:
            event_type = event_data.get(b'event_type', b'').decode()
            
            if event_type == 'recommendation_served':
                served_count += 1
                algorithm = event_data.get(b'algorithm', b'').decode()
                algorithms[algorithm] = algorithms.get(algorithm, 0) + 1
                
                experiment_id = event_data.get(b'experiment_id', b'').decode()
                if experiment_id:
                    experiments[experiment_id] = experiments.get(experiment_id, 0) + 1
            
            elif event_type == 'recommendation_click':
                click_count += 1
        
        return {
            'recommendations_served_last_hour': served_count,
            'clicks_last_hour': click_count,
            'ctr_last_hour': click_count / served_count if served_count > 0 else 0,
            'algorithms_used': algorithms,
            'active_experiments': experiments,
            'timestamp': datetime.now().isoformat()
        }