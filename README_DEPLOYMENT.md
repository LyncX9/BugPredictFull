# 🚀 Bug Prediction API - Deployment Guide

Model machine learning untuk prediksi bug berdasarkan code complexity metrics.

## 📋 Prerequisites

- Python 3.10+
- Model file: `best_model.joblib` dan `feature_names.joblib`

## 🔧 Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## 🌐 REST API (untuk Vue.js Integration)

### Start Server

```bash
# Development mode (auto-reload)
uvicorn app:app --reload

# Production mode
uvicorn app:app --host 0.0.0.0 --port 8000
```

Server akan running di: **http://localhost:8000**

### API Documentation

Buka browser: **http://localhost:8000/docs** untuk interactive API docs (Swagger UI)

### Endpoints

#### 1. Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "model": "loaded",
  "timestamp": "2026-01-14T19:19:26"
}
```

#### 2. Single Prediction
```bash
POST /predict
Content-Type: application/json

{
  "radon_total_complexity": 60,
  "radon_num_items": 29,
  "pylint_msgs_count": 32,
  "pylint_rc": 30,
  "bandit_issues_count": 1,
  "bandit_rc": 1
}
```

Response:
```json
{
  "is_bug": true,
  "confidence": 89.5,
  "probabilities": {
    "no_bug": 0.105,
    "bug": 0.895
  },
  "metrics": { ... }
}
```

#### 3. Batch Prediction
```bash
POST /predict/batch
Content-Type: application/json

{
  "items": [
    { "radon_total_complexity": 60, ... },
    { "radon_total_complexity": 10, ... }
  ]
}
```

### Vue.js Integration Example

```javascript
// Vue.js axios example
async predictBug(metrics) {
  try {
    const response = await axios.post('http://localhost:8000/predict', {
      radon_total_complexity: metrics.complexity,
      radon_num_items: metrics.items,
      pylint_msgs_count: metrics.pylint,
      pylint_rc: metrics.pylintRc,
      bandit_issues_count: metrics.bandit,
      bandit_rc: metrics.banditRc
    });
    
    console.log('Prediction:', response.data.is_bug);
    console.log('Confidence:', response.data.confidence);
    return response.data;
  } catch (error) {
    console.error('Prediction failed:', error);
  }
}
```

## 🖥️ Python Script (Standalone)

### Import dalam Code

```python
from predict import BugPredictor

# Initialize
predictor = BugPredictor()

# Single prediction
result = predictor.predict_single({
    'radon_total_complexity': 60,
    'radon_num_items': 29,
    'pylint_msgs_count': 32,
    'pylint_rc': 30,
    'bandit_issues_count': 1,
    'bandit_rc': 1
})

print(f"Bug: {result['is_bug']}, Confidence: {result['confidence']:.2f}%")
```

### CLI Usage

#### Single Prediction (Interactive)
```bash
python predict.py --single
```

#### Batch Prediction dari CSV
```bash
# Input CSV harus punya columns: radon_total_complexity, radon_num_items, dll
python predict.py --csv input.csv --output results.csv
```

## 🔒 CORS Configuration

Untuk production, edit `app.py` line 26:

```python
# Development (allow all origins)
allow_origins=["*"]

# Production (specific domain)
allow_origins=["https://yourdomain.com"]
```

## 🐛 Troubleshooting

### Error: Model not loaded
- Pastikan file `best_model.joblib` dan `feature_names.joblib` ada di directory yang sama
- Check file permissions

### CORS Error di Browser
- Pastikan CORS middleware sudah enabled di `app.py`
- Untuk development, gunakan `allow_origins=["*"]`

### Port already in use
```bash
# Gunakan port lain
uvicorn app:app --port 8001
```

## 📊 Input Features

API menerima 6 metrics:

1. **radon_total_complexity** - Total cyclomatic complexity
2. **radon_num_items** - Number of code items  
3. **pylint_msgs_count** - Pylint messages count
4. **pylint_rc** - Pylint return code
5. **bandit_issues_count** - Bandit security issues
6. **bandit_rc** - Bandit return code

## 🎯 Response Format

- **is_bug**: boolean - True jika diprediksi ada bug
- **confidence**: float (0-100) - Confidence percentage
- **probabilities**: dict - Probability untuk tiap class
- **metrics**: dict - Input metrics yang digunakan

## 📞 Support

Untuk issues atau questions, check API docs di `/docs` endpoint.
