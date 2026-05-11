# KickLiveArchiver

KickLiveArchiver adalah aplikasi untuk merekam siaran live streaming Kick.com secara otomatis, dengan antarmuka grafis berbasis CustomTkinter dan dukungan remux hasil rekaman.

## Fitur
- Monitoring otomatis status live channel Kick.com
- Rekam otomatis saat channel live
- Remux hasil rekaman
- Antarmuka GUI modern (CustomTkinter)
- Integrasi dengan ffmpeg

## Instalasi

1. **Clone repository ini:**
   ```bash
   git clone <repo-url>
   cd KickLiveArchiver
   ```

2. **Buat dan aktifkan virtual environment (opsional tapi direkomendasikan):**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   Pastikan sudah menginstall:
   - Python 3.8+
   - [ffmpeg](https://ffmpeg.org/) (sudah disediakan di folder `ffmpeg/`)
   - [streamlink](https://streamlink.github.io/)
   - [customtkinter](https://github.com/TomSchimansky/CustomTkinter)

   Install dependencies utama:
   ```bash
   pip install streamlink customtkinter
   ```

4. **Jalankan aplikasi:**
   ```bash
   python main.py
   ```

## Build ke EXE (Windows)

Aplikasi ini sudah disiapkan untuk dibuild menggunakan PyInstaller.

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build executable:
   ```bash
   pyinstaller KickLiveArchiver.spec
   ```

3. Hasil build ada di folder `dist/KickLiveArchiver/`

## Struktur Folder Penting
- `main.py` : Entry point aplikasi
- `ui.py` : Antarmuka pengguna
- `monitor.py` : Monitoring status live
- `recorder.py` : Proses rekaman
- `remux.py` : Remux hasil rekaman
- `ffmpeg/` : Binary ffmpeg
- `assets/` : Asset tambahan
- `output/` : Hasil rekaman

## Konfigurasi
- Edit file `config.json` untuk pengaturan channel, output, dsb.

## Lisensi
Lihat file LICENSE untuk detail lisensi.

---

**Kontribusi dan saran sangat diterima!**
