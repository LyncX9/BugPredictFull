# 🚀 Cara Menjalankan DefectScanner Project

## Prerequisites
- PHP 8.2+ terinstall
- Composer terinstall
- Node.js 18+ dan npm terinstall
- Python 3 terinstall (untuk script extract_metrics.py)

## Langkah 1: Setup Backend (Laravel)

### 1.1 Install Dependencies
```bash
cd backend
composer install
```

### 1.2 Setup Environment File
```bash
# Copy file .env.example ke .env (jika belum ada)
cp .env.example .env

# Generate application key
php artisan key:generate
```

### 1.3 Setup Database
```bash
# Pastikan database SQLite sudah ada
# Jika belum, buat file database.sqlite di folder database/
touch database/database.sqlite

# Jalankan migration
php artisan migrate
```

### 1.4 Jalankan Backend Server
```bash
php artisan serve
```
Backend akan berjalan di: **http://127.0.0.1:8000**

---

## Langkah 2: Setup Frontend (Vue.js)

### 2.1 Install Dependencies
Buka terminal baru:
```bash
cd frontend
npm install
```

### 2.2 Jalankan Frontend Development Server
```bash
npm run dev
```
Frontend akan berjalan di: **http://localhost:5173** (atau port lain yang tersedia)

---

## Langkah 3: Testing Aplikasi

### 3.1 Buka Browser
Buka browser dan akses: **http://localhost:5173**

### 3.2 Test Fitur-fitur:
1. ✅ **Upload File Python** - Klik "Upload New Scan" dan upload file .py
2. ✅ **Lihat Scan History** - Klik "Scan History" untuk melihat daftar scan
3. ✅ **Filter Risk** - Coba filter berdasarkan risk level (All, High, Medium, Low)
4. ✅ **Filter Days** - Coba filter berdasarkan date range (Today, 7 Days, 30 Days)
5. ✅ **Search** - Coba search berdasarkan nama file
6. ✅ **Latency Status** - Perhatikan status latency di sidebar (update setiap 5 detik)

---

## Troubleshooting

### Error: Database tidak ditemukan
```bash
cd backend
touch database/database.sqlite
php artisan migrate
```

### Error: Port sudah digunakan
- Backend: Ubah port dengan `php artisan serve --port=8001`
- Frontend: Vite akan otomatis mencari port lain, atau edit `vite.config.js`

### Error: CORS Error
Pastikan backend sudah berjalan di `http://127.0.0.1:8000`
Jika berbeda, update URL di:
- `frontend/src/components/Sidebar.vue`
- `frontend/src/views/Dashboard.vue`
- `frontend/src/views/Scanner.vue`

### Error: Migration Error
```bash
cd backend
php artisan migrate:fresh
```

### Error: Python Script tidak ditemukan
Pastikan file `extract_metrics.py` ada di folder `backend/`

---

## Struktur Project

```
web/
├── backend/          # Laravel Backend
│   ├── app/
│   ├── database/
│   ├── routes/
│   └── extract_metrics.py
│
└── frontend/         # Vue.js Frontend
    ├── src/
    │   ├── components/
    │   ├── views/
    │   └── router/
    └── package.json
```

---

## Command Cepat

### Menjalankan Semua (2 Terminal)

**Terminal 1 (Backend):**
```bash
cd backend && php artisan serve
```

**Terminal 2 (Frontend):**
```bash
cd frontend && npm run dev
```

---

## Catatan Penting

1. ⚠️ Pastikan **backend berjalan terlebih dahulu** sebelum frontend
2. ⚠️ Pastikan **migration sudah dijalankan** sebelum testing
3. ⚠️ File Python yang diupload harus berekstensi `.py`
4. ⚠️ API Prediction Railway harus tersedia untuk mendapatkan hasil scan yang lengkap

---

## Next Steps (Opsional)

1. **Setup Production Build:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Setup Queue Worker (jika perlu):**
   ```bash
   cd backend
   php artisan queue:work
   ```

3. **Setup Environment Variables:**
   Edit `backend/.env` untuk konfigurasi database, API keys, dll.

---

## Support

Jika ada masalah, cek:
- Console browser (F12) untuk error frontend
- Laravel logs di `backend/storage/logs/laravel.log`
- Terminal untuk error messages
