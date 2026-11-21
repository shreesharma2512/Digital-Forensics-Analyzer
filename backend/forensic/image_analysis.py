import os
from PIL import Image, ExifTags

def analyze_image(file_path):
    result = {"available": False, "error": None}
    try:
        with Image.open(file_path) as image:
            result.update({
                "available": True,
                "format": image.format or "Unknown",
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "exif": {}
            })
            try:
                raw_exif = image.getexif()
                for key, value in raw_exif.items():
                    name = ExifTags.TAGS.get(key, str(key))
                    result["exif"][name] = str(value)[:300]
            except Exception:
                result["exif"] = {}
    except Exception as exc:
        result["error"] = str(exc)
    return result
