from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recommendations.models import Product, UserBehavior
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Populate database with sample data'
    
    def handle(self, *args, **options):
        fake = Faker()
        
        # Create sample users
        users = []
        for i in range(100):
            user = User.objects.create_user(
                username=f'user_{i}',
                email=fake.email(),
                password='password123'
            )
            users.append(user)
        
        # Create sample products
        categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
        products = []
        
        for i in range(500):
            product = Product.objects.create(
                name=fake.catch_phrase(),
                description=fake.text(),
                category=random.choice(categories),
                price=random.uniform(10, 1000)
            )
            products.append(product)
        
        # Create sample interactions
        interaction_types = ['view', 'like', 'cart', 'purchase']
        
        for _ in range(10000):
            UserBehavior.objects.create(
                user=random.choice(users),
                product=random.choice(products),
                interaction_type=random.choice(interaction_types)
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data')
        )