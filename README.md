# TikTok Profile Scanner (No Login Required)

Alat berbasis Python untuk melakukan ekstraksi data profil TikTok melalui antarmuka web publik. Program ini dirancang untuk mengambil informasi statistik akun dan mengunduh foto profil dalam resolusi tinggi tanpa memerlukan proses autentikasi.

## Fitur Utama

- **Ekstraksi Data Publik:** Mengambil informasi tanpa memerlukan kredensial login.
- **Informasi Komprehensif:** Menampilkan Username, Nama, Jumlah Pengikut, Mengikuti, Total Suka, Status Verifikasi, dan Bio.
- **Pratinjau Terminal:** Menampilkan pratinjau foto profil langsung pada konsol menggunakan TrueColor ANSI.
- **Pengunduh Kualitas HD:** Algoritma otomatis untuk mencari dan mengunduh foto profil dengan resolusi maksimal (hingga 1080x1080).
- **Manajemen File:** Penyimpanan otomatis hasil unduhan ke dalam direktori terorganisir dengan penamaan file berbasis timestamp.

### 1. Informasi Profil (Terminal Output)
Data yang berhasil diambil dari skrip meliputi:
- **Username:** ID unik pengguna TikTok.
- **Nama Lengkap:** Nama tampilan (nickname) yang digunakan profil.
- **Statistik Akun:**
  - Jumlah Pengikut (Followers).
  - Jumlah Mengikuti (Following).
  - Total Suka (Total Likes) yang diterima dari seluruh konten.
- **Status Verifikasi:** Informasi apakah akun tersebut merupakan akun centang biru (Verified).
- **Bio/Deskripsi:** Teks biografi singkat yang tertera pada profil.

## Prasyarat Sistem

- **Python:** Versi 3.8 atau lebih tinggi.
- **Playwright:** Library untuk otomatisasi browser.
- **Pillow (PIL):** Library untuk pengolahan citra digital.
- **Requests:** Library untuk pengiriman permintaan HTTP.

## Panduan Instalasi

1. Kloning repositori ini:
   ```bash
   git clone https://github.com/prawira-rexsa/tiktok-profile-scanner
   cd tiktok-profile-scanner
   python tiktokStalk.py
