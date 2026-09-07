# 🌻 Sunflower Land - Telegram Mini App (TMA) & Web3 Bot

Proyek ini adalah implementasi lengkap sistem **Telegram Mini App (TMA)** berbasis **Python** (`python-telegram-bot` v20+ Async) dan **Web Frontend** (HTML5, Tailwind CSS, Ethers.js) untuk memainkan game Web3 Metaverse **[Sunflower Land](https://sunflower-land.com)** langsung di dalam obrolan Telegram secara *fullscreen*, responsif, dan real-time.

---

## 📁 Struktur Direktori Proyek

```text
.
├── public/
│   └── index.html          # Frontend Telegram Mini App (Iframe game, Web3 modal, HUD)
├── main.py                 # Backend Telegram Bot (Async python-telegram-bot v20+)
├── requirements.txt        # Dependensi Python (python-telegram-bot, httpx, python-dotenv)
├── vercel.json             # Konfigurasi deployment 1-klik ke Vercel (HTTPS)
├── .env                    # Variabel environment & token bot (aktif)
├── .env.example            # Template variabel environment
└── README.md               # Dokumentasi dan panduan deployment lengkap
```

---

## 🚀 Fitur Utama

1. **Frontend TMA (Web3 & Responsive):**
   - **Layar Penuh (Fullscreen):** Menggunakan `Telegram.WebApp.expand()` & `Telegram.WebApp.ready()` resmi dari Telegram SDK.
   - **Game Iframe Responsif:** Memuat game Sunflower Land (`https://sunflower-land.com/play/`) dengan dukungan hardware acceleration, pointer-lock, dan sandbox yang aman.
   - **Koneksi Web3 Wallet (Polygon PoS - Chain ID 137):** Terintegrasi dengan deteksi injected wallet (`window.ethereum`, MetaMask, OKX Wallet, Trust Wallet) dan deep link universal untuk mobile.
   - **Overlay HUD Interaktif:** Dilengkapi status indikator game online, pemantau saldo POL (Polygon gas), tombol toggle fullscreen/HUD, tombol reload frame, dan tombol switcher ke situs resmi.
   - **Live Token Tracker $SFL:** Memeriksa harga token Sunflower Land ($SFL) dalam USD & IDR secara real-time via API CoinGecko.

2. **Backend Telegram Bot:**
   - Dibuat dengan arsitektur asynchronous `python-telegram-bot` v20+.
   - Command `/start`: Kartu sambutan interaktif dengan tombol `InlineKeyboardButton` bertipe `web_app`.
   - Command `/farm` atau `/play`: Akses kilat peluncur game Sunflower Land.
   - Command `/status`: Memeriksa latensi server Sunflower Land (ping ms) dan harga live token $SFL dari CoinGecko.
   - Command `/wallet`: Panduan pengaturan wallet Polygon PoS.
   - Command `/help`: Panduan lengkap perintah dan gameplay.
   - Otomatis mendaftarkan daftar command dan `MenuButtonWebApp` ke Telegram.

---

## ⚙️ Persiapan & Instalasi Backend

### 1. Prasyarat
- Python 3.10 atau versi lebih baru
- Pip

### 2. Instal Dependensi
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi `.env`
Pastikan file `.env` telah dikonfigurasi:
```env
TELEGRAM_BOT_TOKEN=8972855558:AAG-gayE-PG5YaOK941EhtsvcItsj_-OGA4
WEBAPP_URL=https://sunflower-tma.vercel.app
SUNFLOWER_GAME_URL=https://sunflower-land.com/play/
```
> **Catatan:** Ganti nilai `WEBAPP_URL` dengan URL HTTPS frontend Anda setelah dideploy (lihat panduan hosting di bawah).

### 4. Menjalankan Bot
```bash
python3 main.py
```

---

## 🌐 Panduan Hosting Gratis Frontend (Wajib HTTPS)

Telegram Mini App **mewajibkan protokol HTTPS** dengan sertifikat SSL valid. Anda dapat menghosting folder `public/` secara gratis menggunakan salah satu penyedia berikut:

### Opsi A: Vercel (Direkomendasikan - Paling Cepat)
File konfigurasi `vercel.json` sudah tersedia di dalam proyek ini.

1. **Deploy via Vercel CLI:**
   ```bash
   npm i -g vercel
   vercel --prod
   ```
2. **Deploy via GitHub:**
   - Push repository ini ke akun GitHub Anda.
   - Masuk ke [vercel.com](https://vercel.com).
   - Klik **"Add New Project"** &rarr; Pilih repository ini.
   - Framework Preset: **Other**. Root directory: `./` (Vercel otomatis membaca `vercel.json` dan folder `public`).
   - Klik **Deploy**.
   - Salin URL domain HTTPS yang diberikan (contoh: `https://sunflower-tma.vercel.app`).

### Opsi B: Cloudflare Pages (Gratis & Cepat)
1. Buka [Cloudflare Dashboard](https://dash.cloudflare.com/) &rarr; **Workers & Pages** &rarr; **Create application** &rarr; **Pages**.
2. Hubungkan ke repository GitHub Anda.
3. Build output directory: `public`.
4. Klik **Save and Deploy**. Cloudflare Pages akan memberikan domain HTTPS gratis (contoh: `https://sunflower-land.pages.dev`).

### Opsi C: Pengujian Lokal dengan Cloudflare Tunnel / Ngrok
Jika ingin menguji lokal dari laptop/PC Anda tanpa deploy:
```bash
# Jalankan web server lokal di folder public
python3 -m http.server 8080 --directory public

# Di terminal lain, buka tunnel HTTPS gratis
npx localtunnel --port 8080
# atau
cloudflared tunnel --url http://localhost:8080
```
Salin URL `https://...` yang dihasilkan ke file `.env` pada variabel `WEBAPP_URL`.

---

## 🤖 Panduan Konfigurasi di @BotFather

Ikuti langkah-langkah berikut di aplikasi Telegram untuk menghubungkan Mini App ke bot Anda:

1. Buka Telegram dan cari **[@BotFather](https://t.me/BotFather)**.
2. Ketik `/mybots` dan pilih bot Anda (misalnya **`@DbsRza_bot`**).

### A. Mengatur Menu Button (Tombol WebApp di Samping Kolom Chat)
1. Di menu bot pada BotFather, pilih **Bot Settings** &rarr; **Menu Button** &rarr; **Configure menu button**.
2. Kirim URL WebApp HTTPS Anda (contoh: `https://sunflower-tma.vercel.app`).
3. Kirim teks tombol yang ingin ditampilkan: `🌻 Play SFL`.
4. Selesai! Sekarang di obrolan bot, pengguna akan melihat tombol permanen di samping kolom pesan untuk membuka game dalam satu klik.

### B. Mendaftarkan Mini App Resmi (`/newapp`)
Jika Anda ingin bot memiliki link peluncur resmi `t.me/DbsRza_bot/app`:
1. Di `@BotFather`, ketik `/newapp`.
2. Pilih bot Anda (`@DbsRza_bot`).
3. Masukkan judul app: `Sunflower Land TMA`.
4. Masukkan deskripsi pendek: `Mainkan game metaverse Web3 Sunflower Land langsung di Telegram!`.
5. Unggah foto avatar/ikon Mini App (resolusi 640x640 px).
6. (Opsional) Kirim animasi GIF (resolusi 640x360 px) atau ketik `/empty`.
7. Masukkan WebApp URL: `https://sunflower-tma.vercel.app`.
8. Tentukan short name (nama link): `game` atau `play`.
9. Link peluncur Mini App Anda sekarang aktif di: `https://t.me/DbsRza_bot/game`.

---

## 🎮 Cara Penggunaan Bot

1. Buka obrolan dengan bot di Telegram: **[@DbsRza_bot](https://t.me/DbsRza_bot)**.
2. Kirim perintah `/start`.
3. Klik tombol **"🌻 Buka Sunflower Land (TMA)"**.
4. Game akan langsung terbuka secara fullscreen di layar Telegram Anda.
5. Hubungkan wallet crypto (Polygon PoS) untuk menyimpan progres farming dan bertransaksi item NFT.
6. Ketik `/status` untuk mengecek harga token $SFL dan konektivitas server.

---

## 📜 Smart Contract & Jaringan
- **Blockchain:** Polygon PoS (Chain ID: `137`)
- **Native Gas Token:** `POL` (dahulu `MATIC`)
- **Sunflower Land Token ($SFL):** `0xd1f9c58e33933a9970353798ac555049721a5948`
- **Situs Resmi:** [sunflower-land.com](https://sunflower-land.com)
- **Dokumentasi Sunflower Land:** [docs.sunflower-land.com](https://docs.sunflower-land.com)
