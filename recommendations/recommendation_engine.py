from django.core.cache import cache
from django.db.models import Q, Count, Avg
from .models import UserBehavior, Product, UserProfile, RecommendationCache
from .ml_models import CollaborativeFilteringModel, MatrixFactorizationModel
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import json
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.cf_model = CollaborativeFilteringModel()
        self.mf_model = MatrixFactorizationModel()
        self.is_trained = False
        
    def train_models(self):
        """Train all recommendation models"""
        try:
            behaviors = UserBehavior.objects.select_related('user', 'product').all()
            
            if not behaviors.exists():
                logger.warning("No user behavior data available for training")
                return False
            
            data = []
            for behavior in behaviors:
                data.append({
                    'user_id': behavior.user.id,
                    'product_id': behavior.product.id,
                    'interaction_type': behavior.interaction_type,
                    'timestamp': behavior.timestamp
                })
            
            df = pd.DataFrame(data)
            
            logger.info("Training collaborative filtering model...")
            self.cf_model.train(df)
            
            logger.info("Training matrix factorization model...")
            self.mf_model.fit(df)
            
            self.is_trained = True
            cache.set('models_trained', True, timeout=3600)
            
            logger.info("Models trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training models: {str(e)}")
            return False
    
    def get_recommendations(self, user_id: int, num_recommendations: int = 10) -> List[Dict]:
        """Get personalized recommendations for user"""
        cache_key = f"recommendations_user_{user_id}_{num_recommendations}"
        cached_recommendations = cache.get(cache_key)
        
        if cached_recommendations:
            return cached_recommendations
        
        try:
            if not self.is_trained and not cache.get('models_trained'):
                self.train_models()
            
            user_interactions = UserBehavior.objects.filter(
                user_id=user_id
            ).values_list('product_id', flat=True)
            
            candidate_products = Product.objects.exclude(
                id__in=user_interactions
            ).values_list('id', flat=True)
            
            if not candidate_products:
                return self._get_popular_recommendations(num_recommendations)
            
            candidate_list = list(candidate_products)
            
            cf_scores = self.cf_model.predict_user_preferences(user_id, candidate_list)
            
            mf_scores = []
            for product_id in candidate_list:
                score = self.mf_model.predict(user_id, product_id)
                mf_scores.append(score)
            
            ensemble_scores = 0.7 * cf_scores + 0.3 * np.array(mf_scores)
            
            recommendations = []
            for i, product_id in enumerate(candidate_list):
                product = Product.objects.get(id=product_id)
                recommendations.append({
                    'product_id': product_id,
                    'product_name': product.name,
                    'category': product.category,
                    'price': float(product.price),
                    'confidence_score': float(ensemble_scores[i]),
                    'cf_score': float(cf_scores[i]),
                    'mf_score': float(mf_scores[i])
                })
            
            recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
            final_recommendations = recommendations[:num_recommendations]
            
            cache.set(cache_key, final_recommendations, timeout=1800)
            
            self._store_recommendations_cache(user_id, final_recommendations)
            
            return final_recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations for user {user_id}: {str(e)}")
            return self._get_popular_recommendations(num_recommendations)
    
    def _get_popular_recommendations(self, num_recommendations: int) -> List[Dict]:
        """Fallback to popular products for cold start"""
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
            
            cache_pattern = f"recommendations_user_{user_id}_*"
            cache.delete_pattern(cache_pattern)
            
            self._update_user_embedding(user_id)
            
        except Exception as e:
            logger.error(f"Error recording interaction: {str(e)}")
    
    def _update_user_embedding(self, user_id: int):
        """Update user embedding vector"""
        try:
            if self.cf_model.model:
                embedding = self.cf_model.get_user_embedding(user_id)
                if embedding is not None:
                    profile, created = UserProfile.objects.get_or_create(user_id=user_id)
                    profile.embedding_vector = embedding.tolist()
                    profile.save()
        except Exception as e:
            logger.error(f"Error updating user embedding: {str(e)}")