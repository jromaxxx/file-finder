# finder/scanner.py
import os
import hashlib
import pandas as pd
from pathlib import Path

def compute_hash(path, chunk_size=4096):
    """
    Compute the MD5 hash of a file.
    :param path: Path to the file.
    :param chunk_size: Size of chunks to read the file in bytes.
    :return: MD5 hash as a hexadecimal string.
    """
    hasher = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
    except Exception as e:
        print(f"Error computing hash for {path}: {e}")
        return None
    return hasher.hexdigest()

def scan_directory(base_path):
    """
    Scan a directory and return a DataFrame with file details.
    :param base_path: Path to the directory to scan.
    :return: DataFrame with columns: path, size, name, hash.
    """
    files = []
    base_path = Path(base_path)

    for filepath in base_path.rglob("*"):
        if filepath.is_file():
            try:
                files.append({
                    "path": str(filepath),
                    "size": filepath.stat().st_size,
                    "name": filepath.name,  # Ensure the 'name' column is included
                    "hash": compute_hash(filepath)  # Ensure the 'hash' column is included
                })
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    df = pd.DataFrame(files)
    if df.empty:
        print("No files found in the directory.")
    return df

def find_duplicates(df):
    """
    Find duplicate files based on their hash values.
    :param df: DataFrame containing file details.
    :return: DataFrame with duplicate files.
    """
    if "hash" not in df.columns:
        raise KeyError("The DataFrame does not contain a 'hash' column.")
    return df[df.duplicated("hash", keep=False)].sort_values(by="hash")

def find_large_files(df, top_n=20):
    """
    Find the largest files in the directory.
    :param df: DataFrame containing file details.
    :param top_n: Number of largest files to return.
    :return: DataFrame with the largest files.
    """
    if "size" not in df.columns:
        raise KeyError("The DataFrame does not contain a 'size' column.")
    return df.sort_values(by="size", ascending=False).head(top_n)
