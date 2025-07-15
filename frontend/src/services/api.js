// API service to connect React frontend with Django backend
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-domain.com/api' 
  : 'http://localhost:8000/api';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Get personalized recommendations
  async getRecommendations(userId, count = 10) {
    return this.request(`/recommendations/${userId}/?count=${count}`);
  }

  // Record user interaction
  async recordInteraction(userId, productId, interactionType) {
    return this.request('/interaction/', {
      method: 'POST',
      body: JSON.stringify({
        user_id: userId,
        product_id: productId,
        interaction_type: interactionType
      })
    });
  }

  // Search products
  async searchProducts(query, userId = null) {
    const params = new URLSearchParams({ q: query });
    if (userId) params.append('user_id', userId);
    return this.request(`/search/?${params}`);
  }

  // Trigger model training
  async trainModels() {
    return this.request('/train/', { method: 'POST' });
  }

  // Get all products (fallback for demo)
  async getAllProducts() {
    try {
      return await this.searchProducts('', null);
    } catch (error) {
      // Return sample data if backend is not available
      return {
        products: [
          { id: 1, name: "Wireless Bluetooth Headphones", category: "Electronics", price: 99.99, description: "Premium noise-canceling headphones" },
          { id: 2, name: "Smart Fitness Watch", category: "Electronics", price: 199.99, description: "Track your health and fitness goals" },
          { id: 3, name: "Organic Cotton T-Shirt", category: "Clothing", price: 29.99, description: "Comfortable and sustainable fashion" },
          { id: 4, name: "Premium Coffee Beans", category: "Food", price: 24.99, description: "Single-origin artisan roasted coffee" },
          { id: 5, name: "Yoga Mat Pro", category: "Sports", price: 59.99, description: "Non-slip premium yoga mat" }
        ],
        count: 5
      };
    }
  }
}

const apiService = new ApiService();
export default apiService;