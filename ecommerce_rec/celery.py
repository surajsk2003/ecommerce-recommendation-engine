import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_rec.settings')

app = Celery('ecommerce_rec')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task
def retrain_models():
    """Periodic task to retrain recommendation models"""
    from recommendations.recommendation_engine import RecommendationEngine
    
    engine = RecommendationEngine()
    success = engine.train_models()
    
    return f"Model retraining {'successful' if success else 'failed'}"