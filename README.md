# Python Photo Booth 📸

Aplikasi photo booth interaktif yang dibuat dengan Python menggunakan OpenCV, Tkinter, dan PIL. Aplikasi ini memungkinkan Anda untuk mengambil foto dengan berbagai filter efek secara real-time menggunakan webcam.

![Python Photo Booth](https://img.shields.io/badge/Python-3.7%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Fitur Utama

- **Real-time Camera Preview**: Tampilan langsung dari webcam dengan efek mirror
- **Multiple Filters**: 7 filter berbeda untuk foto Anda
- **Countdown Timer**: Timer 3 detik sebelum foto diambil
- **Keyboard Shortcuts**: Kontrol cepat menggunakan keyboard
- **Auto Save**: Sistem penyimpanan otomatis dengan timestamp
- **User-friendly Interface**: Antarmuka yang mudah digunakan
- **Cross-platform**: Berjalan di Windows, macOS, dan Linux

## 🎨 Filter yang Tersedia

1. **Normal** - Tampilan standar tanpa filter
2. **Hitam Putih** - Efek grayscale klasik
3. **Sepia** - Efek vintage dengan tone coklat keemasan
4. **Kartun** - Efek kartun dengan edge detection
5. **Negatif** - Inverse color effect
6. **Blur** - Efek blur gaussian
7. **Deteksi Tepi** - Edge detection dengan Canny algorithm

## 🛠️ Persyaratan Sistem

### Hardware
- Webcam (built-in atau eksternal)
- RAM minimal 2GB
- Ruang penyimpanan 100MB+

### Software
- Python 3.7 atau lebih baru
- Sistem operasi: Windows 10+, macOS 10.14+, atau Linux Ubuntu 18.04+

## 📦 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/username/python-photo-booth.git
cd python-photo-booth
```

### 2. Install Dependencies
```bash
# Menggunakan pip
pip install opencv-python pillow numpy

# Atau menggunakan requirements.txt (jika tersedia)
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
python photo_booth.py
```

## 🚀 Cara Penggunaan

### Mengambil Foto
1. **Menggunakan Mouse**: Klik tombol "Ambil Foto (Space)"
2. **Menggunakan Keyboard**: Tekan tombol `Space`
3. Countdown 3 detik akan dimulai
4. Foto akan diambil otomatis setelah countdown selesai

### Mengubah Filter
1. Gunakan dropdown menu "Filter" di bagian bawah
2. Pilih filter yang diinginkan
3. Preview akan berubah secara real-time

### Menyimpan Foto
1. **Menggunakan Mouse**: Klik tombol "Simpan Foto (S)" setelah foto diambil
2. **Menggunakan Keyboard**: Tekan tombol `S`
3. Foto akan disimpan di folder `photo_booth_images/`

### Keyboard Shortcuts
- `Space` - Ambil foto
- `S` - Simpan foto terakhir

## 📁 Struktur File

```
python-photo-booth/
│
├── photo_booth.py          # File utama aplikasi
├── README.md              # Dokumentasi ini
├── requirements.txt       # Dependencies (opsional)
├── photo_booth_images/    # Folder penyimpanan foto (dibuat otomatis)
│   ├── photo_booth_normal_20241201_143022.jpg
│   ├── photo_booth_sepia_20241201_143055.jpg
│   └── ...
└── screenshots/           # Screenshot aplikasi (opsional)
    ├── main_interface.png
    └── filters_demo.png
```

## 🖥️ Screenshot

### Interface Utama
```
┌─────────────────────────────────────────────────┐
│                Camera Preview                    │
│            [Live Video Feed]                    │
│                                                 │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│ [Ambil Foto] [Filter: ▼] [Simpan Foto]         │
└─────────────────────────────────────────────────┘
│ Status: Siap untuk mengambil foto               │
└─────────────────────────────────────────────────┘
```

## 🔧 Konfigurasi

### Mengubah Resolusi Kamera
```python
# Di dalam class PhotoBooth.__init__()
self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

### Mengubah Folder Penyimpanan
```python
# Di dalam class PhotoBooth.__init__()
self.save_dir = "path/to/your/folder"
```

### Menambah Filter Baru
```python
# Tambahkan ke available_filters dictionary
self.available_filters = {
    # ... filter yang sudah ada
    "new_filter": "Nama Filter Baru"
}

# Implementasikan di apply_filter method
elif filter_name == "new_filter":
    # Kode filter Anda di sini
    return processed_frame
```

## 🚨 Troubleshooting

### Error: Modul 'cv2' belum terinstal
```bash
pip install opencv-python
```

### Error: Modul 'PIL' belum terinstal
```bash
pip install pillow
```

### Error: Tidak dapat mengakses kamera
- Pastikan webcam terhubung dengan benar
- Tutup aplikasi lain yang menggunakan kamera
- Coba ganti index kamera di `cv2.VideoCapture(0)` menjadi `cv2.VideoCapture(1)`

### Aplikasi berjalan lambat
- Tutup aplikasi lain yang berat
- Kurangi resolusi kamera
- Pastikan driver kamera up-to-date

### Foto tidak tersimpan
- Periksa permission folder
- Pastikan ada ruang penyimpanan yang cukup
- Coba jalankan sebagai administrator (Windows)

## 📊 Format File Output

Foto disimpan dengan format:
```
photo_booth_{filter}_{YYYYMMDD_HHMMSS}.jpg
```

Contoh:
- `photo_booth_normal_20241201_143022.jpg`
- `photo_booth_sepia_20241201_143055.jpg`
- `photo_booth_cartoon_20241201_143128.jpg`

## 🤝 Kontribusi

Kontribusi sangat diterima! Berikut cara berkontribusi:

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

### Ideas untuk Kontribusi
- Menambah filter baru
- Improve UI/UX
- Menambah fitur video recording
- Support untuk multiple camera
- Integrasi dengan social media
- Face detection dan auto-focus

## 📝 Changelog

### v1.0.0 (2024-12-01)
- Initial release
- Basic photo capture functionality
- 7 different filters
- Keyboard shortcuts
- Auto-save with timestamp

## 📄 License

Project ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail lengkap.

## 👨‍💻 Author

**Your Name**
- GitHub: [@adrptrp](https://github.com/adrptrp)
- Email: adrian.pp13124@gmail.com

## 🙏 Acknowledgments

- [OpenCV](https://opencv.org/) - Computer vision library
- [Pillow](https://pillow.readthedocs.io/) - Python Imaging Library
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI toolkit
- Community contributors dan testers

## 📞 Support

Jika Anda mengalami masalah atau memiliki pertanyaan:

1. Cek bagian [Troubleshooting](#-troubleshooting)
2. Buka [Issues](https://github.com/username/python-photo-booth/issues) di GitHub
3. Kirim email ke: adrian.pp13124@gmail.com

---

⭐ Jika project ini membantu Anda, silakan berikan star di GitHub!

**Happy Photo Taking! 📸✨**
