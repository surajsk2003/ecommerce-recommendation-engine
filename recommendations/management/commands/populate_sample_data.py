from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recommendations.models import Product, UserBehavior
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Populate database with sample data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )
    
    def handle(self, *args, **options):
        fake = Faker()
        
        # Clear existing data if requested
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            UserBehavior.objects.all().delete()
            Product.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
        
        # Check if data already exists
        if User.objects.filter(username__startswith='user_').exists():
            self.stdout.write(
                self.style.WARNING('Sample data already exists. Use --clear to reset.')
            )
            return
        
        # Create sample users
        users = []
        for i in range(100):
            user, created = User.objects.get_or_create(
                username=f'user_{i}',
                defaults={
                    'email': fake.email(),
                    'password': 'password123'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        
        # Create sample products
        categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
        products = []
        
        for i in range(500):
            product, created = Product.objects.get_or_create(
                name=fake.catch_phrase(),
                defaults={
                    'description': fake.text(),
                    'category': random.choice(categories),
                    'price': random.uniform(10, 1000)
                }
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