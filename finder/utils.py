# finder/utils.py
import humanize

def human_readable_size(size_bytes):
    """Convierte bytes en formato legible como '2.5 MB'"""
    return humanize.naturalsize(size_bytes, binary=True)

def is_valid_path(path):
    """Verifica si un path es seguro para escanear"""
    try:
        return path.is_file()
    except Exception:
        return False
