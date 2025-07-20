from django.core.cache import cache
from django.db.models import Q, Count, Avg
from .models import UserBehavior, Product, UserProfile, RecommendationCache
from typing import List, Dict, Tuple
import json
import logging
import random

logger = logging.getLogger(__name__)

class SimpleRecommendationEngine:
    """Simple recommendation engine without ML dependencies"""
    
    def __init__(self):
        self.is_trained = True  # Always ready for simple recommendations
        
    def train_models(self):
        """Mock training - always successful"""
        logger.info("Simple recommendation engine initialized")
        cache.set('models_trained', True, timeout=3600)
        return True
    
    def get_recommendations(self, user_id: int, num_recommendations: int = 10) -> List[Dict]:
        """Get simple recommendations based on user behavior"""
        cache_key = f"simple_recommendations_user_{user_id}_{num_recommendations}"
        cached_recommendations = cache.get(cache_key)
        
        if cached_recommendations:
            return cached_recommendations
        
        try:
            # Get user's past interactions
            user_interactions = UserBehavior.objects.filter(
                user_id=user_id
            ).values_list('product_id', flat=True)
            
            # Get products user hasn't interacted with
            candidate_products = Product.objects.exclude(
                id__in=user_interactions
            )[:num_recommendations * 2]  # Get more to choose from
            
            if not candidate_products.exists():
                return self._get_popular_recommendations(num_recommendations)
            
            # Simple scoring based on category preferences and popularity
            recommendations = []
            user_categories = self._get_user_preferred_categories(user_id)
            
            for product in candidate_products:
                # Base score
                score = 0.5
                
                # Category boost
                if product.category.lower() in [cat.lower() for cat in user_categories]:
                    score += 0.3
                
                # Popularity boost
                interaction_count = UserBehavior.objects.filter(product=product).count()
                if interaction_count > 10:
                    score += 0.2
                elif interaction_count > 5:
                    score += 0.1
                
                # Random factor for diversity
                score += random.uniform(-0.1, 0.1)
                
                recommendations.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'category': product.category,
                    'price': float(product.price),
                    'confidence_score': min(1.0, max(0.0, score)),
                    'cf_score': score * 0.7,
                    'mf_score': score * 0.3
                })
            
            # Sort by confidence score and take top N
            recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
            final_recommendations = recommendations[:num_recommendations]
            
            # Cache results
            cache.set(cache_key, final_recommendations, timeout=1800)
            
            # Store in database for analytics
            self._store_recommendations_cache(user_id, final_recommendations)
            
            return final_recommendations
            
        except Exception as e:
            logger.error(f"Error generating simple recommendations for user {user_id}: {str(e)}")
            return self._get_popular_recommendations(num_recommendations)
    
    def _get_user_preferred_categories(self, user_id: int) -> List[str]:
        """Get user's preferred categories based on interaction history"""
        try:
            interactions = UserBehavior.objects.filter(user_id=user_id).select_related('product')
            category_counts = {}
            
            for interaction in interactions:
                category = interaction.product.category
                weight = 1
                if interaction.interaction_type == 'purchase':
                    weight = 5
                elif interaction.interaction_type == 'cart':
                    weight = 3
                elif interaction.interaction_type == 'like':
                    weight = 2
                
                category_counts[category] = category_counts.get(category, 0) + weight
            
            # Return top 3 categories
            sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
            return [cat for cat, _ in sorted_categories[:3]]
            
        except Exception as e:
            logger.error(f"Error getting user categories: {str(e)}")
            return []
    
    def _get_popular_recommendations(self, num_recommendations: int) -> List[Dict]:
        """Fallback to popular products"""
        cache_key = f"popular_products_{num_recommendations}"
        cached_popular = cache.get(cache_key)
        
        if cached_popular:
            return cached_popular
        
        popular_products = Product.objects.annotate(
            interaction_count=Count('userbehavior')
        ).order_by('-interaction_count')[:num_recommendations]
        
        recommendations = []
        for product in popular_products:
            recommendations.append({
                'product_id': product.id,
                'product_name': product.name,
                'category': product.category,
                'price': float(product.price),
                'confidence_score': 0.5,
                'cf_score': 0.5,
                'mf_score': 0.5
            })
        
        cache.set(cache_key, recommendations, timeout=3600)
        return recommendations
    
    def _store_recommendations_cache(self, user_id: int, recommendations: List[Dict]):
        """Store recommendations in database for analytics"""
        try:
            RecommendationCache.objects.create(
                user_id=user_id,
                recommended_products=[r['product_id'] for r in recommendations],
                confidence_scores=[r['confidence_score'] for r in recommendations]
            )
        except Exception as e:
            logger.error(f"Error storing recommendation cache: {str(e)}")
    
    def record_interaction(self, user_id: int, product_id: int, interaction_type: str):
        """Record user interaction and invalidate cache"""
        try:
            UserBehavior.objects.create(
                user_id=user_id,
                product_id=product_id,
                interaction_type=interaction_type
            )
            
            # Clear user's recommendation cache
            cache_pattern = f"simple_recommendations_user_{user_id}_*"
            cache.delete_pattern(cache_pattern)
            
        except Exception as e:
            logger.error(f"Error recording interaction: {str(e)}")


# Create global instance
RecommendationEngine = SimpleRecommendationEngine