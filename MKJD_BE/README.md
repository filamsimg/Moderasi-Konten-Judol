# MKJD_BE

Backend FastAPI untuk sistem moderasi komentar judi online.

## Prasyarat
- Python 3.10+
- PostgreSQL (disarankan; SQLite bisa untuk dev)

## Quick start (Makefile)
Setup dependensi + run API (sekali jalan):
```bash
make dev
```

Jika ingin inference model BERT lokal:
```bash
make dev-ml
```

Catatan: `make dev` hanya install dependencies saat pertama kali atau ketika `requirements-core.txt` berubah.

## Migrasi DB (Alembic)
Jalankan migrasi:
```bash
alembic upgrade head
```

## Seed data default
```bash
python app/seed.py
```

Seed sample untuk testing:
```bash
python app/seed.py --sample
```

## Setup manual
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements-core.txt
```

Jika ingin inference model BERT lokal:
```bash
pip install -r requirements-ml.txt
```

Salin env:
```bash
copy .env.example .env
```

Jalankan API:
```bash
python -m uvicorn app.main:app --reload
```

## PostgreSQL via Docker
Jalankan API + database lokal:
```bash
docker compose up -d
```

API akan tersedia di `http://localhost:8000`.

Pastikan `DATABASE_URL` mengarah ke Postgres, lalu migrasi:
```bash
alembic upgrade head
```

## Makefile (Docker + DB)
Jalankan API + Postgres:
```bash
make docker-up
```

Hentikan layanan:
```bash
make docker-down
```

Rebuild DB dari nol + migrasi + seed sample:
```bash
make docker-fresh
```

## Postman
Import collection:
```
postman/MKJD_BE.postman_collection.json
```

## Struktur
- `app/main.py`: entrypoint FastAPI
- `app/db`: koneksi DB dan model
- `app/api/v1`: endpoint API
- `app/services`: logika bisnis, normalisasi, inference
- `app/workers`: job polling YouTube (placeholder)

## Catatan model
- Model BERT default diarahkan ke `./models/model_judol_bert`.
- Aktifkan dengan `MODEL_ENABLED=true` di `.env`.

## OAuth YouTube (setup FE)
Isi env berikut:
```
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REDIRECT_URI=http://localhost:8000/v1/oauth/youtube/callback
FRONTEND_URL=http://localhost:3000/setup
```

Flow singkat:
- FE panggil `GET /v1/oauth/youtube/connect` lalu redirect ke Google.
- Google redirect ke `YOUTUBE_REDIRECT_URI`, BE simpan token lalu redirect ke `FRONTEND_URL?oauth=success`.
- FE lanjut ambil kanal dari `GET /v1/oauth/youtube/channels`.

## Model dari Google Drive
Unduh model dari folder Drive ini:
```
https://drive.google.com/drive/folders/1yo4KrugTmAWwmtx0Lv23qLjlXZikzYdp?usp=drive_link
```

Simpan hasil download ke:
```
MKJD_BE/models/model_judol_bert/
```

Lalu set `.env`:
```
MODEL_ENABLED=true
MODEL_PATH=./models/model_judol_bert
```
