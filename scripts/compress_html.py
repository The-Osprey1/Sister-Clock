#!/usr/bin/env python3
"""
compress_html.py - Synchronizes readable index_html with compressed index_html_gz in index_html.h
Uses deterministic gzip (level 9, mtime=0) so the output is identical across runs.

The gzip header's operating-system byte is pinned to 0xff ("unknown") and line endings are
normalized to LF, so Windows and Linux produce the same bytes.

Usage:
  python scripts/compress_html.py           # rebuild index_html_gz from the readable HTML
  python scripts/compress_html.py --check   # exit 1 if index_html_gz does not match the readable HTML
"""

import os
import gzip
import re
import sys

HTML_PATTERN = r'(const char index_html\[\] PROGMEM = R"rawliteral\()([\s\S]*?)(\)rawliteral";)'
GZ_PATTERN = r'const uint8_t index_html_gz\[\] PROGMEM = \{[\s\S]*?const size_t index_html_gz_len = sizeof\(index_html_gz\);'
GZ_BYTES_PATTERN = r'const uint8_t index_html_gz\[\] PROGMEM = \{([\s\S]*?)\};'
GZIP_OS_BYTE_OFFSET = 9
GZIP_OS_UNKNOWN = 0xFF


def read_header(header_path):
    with open(header_path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def readable_html(content):
    match = re.search(HTML_PATTERN, content)
    if not match:
        raise ValueError("Could not find uncompressed index_html rawliteral in header!")
    return match.group(2).replace("\r\n", "\n")


def embedded_gz(content):
    match = re.search(GZ_BYTES_PATTERN, content)
    if not match:
        raise ValueError("Could not find existing index_html_gz array in header!")
    return bytes(int(x, 16) for x in re.findall(r"0x([0-9a-fA-F]{2})", match.group(1)))


def deterministic_gzip(html_text):
    gz_bytes = bytearray(gzip.compress(html_text.encode("utf-8"), compresslevel=9, mtime=0))
    gz_bytes[GZIP_OS_BYTE_OFFSET] = GZIP_OS_UNKNOWN
    return bytes(gz_bytes)


def check_index_html(header_path):
    content = read_header(header_path)
    served = gzip.decompress(embedded_gz(content)).decode("utf-8")
    if served != readable_html(content):
        print("index_html_gz is out of sync with index_html. Run: python scripts/compress_html.py")
        return False
    print("index_html_gz matches index_html.")
    return True


def compress_index_html(header_path):
    content = read_header(header_path)
    html_text = readable_html(content)
    html_bytes = html_text.encode("utf-8")

    gz_bytes = deterministic_gzip(html_text)

    # Format bytes as C array with 16 bytes per line
    hex_lines = []
    for i in range(0, len(gz_bytes), 16):
        chunk = gz_bytes[i:i+16]
        hex_lines.append("  " + ", ".join(f"0x{b:02x}" for b in chunk))
    c_array_body = ",\n".join(hex_lines)

    new_gz_section = f"const uint8_t index_html_gz[] PROGMEM = {{\n{c_array_body}\n}};\nconst size_t index_html_gz_len = sizeof(index_html_gz);"

    if not re.search(GZ_PATTERN, content):
        raise ValueError("Could not find existing index_html_gz array in header!")

    updated_content = re.sub(GZ_PATTERN, lambda _: new_gz_section, content)

    with open(header_path, "w", encoding="utf-8", newline="") as f:
        f.write(updated_content)

    print(f"Compressed index_html: {len(html_bytes):,} bytes -> {len(gz_bytes):,} bytes ({100 * (1 - len(gz_bytes)/len(html_bytes)):.1f}% reduction)")
    return len(html_bytes), len(gz_bytes)

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    header_path = os.path.join(base_dir, "firmware", "index_html.h")
    if "--check" in sys.argv[1:]:
        sys.exit(0 if check_index_html(header_path) else 1)
    compress_index_html(header_path)
