# Palm Fruit Classification App

Aplikasi Flutter untuk mengklasifikasikan jenis buah sawit menggunakan kamera atau galeri.

## Setup & Menjalankan

1. Pastikan Flutter SDK telah terinstall.
2. Buka terminal di folder `mobile/`.
3. Jalankan `flutter pub get` untuk mengunduh dependencies.
4. Jalankan aplikasi di emulator atau device fisik:
   ```bash
   flutter run
   ```

## Mengganti URL Backend

Buka file `lib/services/prediction_service.dart`.
Ubah variabel `baseUrl` sesuai kebutuhan:

- **Android Emulator**: `http://10.0.2.2:8000`
- **Device Fisik/Real Device**: `http://<IP_LAPTOP>:8000` (pastikan laptop dan HP dalam satu jaringan WiFi yang sama).

## Dependencies
- `image_picker` : Untuk memilih gambar dari kamera atau galeri.
- `http` : Untuk mengirim HTTP multipart request ke backend.
- `mime` & `http_parser` : Untuk mengenali dan memparsing file gambar.
