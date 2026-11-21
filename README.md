# Digital Forensics Analyzer

A beginner-friendly Flask application for educational digital evidence triage. Upload a file, inspect basic metadata, calculate MD5 and SHA-256 hashes, view image dimensions/EXIF metadata, and download a PDF summary.

## Features
- Evidence upload with extension allowlist and 25 MB limit
- SQLite evidence register
- File size, extension, MIME guess and modified timestamp
- MD5 and SHA-256 hashes
- Image properties and readable EXIF metadata (when present)
- Downloadable PDF analysis report

## Technology
Python, Flask, SQLite, Pillow, ReportLab, HTML, Bootstrap 5 and JavaScript.

## Requirements
- Python 3.10 or newer
- pip

## Run on Windows
Open Command Prompt or the VS Code terminal in this project folder:

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Run on macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Project structure
```text
app.py                 Flask routes and application startup
database.py            SQLite database operations
forensic/hashing.py    MD5 and SHA-256 calculation
forensic/file_analysis.py Basic file metadata
forensic/image_analysis.py Image properties and EXIF extraction
forensic/report.py     PDF report generation
templates/             HTML pages
static/                CSS and JavaScript
uploads/                Uploaded evidence copies (not committed)
reports/                Generated PDF reports (not committed)
```

## Important limitations and safe use
This is an educational prototype, not a certified forensic acquisition suite. MIME type is inferred from the filename, timestamps can be modified, and metadata can be absent or manipulated. A hash demonstrates content equality between copies when recalculated; it does not prove provenance or authenticity. The app does not implement a formal chain-of-custody process, disk imaging, malware scanning, or automated proof of tampering.

Use only files you own or are authorized to examine. For real investigations, use validated forensic procedures, preserve originals read-only, record custody transfers, and have findings reviewed by a qualified examiner. Do not upload confidential or sensitive evidence to an exposed/public server.

## GitHub publishing
1. Create a new **public** GitHub repository named `Digital-Forensics-Analyzer`.
2. Do not upload `venv/`, `forensics.db`, or real evidence files from `uploads/`.
3. From the project folder run:

```bash
git init
git add .
git commit -m "Initial Digital Forensics Analyzer project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Digital-Forensics-Analyzer.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.
