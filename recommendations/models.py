from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserBehavior(models.Model):
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('like', 'Like'),
        ('cart', 'Add to Cart'),
        ('purchase', 'Purchase'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    rating = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'product']),
            models.Index(fields=['timestamp']),
        ]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.JSONField(default=dict)
    embedding_vector = models.JSONField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

class RecommendationCache(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommended_products = models.JSONField()
    confidence_scores = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

class DatasetUpload(models.Model):
    DATASET_TYPES = [
        ('interactions', 'User Interactions'),
        ('items', 'Product Items'),
        ('users', 'User Profiles'),
    ]
    
    dataset_type = models.CharField(max_length=20, choices=DATASET_TYPES)
    file_path = models.CharField(max_length=500)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.dataset_type} - {self.uploaded_at}"

class ModelTraining(models.Model):
    dataset_ids = models.JSONField()  # List of dataset IDs used for training
    config = models.JSONField()  # Model configuration parameters
    model_path = models.CharField(max_length=500)  # Path to saved model
    training_duration = models.FloatField()  # Training duration in seconds
    num_users = models.IntegerField()
    num_items = models.IntegerField()
    num_interactions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Training {self.id} - {self.created_at}"

class ExperimentResult(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    config = models.JSONField()
    results = models.JSONField()
    status = models.CharField(max_length=20, default='running')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']