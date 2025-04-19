# finder/scanner.py
import os
import hashlib
import pandas as pd
from pathlib import Path

def compute_hash(path, chunk_size=4096):
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def scan_directory(base_path):
    files = []
    base_path = Path(base_path)

    for filepath in base_path.rglob("*"):
        if filepath.is_file():
            try:
                files.append({
                    "path": str(filepath),
                    "size": filepath.stat().st_size,
                    "name": filepath.name,
                    "hash": compute_hash(filepath)
                })
            except Exception as e:
                print(f"Error con {filepath}: {e}")

    df = pd.DataFrame(files)
    return df

def find_duplicates(df):
    return df[df.duplicated("hash", keep=False)].sort_values(by="hash")

def find_large_files(df, top_n=20):
    return df.sort_values(by="size", ascending=False).head(top_n)
