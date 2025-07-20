import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)

class CollaborativeFilteringModel:
    """Simplified CF model using scikit-learn only"""
    
    def __init__(self, n_components=50):
        self.n_components = n_components
        self.model = TruncatedSVD(n_components=n_components, random_state=42)
        self.user_encoder = {}
        self.product_encoder = {}
        self.user_decoder = {}
        self.product_decoder = {}
        self.user_item_matrix = None
        self.is_fitted = False
        
    def prepare_data(self, df):
        """Prepare interaction data for training"""
        # Create user and product encoders
        unique_users = df['user_id'].unique()
        unique_products = df['product_id'].unique()
        
        self.user_encoder = {user: idx for idx, user in enumerate(unique_users)}
        self.product_encoder = {product: idx for idx, product in enumerate(unique_products)}
        self.user_decoder = {idx: user for user, idx in self.user_encoder.items()}
        self.product_decoder = {idx: product for product, idx in self.product_encoder.items()}
        
        # Create user-item interaction matrix
        n_users = len(unique_users)
        n_products = len(unique_products)
        
        self.user_item_matrix = np.zeros((n_users, n_products))
        
        for _, row in df.iterrows():
            user_idx = self.user_encoder[row['user_id']]
            product_idx = self.product_encoder[row['product_id']]
            
            # Simple scoring: view=1, like=2, cart=3, purchase=5
            score_map = {'view': 1, 'like': 2, 'cart': 3, 'purchase': 5}
            score = score_map.get(row.get('interaction_type', 'view'), 1)
            
            self.user_item_matrix[user_idx, product_idx] = max(
                self.user_item_matrix[user_idx, product_idx], score
            )
        
        return self.user_item_matrix
    
    def train(self, df):
        """Train the collaborative filtering model"""
        try:
            logger.info("Training simplified collaborative filtering model...")
            
            # Prepare data
            interaction_matrix = self.prepare_data(df)
            
            # Fit SVD model
            self.model.fit(interaction_matrix)
            self.is_fitted = True
            
            logger.info(f"Model trained with {len(self.user_encoder)} users and {len(self.product_encoder)} products")
            return True
            
        except Exception as e:
            logger.error(f"Error training CF model: {str(e)}")
            return False
    
    def predict_user_preferences(self, user_id, product_ids):
        """Predict user preferences for given products"""
        if not self.is_fitted:
            logger.warning("Model not trained yet")
            return np.random.random(len(product_ids))
        
        try:
            if user_id not in self.user_encoder:
                # Cold start - return random scores
                return np.random.random(len(product_ids))
            
            user_idx = self.user_encoder[user_id]
            
            # Transform the user-item matrix
            user_features = self.model.transform(self.user_item_matrix)
            product_features = self.model.components_.T
            
            # Get user vector
            user_vector = user_features[user_idx]
            
            scores = []
            for product_id in product_ids:
                if product_id in self.product_encoder:
                    product_idx = self.product_encoder[product_id]
                    product_vector = product_features[product_idx]
                    
                    # Compute similarity score
                    score = np.dot(user_vector, product_vector)
                    scores.append(max(0, score))  # Ensure non-negative
                else:
                    scores.append(0.1)  # Low score for unknown products
            
            return np.array(scores)
            
        except Exception as e:
            logger.error(f"Error predicting preferences: {str(e)}")
            return np.random.random(len(product_ids))
    
    def get_user_embedding(self, user_id):
        """Get user embedding vector"""
        if not self.is_fitted or user_id not in self.user_encoder:
            return None
        
        try:
            user_idx = self.user_encoder[user_id]
            user_features = self.model.transform(self.user_item_matrix)
            return user_features[user_idx]
        except Exception as e:
            logger.error(f"Error getting user embedding: {str(e)}")
            return None


class MatrixFactorizationModel:
    """Simple matrix factorization using scikit-learn"""
    
    def __init__(self, n_factors=50, learning_rate=0.01, regularization=0.1):
        self.n_factors = n_factors
        self.learning_rate = learning_rate
        self.regularization = regularization
        self.user_factors = None
        self.item_factors = None
        self.user_bias = None
        self.item_bias = None
        self.global_bias = 0
        self.user_encoder = {}
        self.item_encoder = {}
        self.is_fitted = False
    
    def fit(self, df, epochs=20):
        """Fit matrix factorization model"""
        try:
            logger.info("Training simplified matrix factorization model...")
            
            # Prepare data
            unique_users = df['user_id'].unique()
            unique_items = df['product_id'].unique()
            
            self.user_encoder = {user: idx for idx, user in enumerate(unique_users)}
            self.item_encoder = {item: idx for idx, item in enumerate(unique_items)}
            
            n_users = len(unique_users)
            n_items = len(unique_items)
            
            # Initialize factors randomly
            np.random.seed(42)
            self.user_factors = np.random.normal(0, 0.1, (n_users, self.n_factors))
            self.item_factors = np.random.normal(0, 0.1, (n_items, self.n_factors))
            self.user_bias = np.zeros(n_users)
            self.item_bias = np.zeros(n_items)
            
            # Calculate global bias
            score_map = {'view': 1, 'like': 2, 'cart': 3, 'purchase': 5}
            ratings = [score_map.get(row.get('interaction_type', 'view'), 1) for _, row in df.iterrows()]
            self.global_bias = np.mean(ratings)
            
            # Simple SGD training (simplified)
            for epoch in range(epochs):
                for _, row in df.iterrows():
                    user_idx = self.user_encoder[row['user_id']]
                    item_idx = self.item_encoder[row['product_id']]
                    rating = score_map.get(row.get('interaction_type', 'view'), 1)
                    
                    # Predict and calculate error
                    prediction = self.predict_single(user_idx, item_idx)
                    error = rating - prediction
                    
                    # Update factors (simplified SGD)
                    user_factor = self.user_factors[user_idx].copy()
                    item_factor = self.item_factors[item_idx].copy()
                    
                    self.user_factors[user_idx] += self.learning_rate * (
                        error * item_factor - self.regularization * user_factor
                    )
                    self.item_factors[item_idx] += self.learning_rate * (
                        error * user_factor - self.regularization * item_factor
                    )
                    
                    self.user_bias[user_idx] += self.learning_rate * (
                        error - self.regularization * self.user_bias[user_idx]
                    )
                    self.item_bias[item_idx] += self.learning_rate * (
                        error - self.regularization * self.item_bias[item_idx]
                    )
            
            self.is_fitted = True
            logger.info(f"Matrix factorization trained for {epochs} epochs")
            return True
            
        except Exception as e:
            logger.error(f"Error training MF model: {str(e)}")
            return False
    
    def predict_single(self, user_idx, item_idx):
        """Predict single user-item interaction"""
        if not self.is_fitted:
            return self.global_bias
        
        prediction = (
            self.global_bias +
            self.user_bias[user_idx] +
            self.item_bias[item_idx] +
            np.dot(self.user_factors[user_idx], self.item_factors[item_idx])
        )
        return prediction
    
    def predict(self, user_id, item_id):
        """Predict user-item interaction score"""
        if not self.is_fitted:
            return 0.5
        
        if user_id not in self.user_encoder or item_id not in self.item_encoder:
            return self.global_bias / 5.0  # Normalize to 0-1 range
        
        user_idx = self.user_encoder[user_id]
        item_idx = self.item_encoder[item_id]
        
        prediction = self.predict_single(user_idx, item_idx)
        return max(0, min(1, prediction / 5.0))  # Normalize to 0-1 range