# MKJD Monorepo

Repositori ini berisi:
- `MKJD_BE`: Backend FastAPI
- `MKJD_FE`: Frontend Nuxt

## Quick start (root)
Backend:
```bash
make be-dev
```

Backend + model BERT lokal:
```bash
make be-dev-ml
```

Postgres (rebuild + seed):
```bash
make be-db-fresh
```

Frontend:
```bash
make fe-install
make fe-dev
```

## Catatan
- Detail BE ada di `MKJD_BE/README.md`.
- Detail FE ada di `MKJD_FE/README.md` (jika ada).
