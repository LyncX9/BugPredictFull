# DefectScanner Setup Guide

## Perubahan yang Telah Dilakukan

### Backend (Laravel)
1. ✅ **ScanController** - Ditambahkan filtering untuk risk level dan date range
2. ✅ **ScanController** - Ditambahkan endpoint `/api/latency` untuk real-time latency monitoring
3. ✅ **Scan Model** - Ditambahkan fillable fields dan proper casting
4. ✅ **Migration** - Ditambahkan kolom `file_path`, `defect_probability`, dan `risk_level`

### Frontend (Vue.js)
1. ✅ **Dashboard.vue** - Filter risk (all, high, medium, low) dan filter days (today, 7 days, 30 days)
2. ✅ **Dashboard.vue** - Pagination yang benar dengan responsive design
3. ✅ **Scanner.vue** - Preview file yang diupload (bukan hardcoded text)
4. ✅ **Scanner.vue** - Animasi scanning yang realistis seperti pada gambar
5. ✅ **Sidebar.vue** - Fetch latency real-time dari backend setiap 5 detik
6. ✅ **App.vue** - Responsive design untuk mobile dan desktop dengan mobile menu
7. ✅ **Style.css** - Animasi dan efek visual yang lebih baik

## Setup Instructions

### Backend Setup
```bash
cd backend
composer install
php artisan migrate
php artisan serve
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Menjalankan Migration Baru
```bash
cd backend
php artisan migrate
```

## Fitur yang Telah Diimplementasikan

### 1. Filter Risk Level
- All Risks (default)
- High Risk (≥70%)
- Medium Risk (30-69%)
- Low Risk (<30%)

### 2. Filter Date Range
- Today
- Last 7 Days
- Last 30 Days (default)

### 3. Real-time Latency Monitoring
- Endpoint: `GET /api/latency`
- Update otomatis setiap 5 detik
- Menampilkan status online/offline

### 4. File Preview
- Menampilkan konten file yang diupload
- Syntax highlighting untuk Python
- Highlight baris yang memiliki potensi defect

### 5. Scanning Animation
- Animasi scanning bar yang realistis
- Progress indicator dengan estimasi waktu
- Step-by-step scanning process

### 6. Responsive Design
- Mobile menu untuk layar kecil
- Grid layout yang responsif
- Touch-friendly interface

## API Endpoints

- `GET /api/scans` - List scans dengan filtering
  - Query params: `risk`, `days`, `search`, `page`
- `POST /api/scans` - Upload dan scan file
- `GET /api/scans/{id}` - Detail scan
- `GET /api/latency` - Get model latency status

## Catatan Penting

1. Pastikan Python script `extract_metrics.py` ada di root backend
2. Pastikan API prediction endpoint Railway tersedia
3. CORS sudah dikonfigurasi untuk development
4. Database menggunakan SQLite (default Laravel)
