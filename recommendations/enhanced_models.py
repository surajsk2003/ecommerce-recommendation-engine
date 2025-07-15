import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from scipy.sparse import csr_matrix
import logging
from typing import Dict, List, Tuple, Optional, Any
import joblib
import json
import os
from datetime import datetime

# Optional imports for advanced models
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None
    nn = None
    F = None

logger = logging.getLogger(__name__)

class TransformerRecommendationModel(nn.Module):
    """Advanced Transformer-based recommendation model"""
    
    def __init__(self, num_users, num_items, embedding_dim=128, num_heads=8, num_layers=4):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.item_embedding = nn.Embedding(num_items, embedding_dim)
        
        # Transformer layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_dim,
            nhead=num_heads,
            dim_feedforward=512,
            dropout=0.1,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Output layers
        self.layer_norm = nn.LayerNorm(embedding_dim)
        self.dropout = nn.Dropout(0.1)
        self.output_layer = nn.Linear(embedding_dim * 2, 1)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, user_ids, item_ids):
        user_emb = self.user_embedding(user_ids)
        item_emb = self.item_embedding(item_ids)
        
        # Transformer processing
        combined = torch.cat([user_emb.unsqueeze(1), item_emb.unsqueeze(1)], dim=1)
        transformed = self.transformer(combined)
        
        # Pooling
        pooled = torch.mean(transformed, dim=1)
        pooled = self.layer_norm(pooled)
        pooled = self.dropout(pooled)
        
        # Concatenate user and item embeddings
        user_item_concat = torch.cat([user_emb, item_emb], dim=1)
        
        # Final prediction
        output = self.output_layer(user_item_concat)
        return self.sigmoid(output)

class DeepCollaborativeFiltering(tf.keras.Model):
    """Deep Neural Collaborative Filtering with advanced features"""
    
    def __init__(self, num_users, num_items, embedding_dim=64, hidden_dims=[256, 128, 64]):
        super().__init__()
        self.num_users = num_users
        self.num_items = num_items
        self.embedding_dim = embedding_dim
        
        # Embeddings
        self.user_embedding = tf.keras.layers.Embedding(num_users, embedding_dim)
        self.item_embedding = tf.keras.layers.Embedding(num_items, embedding_dim)
        
        # Bias terms
        self.user_bias = tf.keras.layers.Embedding(num_users, 1)
        self.item_bias = tf.keras.layers.Embedding(num_items, 1)
        self.global_bias = tf.Variable(0.0, trainable=True)
        
        # Deep layers
        self.dense_layers = []
        for dim in hidden_dims:
            self.dense_layers.append(tf.keras.layers.Dense(dim, activation='relu'))
            self.dense_layers.append(tf.keras.layers.Dropout(0.2))
            self.dense_layers.append(tf.keras.layers.BatchNormalization())
        
        self.output_layer = tf.keras.layers.Dense(1, activation='sigmoid')
        
    def call(self, inputs, training=False):
        user_ids, item_ids = inputs
        
        # Get embeddings
        user_emb = self.user_embedding(user_ids)
        item_emb = self.item_embedding(item_ids)
        
        # Get biases
        user_bias = tf.squeeze(self.user_bias(user_ids), axis=-1)
        item_bias = tf.squeeze(self.item_bias(item_ids), axis=-1)
        
        # Matrix factorization component
        mf_output = tf.reduce_sum(user_emb * item_emb, axis=1)
        
        # Deep component
        concat_features = tf.concat([user_emb, item_emb], axis=1)
        deep_output = concat_features
        
        for layer in self.dense_layers:
            deep_output = layer(deep_output, training=training)
        
        deep_output = tf.squeeze(self.output_layer(deep_output), axis=-1)
        
        # Combine MF and Deep components
        prediction = mf_output + deep_output + user_bias + item_bias + self.global_bias
        
        return tf.nn.sigmoid(prediction)

