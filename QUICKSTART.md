# 🚀 Quick Start Guide - Bug Prediction API

## ⚡ Start API Server (3 detik!)

```bash
cd c:\dataset
uvicorn app:app --reload
```

✅ Server running di: **http://localhost:8000**  
📚 API Docs: **http://localhost:8000/docs**

## 🧪 Test dari Vue.js

```javascript
// Di Vue component:
async predictBug() {
  const response = await axios.post('http://localhost:8000/predict', {
    radon_total_complexity: 60,
    radon_num_items: 29,
    pylint_msgs_count: 32,
    pylint_rc: 30,
    bandit_issues_count: 1,
    bandit_rc: 1
  });
  
  console.log('Bug:', response.data.is_bug);        // true/false
  console.log('Confidence:', response.data.confidence); // 0-100%
}
```

## 🐍 Test dengan Python

```bash
python test_predict.py
```

## 📁 Files Created

- ✅ `app.py` - FastAPI REST API
- ✅ `predict.py` - Standalone prediction script  
- ✅ `requirements.txt` - Dependencies
- ✅ `README_DEPLOYMENT.md` - Full documentation
- ✅ `test_api.html` - Browser testing page
- ✅ `test_predict.py` - Python test script

## 🔥 What's Next?

1. **Start server**: `uvicorn app:app --reload`
2. **Test di browser**: Buka `test_api.html` di browser
3. **Integrate ke Vue.js**: Copy code example di atas
4. **Read docs**: Check `README_DEPLOYMENT.md` untuk details

---

**Need help?** Check full documentation di `README_DEPLOYMENT.md`
