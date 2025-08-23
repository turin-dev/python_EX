"""Examples of compressing data and working with archives.

This script demonstrates creating and reading ZIP and tar archives,
and compressing in‑memory data using gzip.
"""

from __future__ import annotations

import os
import tarfile
import zipfile
import gzip


def create_zip_archive(zip_path: str, files: list[str]) -> None:
    """Create a ZIP archive containing the given files."""
    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in files:
            zf.write(file_path, arcname=os.path.basename(file_path))


def list_zip_contents(zip_path: str) -> list[str]:
    """Return the list of file names contained in a ZIP archive."""
    with zipfile.ZipFile(zip_path, mode="r") as zf:
        return zf.namelist()


def create_tar_archive(tar_path: str, files: list[str], compression: str = "gz") -> None:
    """Create a tar archive with optional compression (gz, bz2, xz, or none)."""
    mode = f"w:{compression}" if compression else "w"
    with tarfile.open(tar_path, mode=mode) as tar:
        for file_path in files:
            tar.add(file_path, arcname=os.path.basename(file_path))


def extract_tar_archive(tar_path: str, output_dir: str) -> None:
    """Extract the given tar archive into the specified directory."""
    with tarfile.open(tar_path, mode="r:*") as tar:
        tar.extractall(path=output_dir)


def compress_data(data: bytes) -> bytes:
    """Compress bytes using gzip and return the compressed data."""
    return gzip.compress(data)


def decompress_data(data: bytes) -> bytes:
    """Decompress gzip‑compressed bytes and return the original data."""
    return gzip.decompress(data)


if __name__ == "__main__":
    # Create some sample files for demonstration
    sample_files = ["sample1.txt", "sample2.txt"]
    for idx, fname in enumerate(sample_files, start=1):
        with open(fname, "w", encoding="utf-8") as f:
            f.write(f"This is sample file {idx}\n")

    # Demonstrate ZIP
    create_zip_archive("demo.zip", sample_files)
    print("ZIP contents:", list_zip_contents("demo.zip"))

    # Demonstrate tar
    create_tar_archive("demo.tar.gz", sample_files, "gz")
    extract_dir = "demo_extracted"
    os.makedirs(extract_dir, exist_ok=True)
    extract_tar_archive("demo.tar.gz", extract_dir)
    print("Extracted files:", os.listdir(extract_dir))

    # Demonstrate in‑memory compression
    original = b"Compress me!" * 10
    compressed = compress_data(original)
    decompressed = decompress_data(compressed)
    print(f"Original size: {len(original)}, Compressed: {len(compressed)}, Decompressed equals original: {original == decompressed}")

    # Clean up sample files
    for fname in sample_files:
        os.remove(fname)
    os.remove("demo.zip")
    os.remove("demo.tar.gz")
    for f in os.listdir(extract_dir):
        os.remove(os.path.join(extract_dir, f))
    os.rmdir(extract_dir)