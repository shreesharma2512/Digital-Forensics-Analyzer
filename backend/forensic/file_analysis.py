import mimetypes
import os
from datetime import datetime, timezone

def analyze_file(file_path, original_name):
    stat = os.stat(file_path)
    mime_type, _encoding = mimetypes.guess_type(original_name)
    extension = os.path.splitext(original_name)[1].lower()
    return {
        "filename": original_name,
        "extension": extension or "No extension",
        "mime_type": mime_type or "Unknown / not identified",
        "size_bytes": stat.st_size,
        "size_readable": format_size(stat.st_size),
        "modified_time": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "is_image": extension in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"},
    }

def format_size(size):
    value = float(size)
    for unit in ["B", "KB", "MB", "GB"]:
        if value < 1024 or unit == "GB":
            return f"{value:.2f} {unit}"
        value /= 1024
