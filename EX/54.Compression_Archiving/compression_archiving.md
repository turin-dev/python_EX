# Chapter 54 – Data Compression and Archiving

Python includes modules for compressing data and working with archive files.  The standard library supports algorithms such as zlib, gzip, bzip2 and lzma, and provides APIs for creating ZIP and tar archives【19158217920106†L44-L48】.  The `zipfile` module offers tools to read, write and append ZIP archives, while `tarfile` handles tar archives with optional compression【856138858232659†L67-L75】【919694996865956†L70-L90】.

## Creating and reading ZIP files

ZIP is a common archive format that supports compression and storing multiple files.  The `zipfile` module exposes `ZipFile` objects, which you can open in modes `'r'` (read), `'w'` (write), `'a'` (append), or `'x'` (exclusive creation).  It supports deflated (compressed) and stored (uncompressed) entries.  The documentation notes that the module can handle large ZIP64 archives but cannot create encrypted ZIP files【856138858232659†L67-L75】.  Supported compression methods include `ZIP_STORED` (no compression), `ZIP_DEFLATED` (zlib), `ZIP_BZIP2` and `ZIP_LZMA`【856138858232659†L134-L150】.

Example: creating a ZIP archive and listing its contents:

```python
import zipfile

# Create a ZIP archive with compression
with zipfile.ZipFile("example.zip", mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.write("input.txt")
    zf.writestr("hello.txt", "Hello, ZIP!")

# Read the archive
with zipfile.ZipFile("example.zip") as zf:
    print("Contained files:", zf.namelist())
    with zf.open("hello.txt") as f:
        print(f.read().decode())
```

## Tar archives and compression

The `tarfile` module reads and writes tar archives, optionally compressed with gzip, bzip2 or lzma.  It supports POSIX formats and can store various file types including directories, symbolic links and device files【919694996865956†L70-L90】.  Opening a `TarFile` with mode `'w:gz'`, `'w:bz2'`, or `'w:xz'` chooses the compression algorithm.  Use `tarfile.open()` to create or extract archives.

```python
import tarfile

# Create a gzip‑compressed tar archive
with tarfile.open("example.tar.gz", mode="w:gz") as tar:
    tar.add("input.txt")

# Extract the archive
with tarfile.open("example.tar.gz", mode="r:gz") as tar:
    tar.extractall(path="extracted")
```

## Other compression modules

Low‑level modules like `zlib`, `gzip`, `bz2` and `lzma` provide access to compression algorithms for in‑memory data.  Use them to compress and decompress byte strings without creating archives.

## Summary

For packaging multiple files, use `zipfile` or `tarfile`.  ZIP files are widely supported and provide random access to entries, whereas tar archives preserve file metadata and may compress better when combined with `gzip` or `lzma`.  For simple compression of in‑memory data, use `zlib`, `gzip`, `bz2` or `lzma`.  Python’s standard library makes it easy to compress data and build archives【19158217920106†L44-L48】【856138858232659†L134-L150】【919694996865956†L70-L90】.