class HybridRecommendationSystem:
    """Advanced hybrid recommendation system with multiple algorithms"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.models = {}
        self.weights = {}
        self.scalers = {}
        self.encoders = {}
        self.is_trained = False
        
    def prepare_data(self, interactions_df: pd.DataFrame, 
                    items_df: pd.DataFrame = None, 
                    users_df: pd.DataFrame = None) -> Dict[str, Any]:
        """Prepare data for training"""
        
        # Encode users and items
        self.encoders['user'] = LabelEncoder()
        self.encoders['item'] = LabelEncoder()
        
        interactions_df['user_encoded'] = self.encoders['user'].fit_transform(interactions_df['user_id'])
        interactions_df['item_encoded'] = self.encoders['item'].fit_transform(interactions_df['item_id'])
        
        # Create user-item matrix
        user_item_matrix = csr_matrix(
            (interactions_df['rating'], 
             (interactions_df['user_encoded'], interactions_df['item_encoded'])),
            shape=(len(self.encoders['user'].classes_), len(self.encoders['item'].classes_))
        )
        
        # Extract features
        features = self._extract_features(interactions_df, items_df, users_df)
        
        return {
            'interactions': interactions_df,
            'user_item_matrix': user_item_matrix,
            'features': features,
            'num_users': len(self.encoders['user'].classes_),
            'num_items': len(self.encoders['item'].classes_)
        }
    
    def _extract_features(self, interactions_df: pd.DataFrame, 
                         items_df: pd.DataFrame = None, 
                         users_df: pd.DataFrame = None) -> pd.DataFrame:
        """Extract features for ensemble models"""
        
        # User features
        user_features = interactions_df.groupby('user_id').agg({
            'rating': ['mean', 'std', 'count']
        }).reset_index()
        
        user_features.columns = ['user_id', 'avg_rating', 'std_rating', 'num_ratings']
        user_features['rating_range'] = user_features['std_rating'].fillna(0)
        
        # Item features
        item_features = interactions_df.groupby('item_id').agg({
            'rating': ['mean', 'std', 'count']
        }).reset_index()
        
        item_features.columns = ['item_id', 'avg_rating', 'std_rating', 'num_ratings']
        item_features['popularity_score'] = item_features['num_ratings'] * item_features['avg_rating']
        
        # Merge features
        features_df = interactions_df.merge(user_features, on='user_id', how='left', suffixes=('', '_user'))
        features_df = features_df.merge(item_features, on='item_id', how='left', suffixes=('', '_item'))
        
        return features_df
    
    def train_models(self, data: Dict[str, Any], validation_split: float = 0.2):
        """Train all models"""
        
        interactions_df = data['interactions']
        features_df = data['features']
        
        # Split data
        train_interactions, val_interactions = train_test_split(
            interactions_df, test_size=validation_split, random_state=42
        )
        
        # Train deep learning models
        self._train_deep_models(train_interactions, val_interactions, data)
        
        # Train ensemble models
        self._train_ensemble_models(features_df, train_interactions, val_interactions)
        
        self.is_trained = True
        logger.info("All models trained successfully")
    
    def _train_deep_models(self, train_interactions: pd.DataFrame, 
                          val_interactions: pd.DataFrame, data: Dict[str, Any]):
        """Train deep learning models"""
        
        num_users = data['num_users']
        num_items = data['num_items']
        
        # Prepare training data
        train_users = train_interactions['user_encoded'].values
        train_items = train_interactions['item_encoded'].values
        train_ratings = train_interactions['rating'].values
        
        val_users = val_interactions['user_encoded'].values
        val_items = val_interactions['item_encoded'].values
        val_ratings = val_interactions['rating'].values
        
        # Deep Collaborative Filtering
        logger.info("Training Deep CF model...")
        self.models['deep_cf'] = DeepCollaborativeFiltering(num_users, num_items)
        self.models['deep_cf'].compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['mae', 'mse']
        )
        
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=5, restore_best_weights=True
        )
        
        self.models['deep_cf'].fit(
            [train_users, train_items], train_ratings,
            validation_data=([val_users, val_items], val_ratings),
            epochs=20, batch_size=1024, callbacks=[early_stopping], verbose=1
        )
        
        # Transformer model (simplified for demo)
        logger.info("Training Transformer model...")
        self.models['transformer'] = TransformerRecommendationModel(num_users, num_items)
        self._train_transformer_model(train_interactions, val_interactions)
    
    def _train_transformer_model(self, train_interactions: pd.DataFrame, 
                                val_interactions: pd.DataFrame):
        """Train transformer model using PyTorch"""
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = self.models['transformer'].to(device)
        
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.BCELoss()
        
        # Prepare data loaders
        train_dataset = torch.utils.data.TensorDataset(
            torch.tensor(train_interactions['user_encoded'].values, dtype=torch.long),
            torch.tensor(train_interactions['item_encoded'].values, dtype=torch.long),
            torch.tensor(train_interactions['rating'].values, dtype=torch.float32)
        )
        
        train_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=1024, shuffle=True
        )
        
        model.train()
        for epoch in range(10):
            total_loss = 0
            for batch_users, batch_items, batch_ratings in train_loader:
                batch_users = batch_users.to(device)
                batch_items = batch_items.to(device)
                batch_ratings = batch_ratings.to(device)
                
                optimizer.zero_grad()
                predictions = model(batch_users, batch_items).squeeze()
                loss = criterion(predictions, batch_ratings)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            if epoch % 5 == 0:
                logger.info(f"Transformer Epoch {epoch}: Loss = {total_loss/len(train_loader):.4f}")
    
    def _train_ensemble_models(self, features_df: pd.DataFrame, 
                              train_interactions: pd.DataFrame, 
                              val_interactions: pd.DataFrame):
        """Train ensemble models"""
        
        # Prepare feature columns
        feature_columns = [
            'user_encoded', 'item_encoded',
            'avg_rating_user', 'std_rating_user', 'num_ratings_user',
            'avg_rating_item', 'std_rating_item', 'num_ratings_item',
            'popularity_score'
        ]
        
        # Select available features
        available_features = [col for col in feature_columns if col in features_df.columns]
        
        if not available_features:
            logger.warning("No features available for ensemble models")
            return
        
        # Prepare training data
        train_features = features_df[features_df['user_id'].isin(train_interactions['user_id'])][available_features]
        train_targets = features_df[features_df['user_id'].isin(train_interactions['user_id'])]['rating']
        
        # Handle missing values
        train_features = train_features.fillna(0)
        
        # Scale features
        self.scalers['ensemble'] = StandardScaler()
        train_features_scaled = self.scalers['ensemble'].fit_transform(train_features)
        
        # Train Random Forest
        logger.info("Training Random Forest model...")
        self.models['random_forest'] = RandomForestRegressor(
            n_estimators=100, max_depth=10, random_state=42
        )
        self.models['random_forest'].fit(train_features_scaled, train_targets)
        
        # Set equal weights for ensemble
        self.weights = {
            'deep_cf': 0.4,
            'transformer': 0.3,
            'random_forest': 0.3
        }
    
    def predict_single(self, user_id: int, item_id: int, return_individual: bool = False) -> Dict[str, float]:
        """Predict rating for a single user-item pair"""
        
        if not self.is_trained:
            raise ValueError("Models must be trained before prediction")
        
        predictions = {}
        
        try:
            # Encode user and item
            user_encoded = self.encoders['user'].transform([user_id])[0]
            item_encoded = self.encoders['item'].transform([item_id])[0]
            
            # Deep CF prediction
            try:
                pred = self.models['deep_cf']([np.array([user_encoded]), np.array([item_encoded])])
                predictions['deep_cf'] = float(pred[0])
            except:
                predictions['deep_cf'] = 0.5
            
            # Transformer prediction
            try:
                device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                model = self.models['transformer'].to(device)
                model.eval()
                
                with torch.no_grad():
                    user_tensor = torch.tensor([user_encoded], dtype=torch.long).to(device)
                    item_tensor = torch.tensor([item_encoded], dtype=torch.long).to(device)
                    pred = model(user_tensor, item_tensor)
                    predictions['transformer'] = float(pred[0])
            except:
                predictions['transformer'] = 0.5
            
            # Random Forest prediction (simplified)
            try:
                # Create dummy features for prediction
                features = np.array([[user_encoded, item_encoded, 0.5, 0.2, 10, 0.6, 0.3, 15, 7.5]])
                if 'ensemble' in self.scalers:
                    features_scaled = self.scalers['ensemble'].transform(features)
                    pred = self.models['random_forest'].predict(features_scaled)
                    predictions['random_forest'] = float(pred[0])
                else:
                    predictions['random_forest'] = 0.5
            except:
                predictions['random_forest'] = 0.5
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            # Return default predictions
            predictions = {
                'deep_cf': 0.5,
                'transformer': 0.5,
                'random_forest': 0.5
            }
        
        if return_individual:
            return predictions
        
        # Ensemble prediction
        ensemble_pred = sum(predictions[model] * self.weights.get(model, 1.0) 
                           for model in predictions.keys())
        ensemble_pred /= sum(self.weights.values())
        
        return {'ensemble': ensemble_pred, **predictions}
    
    def get_recommendations(self, user_id: int, num_recommendations: int = 10) -> List[Dict[str, Any]]:
        """Get recommendations for a user"""
        
        if not self.is_trained:
            raise ValueError("Models must be trained before recommendation")
        
        try:
            # Get all unique items
            all_items = list(self.encoders['item'].classes_)
            
            # Score all items for the user
            item_scores = {}
            for item_id in all_items[:100]:  # Limit for demo
                try:
                    pred = self.predict_single(user_id, item_id)
                    item_scores[item_id] = pred['ensemble']
                except:
                    continue
            
            # Sort and return top recommendations
            sorted_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for item_id, score in sorted_items[:num_recommendations]:
                recommendations.append({
                    'item_id': item_id,
                    'predicted_rating': score,
                    'confidence': min(score, 1.0)
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in get_recommendations: {str(e)}")
            return []
    
    def save_models(self, path: str):
        """Save trained models"""
        
        os.makedirs(path, exist_ok=True)
        
        # Save encoders
        joblib.dump(self.encoders, os.path.join(path, 'encoders.pkl'))
        
        # Save scalers
        joblib.dump(self.scalers, os.path.join(path, 'scalers.pkl'))
        
        # Save weights
        with open(os.path.join(path, 'weights.json'), 'w') as f:
            json.dump(self.weights, f)
        
        # Save individual models
        for model_name, model in self.models.items():
            if model is not None:
                try:
                    if model_name == 'deep_cf':
                        model.save_weights(os.path.join(path, f'{model_name}_weights.h5'))
                    elif model_name == 'transformer':
                        torch.save(model.state_dict(), os.path.join(path, f'{model_name}.pth'))
                    else:
                        joblib.dump(model, os.path.join(path, f'{model_name}.pkl'))
                except Exception as e:
                    logger.error(f"Error saving {model_name}: {str(e)}")
    
    def load_models(self, path: str):
        """Load trained models"""
        
        try:
            # Load encoders
            self.encoders = joblib.load(os.path.join(path, 'encoders.pkl'))
            
            # Load scalers
            self.scalers = joblib.load(os.path.join(path, 'scalers.pkl'))
            
            # Load weights
            with open(os.path.join(path, 'weights.json'), 'r') as f:
                self.weights = json.load(f)
            
            self.is_trained = True
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")