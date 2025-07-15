import React, { useState, useEffect, useCallback } from 'react';
import { 
  ShoppingCart, User, Search, Star, TrendingUp, Eye, Heart, Package, 
  BarChart3, Users, Target, Zap, Brain, Activity, Bell, RefreshCw,
  Sparkles, Award, Cpu, Gauge
} from 'lucide-react';

const AdvancedEcommerceAI = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [currentView, setCurrentView] = useState('home');
  const [products, setProducts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [cart, setCart] = useState([]);
  // eslint-disable-next-line no-unused-vars
  const [userBehavior, setUserBehavior] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [analytics, setAnalytics] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [filterCategory, setFilterCategory] = useState('all');
  const [mlMetrics, setMLMetrics] = useState({});
  const [modelTrainingStatus, setModelTrainingStatus] = useState('idle');
  const [notifications, setNotifications] = useState([]);
  const [experimentResults, setExperimentResults] = useState([]);

  // Enhanced product data with more attributes
  const sampleProducts = [
    { 
      id: 1, name: "Wireless Bluetooth Headphones", category: "Electronics", price: 99.99, 
      rating: 4.5, image: "🎧", description: "Premium noise-canceling headphones with 30hr battery",
      tags: ["wireless", "noise-canceling", "premium"], brand: "AudioTech", stock: 45,
      features: ["Active Noise Cancellation", "30hr Battery", "Quick Charge"], reviews: 1247
    },
    { 
      id: 2, name: "Smart Fitness Watch", category: "Electronics", price: 199.99, 
      rating: 4.7, image: "⌚", description: "Advanced health tracking with GPS and heart rate",
      tags: ["fitness", "smartwatch", "health"], brand: "FitTech", stock: 32,
      features: ["GPS Tracking", "Heart Rate Monitor", "Sleep Analysis"], reviews: 892
    },
    { 
      id: 3, name: "Organic Cotton T-Shirt", category: "Clothing", price: 29.99, 
      rating: 4.3, image: "👕", description: "Sustainable and comfortable everyday wear",
      tags: ["organic", "sustainable", "cotton"], brand: "EcoWear", stock: 78,
      features: ["100% Organic Cotton", "Fair Trade", "Machine Washable"], reviews: 456
    },
    { 
      id: 4, name: "Premium Coffee Beans", category: "Food", price: 24.99, 
      rating: 4.8, image: "☕", description: "Single-origin Ethiopian beans, medium roast",
      tags: ["coffee", "organic", "fair-trade"], brand: "BrewMaster", stock: 67,
      features: ["Single Origin", "Medium Roast", "Fair Trade Certified"], reviews: 2134
    },
    { 
      id: 5, name: "Yoga Mat Pro", category: "Sports", price: 59.99, 
      rating: 4.6, image: "🧘", description: "Non-slip premium yoga mat with alignment guides",
      tags: ["yoga", "fitness", "non-slip"], brand: "ZenFit", stock: 23,
      features: ["Non-slip Surface", "Alignment Lines", "Eco-friendly"], reviews: 678
    }
  ];

  const users = [
    { 
      id: 1, name: "Alex Chen", email: "alex@example.com", type: "tech_enthusiast",
      preferences: ["electronics", "gadgets", "innovation"], age: 28, location: "San Francisco"
    },
    { 
      id: 2, name: "Sarah Johnson", email: "sarah@example.com", type: "fitness_lover",
      preferences: ["fitness", "health", "wellness"], age: 32, location: "New York"
    },
    { 
      id: 3, name: "Mike Rodriguez", email: "mike@example.com", type: "fashion_forward",
      preferences: ["fashion", "style", "designer"], age: 35, location: "Los Angeles"
    },
    { 
      id: 4, name: "Emma Wilson", email: "emma@example.com", type: "health_conscious",
      preferences: ["organic", "sustainable", "health"], age: 29, location: "Seattle"
    }
  ];

  // Initialize advanced analytics and ML metrics
  useEffect(() => {
    setProducts(sampleProducts);
    generateAdvancedBehavior();
    generateAdvancedAnalytics();
    generateMLMetrics();
    generateExperimentResults();
    startRealtimeUpdates();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const startRealtimeUpdates = () => {
    const interval = setInterval(() => {
      setAnalytics(prev => ({
        ...prev,
        liveUsers: Math.floor(Math.random() * 500) + 2800,
        requestsPerSecond: Math.floor(Math.random() * 100) + 450
      }));
    }, 3000);
    return () => clearInterval(interval);
  };

  const generateAdvancedBehavior = () => {
    const behaviors = [];
    const interactionTypes = ['view', 'like', 'cart', 'purchase', 'review', 'share', 'wishlist'];
    
    users.forEach(user => {
      const numInteractions = Math.floor(Math.random() * 25) + 10;
      for (let i = 0; i < numInteractions; i++) {
        const productId = Math.floor(Math.random() * sampleProducts.length) + 1;
        const type = interactionTypes[Math.floor(Math.random() * interactionTypes.length)];
        
        behaviors.push({
          userId: user.id,
          productId,
          type,
          timestamp: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000)
        });
      }
    });
    
    setUserBehavior(behaviors);
  };

  const generateAdvancedAnalytics = () => {
    setAnalytics({
      totalUsers: 127543,
      dailyActiveUsers: 23456,
      recommendationClickRate: 0.347,
      conversionRate: 0.078,
      avgOrderValue: 145.67,
      totalRecommendations: 2456789,
      modelAccuracy: 0.867,
      revenueImpact: 234567.89,
      liveUsers: 3247,
      requestsPerSecond: 523,
      avgResponseTime: 145,
      cacheHitRate: 0.934
    });
  };

  const generateMLMetrics = () => {
    setMLMetrics({
      activeModels: 4,
      modelVersion: '2.1.4',
      inferenceLatency: 45,
      throughput: 2340
    });
  };

  const generateExperimentResults = () => {
    setExperimentResults([
      {
        id: 1,
        name: 'Deep Learning vs Collaborative Filtering',
        status: 'completed',
        improvement: '+12.3%',
        confidence: 0.95,
        duration: '7 days',
        metric: 'CTR'
      },
      {
        id: 2,
        name: 'Real-time vs Batch Recommendations',
        status: 'running',
        improvement: '+8.7%',
        confidence: 0.87,
        duration: '3 days',
        metric: 'Conversion'
      }
    ]);
  };

  const addNotification = (message, type = 'info') => {
    const notification = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date()
    };
    setNotifications(prev => [notification, ...prev.slice(0, 4)]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== notification.id));
    }, 5000);
  };

  const generateAdvancedRecommendations = useCallback((userId) => {
    setIsLoading(true);
    setModelTrainingStatus('processing');
    
    setTimeout(() => {
      const recs = sampleProducts.slice(0, 6).map(product => ({
        ...product,
        confidence: Math.random() * 0.5 + 0.5,
        modelScores: {
          collaborative: Math.random(),
          contentBased: Math.random(),
          deepLearning: Math.random(),
          hybrid: Math.random()
        }
      }));
      
      setRecommendations(recs);
      setModelTrainingStatus('completed');
      setIsLoading(false);
      addNotification('🎯 AI recommendations updated with ensemble model', 'success');
    }, 2000);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const recordAdvancedInteraction = (productId, type) => {
    if (!currentUser) return;
    
    const newBehavior = {
      userId: currentUser.id,
      productId,
      type,
      timestamp: new Date()
    };
    
    setUserBehavior(prev => [...prev, newBehavior]);
    
    if (['purchase', 'cart', 'wishlist'].includes(type)) {
      setTimeout(() => generateAdvancedRecommendations(currentUser.id), 800);
      addNotification(`🔄 Model updating based on your ${type} action`, 'info');
    }
  };

  const addToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    if (existingItem) {
      setCart(cart.map(item => 
        item.id === product.id 
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
    recordAdvancedInteraction(product.id, 'cart');
  };

  const handleUserLogin = (user) => {
    setCurrentUser(user);
    generateAdvancedRecommendations(user.id);
    addNotification(`Welcome back, ${user.name}! 🎉`, 'success');
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         product.category.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = filterCategory === 'all' || product.category === filterCategory;
    return matchesSearch && matchesCategory;
  });

  // Enhanced Product Card
  const EnhancedProductCard = ({ product, isRecommendation = false, showAdvanced = false }) => (
    <div className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-gray-100">
      <div className="relative p-6">
        {isRecommendation && (
          <div className="absolute top-2 right-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs px-2 py-1 rounded-full">
            AI Pick
          </div>
        )}
        
        <div className="text-4xl mb-3 text-center">{product.image}</div>
        
        <div className="mb-2">
          <h3 className="font-semibold text-gray-800 text-lg mb-1">{product.name}</h3>
          <p className="text-sm text-gray-500 mb-1">{product.brand} • {product.category}</p>
          <p className="text-xs text-gray-600 line-clamp-2">{product.description}</p>
        </div>
        
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <div className="flex items-center">
              <Star className="w-4 h-4 text-yellow-400 fill-current" />
              <span className="text-sm font-medium text-gray-700 ml-1">{product.rating}</span>
            </div>
            <span className="text-xs text-gray-500">({product.reviews})</span>
          </div>
          <span className={`text-xs px-2 py-1 rounded-full ${
            product.stock > 50 ? 'bg-green-100 text-green-800' :
            product.stock > 20 ? 'bg-yellow-100 text-yellow-800' :
            'bg-red-100 text-red-800'
          }`}>
            {product.stock} left
          </span>
        </div>
        
        {showAdvanced && isRecommendation && (
          <div className="mb-3 p-2 bg-gray-50 rounded-lg">
            <div className="text-xs text-gray-600 mb-1">Model Confidence:</div>
            <div className="space-y-1">
              {Object.entries(product.modelScores || {}).map(([model, score]) => (
                <div key={model} className="flex justify-between text-xs">
                  <span className="capitalize">{model}:</span>
                  <span className="font-medium">{(score * 100).toFixed(1)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
        
        <div className="flex items-center justify-between mb-4">
          <span className="text-xl font-bold text-blue-600">${product.price}</span>
          {isRecommendation && (
            <div className="text-right">
              <div className="text-xs text-green-600 font-medium">
                {Math.round((product.confidence || 0.5) * 100)}% match
              </div>
              <div className="text-xs text-gray-500">AI Score</div>
            </div>
          )}
        </div>
        
        <div className="space-y-2">
          <div className="flex gap-2">
            <button
              onClick={() => recordAdvancedInteraction(product.id, 'view')}
              className="flex-1 bg-gray-100 text-gray-700 px-3 py-2 rounded-lg text-sm hover:bg-gray-200 transition-colors flex items-center justify-center"
            >
              <Eye className="w-4 h-4 mr-1" />
              View
            </button>
            <button
              onClick={() => recordAdvancedInteraction(product.id, 'like')}
              className="bg-red-100 text-red-600 px-3 py-2 rounded-lg text-sm hover:bg-red-200 transition-colors"
            >
              <Heart className="w-4 h-4" />
            </button>
            <button
              onClick={() => recordAdvancedInteraction(product.id, 'wishlist')}
              className="bg-yellow-100 text-yellow-600 px-3 py-2 rounded-lg text-sm hover:bg-yellow-200 transition-colors"
            >
              <Star className="w-4 h-4" />
            </button>
          </div>
          
          <button
            onClick={() => addToCart(product)}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg text-sm hover:from-blue-600 hover:to-purple-700 transition-all flex items-center justify-center"
          >
            <ShoppingCart className="w-4 h-4 mr-2" />
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );

  // Advanced Home View
  const AdvancedHomeView = () => (
    <div className="space-y-8">
      {/* Hero Section with Live Stats */}
      <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 text-white p-8 rounded-2xl relative overflow-hidden">
        <div className="absolute inset-0 bg-black bg-opacity-10"></div>
        <div className="relative z-10">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold mb-4 flex items-center">
                <Sparkles className="w-8 h-8 mr-3" />
                Advanced AI Commerce Platform
              </h1>
              <p className="text-xl opacity-90 mb-6">
                Next-generation recommendations powered by ensemble deep learning
              </p>
              {currentUser && (
                <div className="bg-white bg-opacity-20 p-4 rounded-xl">
                  <p className="font-medium text-lg">Welcome back, {currentUser.name}!</p>
                  <p className="text-sm opacity-80">
                    AI Model v{mlMetrics.modelVersion} • {mlMetrics.activeModels} models active
                  </p>
                </div>
              )}
            </div>
            
            <div className="text-right space-y-2">
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <div className="text-2xl font-bold">{analytics.liveUsers?.toLocaleString()}</div>
                <div className="text-sm opacity-80">Live Users</div>
              </div>
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <div className="text-2xl font-bold">{analytics.requestsPerSecond}</div>
                <div className="text-sm opacity-80">Req/sec</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Model Status Dashboard */}
      {currentUser && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
            <div className="flex items-center justify-between mb-3">
              <Brain className="w-8 h-8 text-purple-500" />
              <span className={`px-2 py-1 rounded text-xs font-medium ${
                modelTrainingStatus === 'completed' ? 'bg-green-100 text-green-800' :
                modelTrainingStatus === 'processing' ? 'bg-yellow-100 text-yellow-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {modelTrainingStatus}
              </span>
            </div>
            <div className="text-2xl font-bold text-gray-800">{mlMetrics.activeModels}</div>
            <div className="text-sm text-gray-600">AI Models Active</div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
            <div className="flex items-center justify-between mb-3">
              <Target className="w-8 h-8 text-green-500" />
              <Gauge className="w-5 h-5 text-gray-400" />
            </div>
            <div className="text-2xl font-bold text-gray-800">{(analytics.modelAccuracy * 100).toFixed(1)}%</div>
            <div className="text-sm text-gray-600">Model Accuracy</div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
            <div className="flex items-center justify-between mb-3">
              <Zap className="w-8 h-8 text-yellow-500" />
              <Activity className="w-5 h-5 text-gray-400" />
            </div>
            <div className="text-2xl font-bold text-gray-800">{mlMetrics.inferenceLatency}ms</div>
            <div className="text-sm text-gray-600">Response Time</div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
            <div className="flex items-center justify-between mb-3">
              <Award className="w-8 h-8 text-blue-500" />
              <TrendingUp className="w-5 h-5 text-gray-400" />
            </div>
            <div className="text-2xl font-bold text-gray-800">{(analytics.recommendationClickRate * 100).toFixed(1)}%</div>
            <div className="text-sm text-gray-600">Click Rate</div>
          </div>
        </div>
      )}

      {/* AI Recommendations Section */}
      {currentUser && (
        <div>
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-800 flex items-center">
                <Target className="w-7 h-7 mr-3 text-blue-500" />
                AI-Powered Recommendations
                {isLoading && <Zap className="w-6 h-6 ml-3 text-yellow-500 animate-pulse" />}
              </h2>
              <p className="text-gray-600 mt-1">
                Ensemble model combining collaborative filtering, content-based, and deep learning
              </p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => generateAdvancedRecommendations(currentUser.id)}
                className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors flex items-center"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </button>
            </div>
          </div>
          
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1,2,3,4,5,6].map(i => (
                <div key={i} className="bg-gray-200 animate-pulse rounded-xl h-80"></div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recommendations.map(product => (
                <EnhancedProductCard 
                  key={product.id} 
                  product={product} 
                  isRecommendation={true} 
                  showAdvanced={true}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Trending Products */}
      <div>
        <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center">
          <TrendingUp className="w-7 h-7 mr-3 text-green-500" />
          Trending Products
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {products.slice(0, 4).map(product => (
            <EnhancedProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </div>
  );

  // Products View
  const AdvancedProductsView = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-gray-800">Product Catalog</h2>
        <div className="flex items-center space-x-4">
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
          >
            <option value="all">All Categories</option>
            <option value="Electronics">Electronics</option>
            <option value="Clothing">Clothing</option>
            <option value="Sports">Sports</option>
            <option value="Food">Food</option>
          </select>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {filteredProducts.map(product => (
          <EnhancedProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );

  // Analytics View
  const AdvancedAnalyticsView = () => (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-gray-800 flex items-center">
        <BarChart3 className="w-7 h-7 mr-3 text-purple-500" />
        Advanced AI Analytics
      </h2>
      
      {/* Business Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: "Revenue Impact", value: `$${analytics.revenueImpact?.toLocaleString()}`, color: "green" },
          { label: "Model Accuracy", value: `${(analytics.modelAccuracy * 100).toFixed(1)}%`, color: "blue" },
          { label: "Conversion Rate", value: `${(analytics.conversionRate * 100).toFixed(1)}%`, color: "purple" },
          { label: "Daily Users", value: `${analytics.dailyActiveUsers?.toLocaleString()}`, color: "orange" }
        ].map((metric, idx) => (
          <div key={idx} className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
            <div className="text-2xl font-bold text-gray-800">{metric.value}</div>
            <div className="text-sm text-gray-600">{metric.label}</div>
          </div>
        ))}
      </div>

      {/* A/B Testing Results */}
      <div>
        <h3 className="text-xl font-semibold text-gray-800 mb-4">A/B Testing Experiments</h3>
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-medium text-gray-500">Experiment</th>
                  <th className="px-6 py-4 text-left text-sm font-medium text-gray-500">Status</th>
                  <th className="px-6 py-4 text-left text-sm font-medium text-gray-500">Improvement</th>
                  <th className="px-6 py-4 text-left text-sm font-medium text-gray-500">Confidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {experimentResults.map(experiment => (
                  <tr key={experiment.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-800">{experiment.name}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        experiment.status === 'completed' ? 'bg-green-100 text-green-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {experiment.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm font-medium text-green-600">{experiment.improvement}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{(experiment.confidence * 100).toFixed(0)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );

  // Cart View
  const AdvancedCartView = () => (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold text-gray-800 flex items-center">
        <ShoppingCart className="w-7 h-7 mr-3" />
        Shopping Cart ({cart.length} items)
      </h2>
      
      {cart.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-xl shadow-lg">
          <ShoppingCart className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p className="text-gray-500 text-lg">Your cart is empty</p>
        </div>
      ) : (
        <div className="space-y-4">
          {cart.map(item => (
            <div key={item.id} className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <span className="text-3xl">{item.image}</span>
                  <div>
                    <h3 className="font-semibold text-lg">{item.name}</h3>
                    <p className="text-gray-600">{item.brand} • {item.category}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xl font-bold text-blue-600">${item.price}</p>
                  <p className="text-gray-600">Qty: {item.quantity}</p>
                  <p className="text-lg font-bold">${(item.price * item.quantity).toFixed(2)}</p>
                </div>
              </div>
            </div>
          ))}
          
          <div className="bg-blue-50 p-6 rounded-xl">
            <div className="flex justify-between items-center">
              <span className="text-xl font-bold">Total: ${cart.reduce((sum, item) => sum + (item.price * item.quantity), 0).toFixed(2)}</span>
              <button 
                onClick={() => {
                  cart.forEach(item => recordAdvancedInteraction(item.id, 'purchase'));
                  addNotification('🎉 Order placed successfully!', 'success');
                  setCart([]);
                }}
                className="bg-gradient-to-r from-green-500 to-blue-600 text-white px-6 py-3 rounded-lg text-lg font-medium hover:from-green-600 hover:to-blue-700 transition-all"
              >
                Checkout
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Enhanced Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900 flex items-center">
                <Brain className="w-6 h-6 mr-2 text-blue-500" />
                Smart Commerce AI
              </h1>
              <span className="ml-3 text-xs bg-gradient-to-r from-purple-500 to-pink-500 text-white px-2 py-1 rounded-full">
                v{mlMetrics.modelVersion}
              </span>
            </div>
            
            <div className="flex-1 max-w-lg mx-8">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search products with AI assistance..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Notifications */}
              <div className="relative">
                <button className="p-2 text-gray-600 hover:text-gray-900 relative">
                  <Bell className="w-6 h-6" />
                  {notifications.length > 0 && (
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {notifications.length}
                    </span>
                  )}
                </button>
                
                {notifications.length > 0 && (
                  <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                    <div className="p-4">
                      <h3 className="text-sm font-medium text-gray-800 mb-3">Notifications</h3>
                      <div className="space-y-2">
                        {notifications.map(notification => (
                          <div key={notification.id} className={`p-3 rounded-lg text-sm ${
                            notification.type === 'success' ? 'bg-green-50 text-green-800' :
                            notification.type === 'error' ? 'bg-red-50 text-red-800' :
                            'bg-blue-50 text-blue-800'
                          }`}>
                            {notification.message}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Cart */}
              <button
                onClick={() => setCurrentView('cart')}
                className="relative p-2 text-gray-600 hover:text-gray-900"
              >
                <ShoppingCart className="w-6 h-6" />
                {cart.length > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {cart.length}
                  </span>
                )}
              </button>
              
              {/* User Menu */}
              {currentUser ? (
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2">
                    <User className="w-6 h-6 text-gray-600" />
                    <div>
                      <span className="text-sm font-medium">{currentUser.name}</span>
                      <div className="text-xs text-gray-500">{currentUser.type}</div>
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      setCurrentUser(null);
                      setRecommendations([]);
                      addNotification('👋 Logged out successfully', 'info');
                    }}
                    className="text-xs text-gray-500 hover:text-gray-700 px-3 py-1 rounded border border-gray-300"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <div className="flex space-x-2">
                  {users.map(user => (
                    <button
                      key={user.id}
                      onClick={() => handleUserLogin(user)}
                      className="text-xs bg-gradient-to-r from-blue-500 to-purple-600 text-white px-3 py-2 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all"
                    >
                      {user.name.split(' ')[0]}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Enhanced Navigation */}
      <nav className="bg-gray-100 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { key: 'home', label: 'AI Dashboard', icon: Brain },
              { key: 'products', label: 'Products', icon: Package },
              { key: 'analytics', label: 'Analytics', icon: BarChart3 }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setCurrentView(tab.key)}
                className={`py-4 px-2 border-b-2 font-medium text-sm flex items-center ${
                  currentView === tab.key
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <tab.icon className="w-4 h-4 mr-2" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentView === 'home' && <AdvancedHomeView />}
        {currentView === 'products' && <AdvancedProductsView />}
        {currentView === 'analytics' && <AdvancedAnalyticsView />}
        {currentView === 'cart' && <AdvancedCartView />}
      </main>

      {/* Enhanced Footer with Live Stats */}
      <footer className="bg-gray-800 text-white py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h3 className="text-lg font-semibold mb-2 flex items-center">
                <Cpu className="w-5 h-5 mr-2" />
                Live AI Performance
              </h3>
              <div className="space-y-1 text-sm">
                <div>🎯 Model Accuracy: {(analytics.modelAccuracy * 100).toFixed(1)}%</div>
                <div>⚡ Response Time: {mlMetrics.inferenceLatency}ms</div>
                <div>🔄 Cache Hit Rate: {(analytics.cacheHitRate * 100).toFixed(1)}%</div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-2 flex items-center">
                <Users className="w-5 h-5 mr-2" />
                User Engagement
              </h3>
              <div className="space-y-1 text-sm">
                <div>👥 Live Users: {analytics.liveUsers?.toLocaleString()}</div>
                <div>📈 CTR: {(analytics.recommendationClickRate * 100).toFixed(1)}%</div>
                <div>💰 Revenue Impact: ${analytics.revenueImpact?.toLocaleString()}</div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-2 flex items-center">
                <Activity className="w-5 h-5 mr-2" />
                System Health
              </h3>
              <div className="space-y-1 text-sm">
                <div>🔥 Requests/sec: {analytics.requestsPerSecond}</div>
                <div>🎲 Models Active: {mlMetrics.activeModels}</div>
                <div>📊 Experiments: {experimentResults.length} running</div>
              </div>
            </div>
          </div>
          
          <div className="mt-6 pt-6 border-t border-gray-700 text-center text-sm text-gray-400">
            🚀 Advanced AI E-Commerce Platform | Real-time ML recommendations with ensemble deep learning
          </div>
        </div>
      </footer>
    </div>
  );
};

export default AdvancedEcommerceAI;