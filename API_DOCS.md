# SmartCommerce AI Recommendation Engine API

## Base URL
- Development: `http://localhost:8000`
- Production: `https://api.smartcommerce.com`

## Authentication
Include API key in headers:
```
Authorization: Bearer <token>
Content-Type: application/json
```

## Core Endpoints

### 1. Recommendations

#### Get Personalized Recommendations
```http
GET /api/recommendations/{user_id}/
```

**Parameters:**
- `user_id` (int): User identifier
- `count` (int, optional): Number of recommendations (default: 10)

**Response:**
```json
{
  "user_id": 123,
  "recommendations": [
    {
      "product_id": 456,
      "product_name": "Wireless Headphones",
      "category": "Electronics",
      "price": 99.99,
      "confidence_score": 0.87,
      "algorithm": "hybrid_ensemble"
    }
  ],
  "count": 10
}
```

### 2. User Interactions

#### Record User Interaction
```http
POST /api/interaction/
```

**Request Body:**
```json
{
  "user_id": 123,
  "product_id": 456,
  "interaction_type": "purchase"
}
```

### 3. Real-time Events

#### Process Streaming Event
```http
POST /api/streaming-event/
```

**Request Body:**
```json
{
  "user_id": "123",
  "product_id": "456",
  "event_type": "view",
  "session_id": "session_abc123",
  "device_type": "mobile",
  "context": {}
}
```

### 4. A/B Testing

#### Create Experiment
```http
POST /api/ab-test/create/
```

**Request Body:**
```json
{
  "experiment_id": "rec_test_v1",
  "name": "Recommendation Algorithm Test",
  "variants": [
    {"name": "control", "config": {"algorithm": "collaborative"}},
    {"name": "treatment", "config": {"algorithm": "deep_learning"}}
  ],
  "traffic_allocation": {"control": 0.5, "treatment": 0.5},
  "success_metrics": ["click_through_rate", "conversion_rate"],
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-01-14T23:59:59Z",
  "minimum_sample_size": 1000
}
```

### 5. Performance Metrics

#### Get Real-time Metrics
```http
GET /api/performance-metrics/
```

**Response:**
```json
{
  "performance": {
    "total_requests": 12345,
    "average_latency_ms": 145,
    "cache_hit_rate": 0.93,
    "active_users": 2847
  },
  "realtime": {
    "recommendations_served_last_hour": 1234,
    "clicks_last_hour": 456,
    "ctr_last_hour": 0.37
  },
  "daily": {
    "recommendations_served": 50000,
    "recommendation_clicks": 18500,
    "click_through_rate": 0.37
  }
}
```

### 6. Model Management

#### Upload Dataset
```http
POST /api/upload-dataset/
```

**Form Data:**
- `file`: CSV file
- `dataset_type`: "interactions" | "items" | "users"

#### Train Enhanced Models
```http
POST /api/enhanced-train/
```

**Request Body:**
```json
{
  "dataset_ids": [1, 2, 3],
  "config": {
    "embedding_dim": 64,
    "learning_rate": 0.001,
    "epochs": 50
  }
}
```

#### Get Model Metrics
```http
GET /api/model-metrics/
```

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Invalid parameter",
  "details": "User ID must be a positive integer"
}
```

## Rate Limiting

- API endpoints: 100 requests/minute
- ML training: 10 requests/hour
- Bulk operations: 5 requests/hour

## Health Checks

```http
GET /health/
GET /ready/
```