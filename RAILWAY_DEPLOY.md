# 🚂 Railway Deployment Guide

Panduan lengkap deployment aplikasi ke Railway.app.

## 📋 Prerequisites

1. Akun [GitHub](https://github.com/)
2. Akun [Railway.app](https://railway.app/) (Bisa login via GitHub)
3. Git terinstall di komputer

## 🚀 Steps to Deploy

### 1. Push Code to GitHub

Pastikan semua file sudah di-push ke repository GitHub:
- `app.py`
- `requirements.txt`
- `Procfile`
- `runtime.txt`
- `best_model.joblib` (Pastikan Git LFS aktif jika file > 100MB)
- `feature_names.joblib`

```bash
git init
git add .
git commit -m "Deploy to Railway"
git branch -M main
git remote add origin https://github.com/LyncX9/predict_defects.git
git push -u origin main
```

### 2. Setup di Railway

1. Login ke [Railway Dashboard](https://railway.app/dashboard)
2. Click **New Project** -> **Deploy from GitHub repo**
3. Pilih repository `predict_defects`
4. Click **Deploy Now**

### 3. Configuration (Optional but Recommended)

Di Dashboard Project Railway -> Settings -> Variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `ALLOWED_ORIGINS` | `https://your-frontend.com` | Domain frontend Vue.js (default: `*`) |
| `PORT` | `8000` | Port aplikasi (Railway set otomatis) |

### 4. Generate Public Domain

1. Pergi ke tab **Settings** -> **Networking**
2. Click **Generate Domain**
3. Copy URL yang muncul (contoh: `bug-prediction-production.up.railway.app`)

URL ini yang akan dipakai di frontend Vue.js!

## 🧪 Verification

Buka URL public di browser:
`https://[YOUR-RAILWAY-URL]/health`

Response:
```json
{
  "status": "healthy",
  "model": "loaded"
}
```

## ⚠️ Troubleshooting

**Build Failed: Python version error**
- Cek `runtime.txt`, pastikan version supported

**Model not found**
- Pastikan file `.joblib` ter-upload ke GitHub
- Cek log deployment di Railway

**Start Command failed**
- Cek `Procfile` pastikan command benar: `web: uvicorn app:app --host 0.0.0.0 --port $PORT`
