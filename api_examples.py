"""
API Usage Examples for E-Commerce Recommendation Engine
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def get_recommendations(user_id, count=10):
    """Get personalized recommendations for a user"""
    url = f"{BASE_URL}/recommendations/{user_id}/"
    params = {"count": count}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Recommendations for User {user_id}:")
            for rec in data['recommendations']:
                print(f"  - {rec['product_name']} (Score: {rec['confidence_score']:.3f})")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Connection error: {str(e)}")

def record_interaction(user_id, product_id, interaction_type):
    """Record a user interaction"""
    url = f"{BASE_URL}/interaction/"
    data = {
        "user_id": user_id,
        "product_id": product_id,
        "interaction_type": interaction_type
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": "dummy"  # For testing
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 201:
            print(f"Interaction recorded: User {user_id} {interaction_type} Product {product_id}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection error: {str(e)}")

def search_products(query, user_id=None):
    """Search products with optional personalization"""
    url = f"{BASE_URL}/search/"
    params = {"q": query}
    
    if user_id:
        params["user_id"] = user_id
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Search results for '{query}':")
            for product in data['products']:
                score = product.get('personalization_score', 'N/A')
                print(f"  - {product['name']} (${product['price']}) - Score: {score}")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Connection error: {str(e)}")

def train_models():
    """Trigger model training"""
    url = f"{BASE_URL}/train/"
    
    try:
        response = requests.post(url, timeout=30)
        
        if response.status_code == 200:
            print("Model training started successfully")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Connection error: {str(e)}")

if __name__ == "__main__":
    # Example usage
    print("=== E-Commerce Recommendation Engine API Examples ===\n")
    
    # Record some interactions
    print("1. Recording user interactions...")
    record_interaction(1, 10, "view")
    record_interaction(1, 10, "like")
    record_interaction(1, 15, "purchase")
    
    print("\n2. Getting recommendations...")
    get_recommendations(1, 5)
    
    print("\n3. Searching products...")
    search_products("electronics", user_id=1)
    
    print("\n4. Training models...")
    train_models()