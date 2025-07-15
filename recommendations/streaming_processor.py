import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import redis
import threading
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict, deque
import hashlib
import uuid

logger = logging.getLogger(__name__)

@dataclass
class UserEvent:
    """Real-time user event data structure"""
    user_id: str
    product_id: str
    event_type: str  # view, click, cart, purchase, etc.
    timestamp: datetime
    session_id: str
    device_type: str
    source: str
    context: Dict[str, Any]
    experiment_id: Optional[str] = None
    variant: Optional[str] = None

class RealTimeEventProcessor:
    """Process real-time user events for immediate recommendations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.redis_client = redis.Redis(
            host=config.get('redis_host', 'localhost'),
            port=config.get('redis_port', 6379),
            decode_responses=True
        )
        
        # Event buffers
        self.event_buffer = deque(maxlen=10000)
        self.user_sessions = defaultdict(lambda: deque(maxlen=100))
        self.trending_items = defaultdict(int)
        
        # Start background processors
        self.start_background_tasks()
    
    def start_background_tasks(self):
        """Start background processing tasks"""
        threading.Thread(target=self._update_trending_items, daemon=True).start()
        threading.Thread(target=self._cleanup_old_sessions, daemon=True).start()
    
    def track_event(self, event: UserEvent) -> Dict[str, Any]:
        """Track a single user event"""
        
        # Convert to dict for processing
        event_dict = {
            'user_id': event.user_id,
            'product_id': event.product_id,
            'event_type': event.event_type,
            'timestamp': event.timestamp.isoformat(),
            'session_id': event.session_id,
            'device_type': event.device_type,
            'source': event.source,
            'context': event.context,
            'experiment_id': event.experiment_id,
            'variant': event.variant
        }
        
        # Add to buffer
        self.event_buffer.append(event_dict)
        
        # Update user session
        self.user_sessions[event.user_id].append(event_dict)
        
        # Update Redis cache
        self._update_user_cache(event)
        
        # Update trending items
        if event.event_type in ['view', 'click', 'purchase']:
            self.trending_items[event.product_id] += 1
        
        # Generate real-time recommendations
        recommendations = self._generate_realtime_recommendations(event.user_id)
        
        return {
            'event_processed': True,
            'timestamp': datetime.now().isoformat(),
            'recommendations': recommendations
        }
    
    def _generate_realtime_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """Generate real-time recommendations"""
        
        # Get user's recent interactions
        recent_events = list(self.user_sessions[user_id])[-20:]
        
        if not recent_events:
            return self._get_trending_recommendations()
        
        # Extract patterns
        viewed_products = set()
        purchased_products = set()
        categories = defaultdict(int)
        
        for event in recent_events:
            if event['event_type'] == 'view':
                viewed_products.add(event['product_id'])
            elif event['event_type'] == 'purchase':
                purchased_products.add(event['product_id'])
            
            # Extract category from context if available
            if 'category' in event.get('context', {}):
                categories[event['context']['category']] += 1
        
        # Generate recommendations based on patterns
        recommendations = []
        
        # Category-based recommendations
        top_category = max(categories.keys(), key=categories.get) if categories else None
        if top_category:
            category_recs = self._get_category_recommendations(top_category, 5)
            recommendations.extend(category_recs)
        
        # Trending items
        trending_recs = self._get_trending_recommendations(5)
        recommendations.extend(trending_recs)
        
        # Remove duplicates and items already interacted with
        seen_products = viewed_products.union(purchased_products)
        unique_recs = []
        for rec in recommendations:
            if rec['product_id'] not in seen_products and rec not in unique_recs:
                unique_recs.append(rec)
                if len(unique_recs) >= 10:
                    break
        
        return unique_recs
    
    def _get_category_recommendations(self, category: str, limit: int) -> List[Dict[str, Any]]:
        """Get recommendations for a specific category"""
        
        cache_key = f"category_recs:{category}"
        cached_recs = self.redis_client.get(cache_key)
        
        if cached_recs:
            return json.loads(cached_recs)[:limit]
        
        # Generate category recommendations
        recs = [
            {
                'product_id': f'cat_{category}_{i}',
                'category': category,
                'score': 0.8 - (i * 0.1),
                'reason': f'Popular in {category}'
            }
            for i in range(limit)
        ]
        
        # Cache for 1 hour
        self.redis_client.setex(cache_key, 3600, json.dumps(recs))
        
        return recs
    
    def _get_trending_recommendations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get trending item recommendations"""
        
        # Sort trending items by score
        sorted_trending = sorted(
            self.trending_items.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        recommendations = []
        for product_id, score in sorted_trending:
            recommendations.append({
                'product_id': product_id,
                'score': min(score / 100.0, 1.0),  # Normalize score
                'reason': 'Trending now'
            })
        
        return recommendations
    
    def _update_trending_items(self):
        """Background task to update trending items"""
        while True:
            try:
                # Decay trending scores every minute
                for product_id in list(self.trending_items.keys()):
                    self.trending_items[product_id] = max(
                        0, self.trending_items[product_id] - 1
                    )
                    
                    # Remove items with zero score
                    if self.trending_items[product_id] == 0:
                        del self.trending_items[product_id]
                
                time.sleep(60)  # Update every minute
                
            except Exception as e:
                logger.error(f"Error updating trending items: {e}")
                time.sleep(60)
    
    def _cleanup_old_sessions(self):
        """Background task to cleanup old user sessions"""
        while True:
            try:
                cutoff_time = datetime.now() - timedelta(hours=24)
                
                for user_id in list(self.user_sessions.keys()):
                    session = self.user_sessions[user_id]
                    
                    # Remove old events
                    while session and datetime.fromisoformat(
                        session[0]['timestamp']
                    ) < cutoff_time:
                        session.popleft()
                    
                    # Remove empty sessions
                    if not session:
                        del self.user_sessions[user_id]
                
                time.sleep(3600)  # Cleanup every hour
                
            except Exception as e:
                logger.error(f"Error cleaning up sessions: {e}")
                time.sleep(3600)
    
    def _update_user_cache(self, event: UserEvent):
        """Update user cache with latest interaction"""
        
        user_key = f"user_latest:{event.user_id}"
        
        latest_interaction = {
            'product_id': event.product_id,
            'event_type': event.event_type,
            'timestamp': event.timestamp.isoformat(),
            'session_id': event.session_id
        }
        
        self.redis_client.setex(user_key, 3600, json.dumps(latest_interaction))