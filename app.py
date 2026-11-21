import os
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort
from werkzeug.utils import secure_filename
from database import init_db, add_evidence, get_evidence, get_one_evidence
from forensic.file_analysis import analyze_file
from forensic.image_analysis import analyze_image
from forensic.hashing import calculate_hashes
from forensic.report import create_pdf_report

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")
ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp",
    "pdf", "txt", "csv", "doc", "docx", "xls", "xlsx",
    "zip", "json", "log"
}
MAX_CONTENT_LENGTH = 25 * 1024 * 1024

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-development-secret")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
init_db()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    records = get_evidence()
    return render_template("dashboard.html", records=records, total=len(records))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("evidence")
        case_ref = (request.form.get("case_ref") or "").strip()
        notes = (request.form.get("notes") or "").strip()

        if not file or not file.filename:
            flash("Please choose a file to upload.", "danger")
            return redirect(url_for("upload"))
        if not allowed_file(file.filename):
            flash("This file type is not allowed. Check the supported formats.", "danger")
            return redirect(url_for("upload"))

        original_name = secure_filename(file.filename)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        stored_name = f"{timestamp}_{original_name}"
        path = os.path.join(app.config["UPLOAD_FOLDER"], stored_name)
        file.save(path)

        try:
            file_info = analyze_file(path, original_name)
            hashes = calculate_hashes(path)
            image_info = analyze_image(path) if file_info["is_image"] else None
            evidence_id = add_evidence({
                "case_ref": case_ref,
                "original_name": original_name,
                "stored_name": stored_name,
                "file_path": path,
                "file_type": file_info["mime_type"],
                "file_size": file_info["size_bytes"],
                "sha256": hashes["sha256"],
                "md5": hashes["md5"],
                "created_at": file_info["modified_time"],
                "notes": notes,
                "analysis_json": {
                    "file_info": file_info,
                    "hashes": hashes,
                    "image_info": image_info,
                    "uploaded_at": datetime.now(timezone.utc).isoformat()
                }
            })
            flash("Evidence uploaded and analyzed successfully.", "success")
            return redirect(url_for("analysis", evidence_id=evidence_id))
        except Exception as exc:
            if os.path.exists(path):
                os.remove(path)
            app.logger.exception("Evidence analysis failed")
            flash(f"Could not analyze this file: {exc}", "danger")
            return redirect(url_for("upload"))

    return render_template("upload.html")

@app.route("/analysis/<int:evidence_id>")
def analysis(evidence_id):
    record = get_one_evidence(evidence_id)
    if not record:
        abort(404)
    return render_template("analysis.html", record=record)

@app.route("/report/<int:evidence_id>")
def report(evidence_id):
    record = get_one_evidence(evidence_id)
    if not record:
        abort(404)
    report_path = create_pdf_report(record, REPORT_FOLDER)
    return send_file(report_path, as_attachment=True, download_name=f"forensic-report-{evidence_id}.pdf")

@app.errorhandler(413)
def too_large(_error):
    flash("File is too large. Maximum upload size is 25 MB.", "danger")
    return redirect(url_for("upload"))

if __name__ == "__main__":
    app.run(debug=True)
