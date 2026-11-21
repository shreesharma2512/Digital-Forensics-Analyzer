# Digital Forensics Analyzer — Vercel + Render

The project is split into `frontend/` (static HTML/CSS/JS) and `backend/` (Flask REST API).

## Render backend
Create a Render Web Service from this GitHub repository. Set Root Directory to `backend`, Runtime to Python, Build Command to `pip install -r requirements.txt`, and Start Command to `gunicorn app:app`. Deploy, then test `/api/health` on the Render URL.

## Vercel frontend
Import the same repository in Vercel. Set Root Directory to `frontend`, Framework Preset to Other, leave Build Command blank, and set Output Directory to `.`. Deploy.

Edit `frontend/js/config.js` and replace `https://YOUR-RENDER-SERVICE.onrender.com` with the actual Render URL. Commit and push; Vercel redeploys automatically. Set Render environment variable `FRONTEND_ORIGIN` to the exact Vercel URL and redeploy the backend.

## API
`GET /api/health`; `GET /api/evidence`; `POST /api/evidence` (multipart fields: `evidence`, optional `case_ref`, `notes`); `GET /api/evidence/<id>`; `GET /api/evidence/<id>/report`.

## Local backend (Windows)
```bat
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Backend runs at `http://127.0.0.1:5000`.

## Storage and forensic limitations
This educational version uses SQLite and temporary upload files on the Render filesystem. Render free web-service storage is ephemeral; records can be lost after restarts/redeploys. For durable records use persistent storage or managed PostgreSQL and object storage. This is not a certified forensic acquisition tool. Hashes support content comparison but do not prove provenance. Use authorized sample files and keep chain-of-custody records separately.
