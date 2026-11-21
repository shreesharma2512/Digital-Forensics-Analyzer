import os,tempfile
from datetime import datetime,timezone
from flask import Flask,jsonify,request,send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from database import init_db,add,all_items,one
from forensic.file_analysis import analyze_file
from forensic.hashing import calculate_hashes
from forensic.image_analysis import analyze_image
from forensic.report import create_pdf_report
BASE=os.path.dirname(os.path.abspath(__file__)); DATA=os.environ.get('DATA_DIR',os.path.join(BASE,'data')); UP=os.path.join(DATA,'uploads'); RP=os.path.join(DATA,'reports'); DB=os.environ.get('DB_PATH',os.path.join(DATA,'forensics.db'))
os.makedirs(UP,exist_ok=True);os.makedirs(RP,exist_ok=True)
MAX=25*1024*1024; ALLOWED={'.png','.jpg','.jpeg','.gif','.bmp','.tiff','.webp','.pdf','.txt','.csv','.doc','.docx','.xls','.xlsx','.zip','.json','.log'}
app=Flask(__name__);app.config['MAX_CONTENT_LENGTH']=MAX
CORS(app,resources={r'/api/*':{'origins':[x.strip() for x in os.environ.get('FRONTEND_ORIGIN','*').split(',') if x.strip()]}});init_db(DB)
@app.get('/')
def home():return jsonify(service='Digital Forensics Analyzer API',status='running',health='/api/health')
@app.get('/api/health')
def health():return jsonify(status='ok')
@app.get('/api/evidence')
def listing():return jsonify(items=all_items(DB))
@app.post('/api/evidence')
def upload():
 f=request.files.get('evidence')
 if not f or not f.filename:return jsonify(error='Choose a file.'),400
 name=secure_filename(f.filename);ext=os.path.splitext(name)[1].lower()
 if ext not in ALLOWED:return jsonify(error='File type is not allowed.'),400
 path=None
 try:
  with tempfile.NamedTemporaryFile(delete=False,suffix=ext,dir=UP) as t:path=t.name;f.save(t)
  size=os.path.getsize(path)
  if size>MAX:return jsonify(error='Maximum upload size is 25 MB.'),413
  info=analyze_file(path,name); hashes=calculate_hashes(path); img=analyze_image(path) if info['is_image'] else None
  analysis={'file_info':info,'hashes':hashes,'image_info':img,'analyzed_at':datetime.now(timezone.utc).isoformat()}
  item={'case_ref':(request.form.get('case_ref') or '').strip(),'original_name':name,'stored_name':os.path.basename(path),'file_path':'','file_type':info['mime_type'],'file_size':size,'sha256':hashes['sha256'],'md5':hashes['md5'],'created_at':info['modified_time'],'notes':(request.form.get('notes') or '').strip(),'analysis':analysis}
  i=add(DB,item);return jsonify(message='Evidence analyzed.',item=one(DB,i)),201
 finally:
  if path and os.path.exists(path):os.remove(path)
@app.get('/api/evidence/<int:i>')
def detail(i):
 x=one(DB,i)
 if not x:return jsonify(error='Evidence record not found.'),404
 return jsonify(item=x)
@app.get('/api/evidence/<int:i>/report')
def report(i):
 x=one(DB,i)
 if not x:return jsonify(error='Evidence record not found.'),404
 p=create_pdf_report(x,RP);return send_file(p,as_attachment=True,download_name=f'forensic-report-{i}.pdf')
@app.errorhandler(413)
def large(_):return jsonify(error='File too large. Maximum size is 25 MB.'),413
if __name__=='__main__':app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
