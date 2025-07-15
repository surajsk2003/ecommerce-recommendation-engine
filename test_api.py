#!/usr/bin/env python3
"""Simple API test script"""

import subprocess
import json

def run_curl(command):
    """Run curl command and return result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

print("=== E-Commerce Recommendation Engine API Test ===\n")

# Test 1: Record interaction
print("1. Recording interaction...")
cmd1 = '''curl -s -X POST "http://127.0.0.1:8000/api/interaction/" -H "Content-Type: application/json" -d '{"user_id": 1, "product_id": 25, "interaction_type": "like"}\''''
result1 = run_curl(cmd1)
print(f"Result: {result1}\n")

# Test 2: Get recommendations
print("2. Getting recommendations...")
cmd2 = 'curl -s "http://127.0.0.1:8000/api/recommendations/1/?count=3"'
result2 = run_curl(cmd2)
try:
    data = json.loads(result2)
    print(f"User {data['user_id']} recommendations:")
    for rec in data['recommendations']:
        print(f"  - {rec['product_name']} (Score: {rec['confidence_score']:.3f})")
except:
    print(f"Raw result: {result2}")
print()

# Test 3: Search products
print("3. Searching products...")
cmd3 = 'curl -s "http://127.0.0.1:8000/api/search/?q=home&user_id=1"'
result3 = run_curl(cmd3)
try:
    data = json.loads(result3)
    print(f"Found {data['count']} products for 'home'")
    for product in data['products'][:3]:
        score = product.get('personalization_score', 'N/A')
        print(f"  - {product['name']} (${product['price']}) - Score: {score}")
except:
    print(f"Raw result: {result3}")
print()

# Test 4: Train models
print("4. Training models...")
cmd4 = 'curl -s -X POST "http://127.0.0.1:8000/api/train/"'
result4 = run_curl(cmd4)
print(f"Result: {result4}")

print("\n=== API Test Complete ===")