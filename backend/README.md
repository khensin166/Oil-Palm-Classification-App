# Palm Fruit Classification Backend

FastAPI backend for Oil Palm Fruit Classification using MobileNetV2.

## Prerequisites
- Python 3.10+
- Docker & Docker Compose (optional)

## Setup Local (tanpa Docker)

1. Buat virtual environment dan aktifkan:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux

   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Pastikan model dan class names ada di folder `models/`:
   - `models/model_mobilenetv2_sawit.keras`
   - `models/class_names.json`

4. Jalankan aplikasi:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Setup Docker

1. Jalankan menggunakan Docker Compose:
   ```bash
   docker compose up -d --build
   ```

2. Cek logs:
   ```bash
   docker compose logs -f
   ```

3. Hentikan container:
   ```bash
   docker compose down
   ```

## API Endpoints

- **GET /** : Cek apakah API berjalan
- **GET /health** : Cek status dan apakah model berhasil diload
- **POST /predict** : Endpoint untuk upload gambar dan mendapatkan hasil prediksi

### Test dengan cURL
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "image=@/path/to/your/image.jpg"
```
