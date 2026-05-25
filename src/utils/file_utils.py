# src/utils/file_utils.py
import hashlib
from pathlib import Path

def ensure_dir(dir_path: Path):
    dir_path.mkdir(parents=True, exist_ok=True)

def get_file_hash(file_path: Path, algo="md5") -> str:
    h = hashlib.new(algo)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()