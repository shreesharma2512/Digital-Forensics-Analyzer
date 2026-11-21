import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "forensics.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_ref TEXT,
                original_name TEXT NOT NULL,
                stored_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT,
                file_size INTEGER,
                sha256 TEXT,
                md5 TEXT,
                created_at TEXT,
                notes TEXT,
                analysis_json TEXT,
                added_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def add_evidence(item):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO evidence
            (case_ref, original_name, stored_name, file_path, file_type, file_size,
             sha256, md5, created_at, notes, analysis_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["case_ref"], item["original_name"], item["stored_name"],
            item["file_path"], item["file_type"], item["file_size"],
            item["sha256"], item["md5"], item["created_at"], item["notes"],
            json.dumps(item["analysis_json"])
        ))
        return cursor.lastrowid

def _serialize(row):
    if not row:
        return None
    item = dict(row)
    try:
        item["analysis"] = json.loads(item.pop("analysis_json") or "{}")
    except json.JSONDecodeError:
        item["analysis"] = {}
    return item

def get_evidence():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM evidence ORDER BY id DESC").fetchall()
        return [_serialize(row) for row in rows]

def get_one_evidence(evidence_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM evidence WHERE id = ?", (evidence_id,)).fetchone()
        return _serialize(row)
