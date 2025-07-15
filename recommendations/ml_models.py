import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)

class CollaborativeFilteringModel:
    def __init__(self, embedding_dim=50, learning_rate=0.001):
        self.embedding_dim = embedding_dim
        self.learning_rate = learning_rate
        self.model = None
        self.user_encoder = {}
        self.product_encoder = {}
        self.user_decoder = {}
        self.product_decoder = {}
        
    def build_model(self, num_users, num_products):
        """Build neural collaborative filtering model"""
        user_input = tf.keras.layers.Input(shape=(), name='user_id')
        product_input = tf.keras.layers.Input(shape=(), name='product_id')
        
        user_embedding = tf.keras.layers.Embedding(
            num_users, self.embedding_dim, name='user_embedding'
        )(user_input)
        product_embedding = tf.keras.layers.Embedding(
            num_products, self.embedding_dim, name='product_embedding'
        )(product_input)
        
        user_vec = tf.keras.layers.Flatten()(user_embedding)
        product_vec = tf.keras.layers.Flatten()(product_embedding)
        
        concat = tf.keras.layers.Concatenate()([user_vec, product_vec])
        
        dense1 = tf.keras.layers.Dense(128, activation='relu')(concat)
        dropout1 = tf.keras.layers.Dropout(0.3)(dense1)
        dense2 = tf.keras.layers.Dense(64, activation='relu')(dropout1)
        dropout2 = tf.keras.layers.Dropout(0.3)(dense2)
        dense3 = tf.keras.layers.Dense(32, activation='relu')(dropout2)
        
        output = tf.keras.layers.Dense(1, activation='sigmoid')(dense3)
        
        self.model = tf.keras.Model(inputs=[user_input, product_input], outputs=output)
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='binary_crossentropy',
            metrics=['mae', 'mse']
        )
        
        return self.model
    
    def prepare_data(self, interactions_df):
        """Prepare training data from user interactions"""
        unique_users = interactions_df['user_id'].unique()
        unique_products = interactions_df['product_id'].unique()
        
        self.user_encoder = {user: idx for idx, user in enumerate(unique_users)}
        self.product_encoder = {product: idx for idx, product in enumerate(unique_products)}
        self.user_decoder = {idx: user for user, idx in self.user_encoder.items()}
        self.product_decoder = {idx: product for product, idx in self.product_encoder.items()}
        
        interactions_df['user_encoded'] = interactions_df['user_id'].map(self.user_encoder)
        interactions_df['product_encoded'] = interactions_df['product_id'].map(self.product_encoder)
        
        interaction_weights = {
            'view': 1.0,
            'like': 2.0,
            'cart': 3.0,
            'purchase': 5.0
        }
        
        interactions_df['implicit_rating'] = interactions_df['interaction_type'].map(interaction_weights)
        
        max_rating = interactions_df['implicit_rating'].max()
        interactions_df['normalized_rating'] = interactions_df['implicit_rating'] / max_rating
        
        return interactions_df
    
    def train(self, interactions_df, epochs=50, batch_size=256, validation_split=0.2):
        """Train the collaborative filtering model"""
        prepared_data = self.prepare_data(interactions_df)
        
        num_users = len(self.user_encoder)
        num_products = len(self.product_encoder)
        self.build_model(num_users, num_products)
        
        user_ids = prepared_data['user_encoded'].values
        product_ids = prepared_data['product_encoded'].values
        ratings = prepared_data['normalized_rating'].values
        
        callbacks = [
            tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
            tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3)
        ]
        
        history = self.model.fit(
            [user_ids, product_ids], ratings,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def predict_user_preferences(self, user_id, product_ids):
        """Predict user preferences for given products"""
        if user_id not in self.user_encoder:
            return np.random.random(len(product_ids)) * 0.1
        
        user_encoded = self.user_encoder[user_id]
        product_encoded = [self.product_encoder.get(pid, 0) for pid in product_ids]
        
        user_array = np.array([user_encoded] * len(product_ids))
        product_array = np.array(product_encoded)
        
        predictions = self.model.predict([user_array, product_array])
        return predictions.flatten()
    
    def get_user_embedding(self, user_id):
        """Get user embedding vector"""
        if user_id not in self.user_encoder:
            return None
        
        user_encoded = self.user_encoder[user_id]
        embedding_layer = self.model.get_layer('user_embedding')
        return embedding_layer.get_weights()[0][user_encoded]

class MatrixFactorizationModel:
    def __init__(self, n_components=50):
        self.n_components = n_components
        self.svd = TruncatedSVD(n_components=n_components, random_state=42)
        self.user_item_matrix = None
        self.user_factors = None
        self.item_factors = None
        self.user_index = {}
        self.product_index = {}
        
    def fit(self, interactions_df):
        """Fit matrix factorization model"""
        pivot_df = interactions_df.pivot_table(
            index='user_id', 
            columns='product_id', 
            values='implicit_rating', 
            fill_value=0
        )
        
        self.user_item_matrix = pivot_df
        self.user_index = {user: idx for idx, user in enumerate(pivot_df.index)}
        self.product_index = {product: idx for idx, product in enumerate(pivot_df.columns)}
        
        self.user_factors = self.svd.fit_transform(pivot_df.values)
        self.item_factors = self.svd.components_.T
        
        return self
    
    def predict(self, user_id, product_id):
        """Predict rating for user-product pair"""
        try:
            user_idx = self.user_index[user_id]
            product_idx = self.product_index[product_id]
            
            prediction = np.dot(self.user_factors[user_idx], self.item_factors[product_idx])
            return max(0, min(1, prediction))
        except (ValueError, KeyError):
            return 0.1