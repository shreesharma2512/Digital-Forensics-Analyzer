import json, os, sqlite3

def connect(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    c=sqlite3.connect(path); c.row_factory=sqlite3.Row; return c

def init_db(path):
    with connect(path) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS evidence (id INTEGER PRIMARY KEY AUTOINCREMENT, case_ref TEXT, original_name TEXT NOT NULL, stored_name TEXT, file_path TEXT, file_type TEXT, file_size INTEGER, sha256 TEXT, md5 TEXT, created_at TEXT, notes TEXT, analysis_json TEXT, added_at TEXT DEFAULT CURRENT_TIMESTAMP)''')

def add(path, x):
    with connect(path) as c:
        q=c.execute('''INSERT INTO evidence(case_ref,original_name,stored_name,file_path,file_type,file_size,sha256,md5,created_at,notes,analysis_json) VALUES(?,?,?,?,?,?,?,?,?,?,?)''', (x.get('case_ref'),x['original_name'],x.get('stored_name'),x.get('file_path'),x.get('file_type'),x.get('file_size'),x.get('sha256'),x.get('md5'),x.get('created_at'),x.get('notes'),json.dumps(x.get('analysis',{}))))
        return q.lastrowid

def serial(r):
    if not r:return None
    d=dict(r)
    try:d['analysis']=json.loads(d.pop('analysis_json') or '{}')
    except Exception:d['analysis']={}
    return d

def all_items(path):
    with connect(path) as c:return [serial(r) for r in c.execute('SELECT * FROM evidence ORDER BY id DESC').fetchall()]

def one(path,i):
    with connect(path) as c:return serial(c.execute('SELECT * FROM evidence WHERE id=?',(i,)).fetchone())
