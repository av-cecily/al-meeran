import io
import base64
import os
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
from config import Config

# rembg is imported lazily (only when visualizer is used)
# This avoids the onnxruntime backend warning on every server startup
_rembg_remove = None

def _get_rembg():
    """Lazy loader for rembg — only loads when AI visualizer is first used."""
    global _rembg_remove
    if _rembg_remove is None:
        try:
            from rembg import remove
            _rembg_remove = remove
        except Exception as e:
            raise RuntimeError(f"AI Visualizer is unavailable: rembg failed to load. ({e})")
    return _rembg_remove

class UploadService:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def process_visualizer_image(file_stream):
        remove_bg = _get_rembg()  # Load rembg only when this function is called

        input_image = Image.open(file_stream).convert("RGBA")
        cutout = remove_bg(input_image)
        alpha = cutout.split()[-1]

        shading = ImageOps.autocontrast(cutout.convert("L"), cutoff=0.5)
        white_bg = Image.new("L", cutout.size, 255)
        final_shading = Image.composite(shading, white_bg, alpha)

        clean_mask = Image.new("RGBA", cutout.size, (255, 255, 255, 0))
        white_furniture = Image.new("RGBA", cutout.size, (255, 255, 255, 255))
        clean_mask.paste(white_furniture, (0, 0), alpha)

        def to_b64(img):
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return base64.b64encode(buf.getvalue()).decode()

        return {'mask': to_b64(clean_mask), 'shadows': to_b64(final_shading)}

    @staticmethod
    def save_file(file, folder_path):
        if file and UploadService.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder_path, filename))
            return filename
        return None
