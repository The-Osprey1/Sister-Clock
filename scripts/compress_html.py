#!/usr/bin/env python3
"""
compress_html.py - Synchronizes readable index_html with compressed index_html_gz in index_html.h
Uses deterministic gzip (level 9, mtime=0) so the output is identical across runs.
"""

import os
import gzip
import re

def compress_index_html(header_path):
    with open(header_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match uncompressed HTML inside rawliteral
    pattern = r'(const char index_html\[\] PROGMEM = R"rawliteral\()([\s\S]*?)(\)rawliteral";)'
    match = re.search(pattern, content)
    if not match:
        raise ValueError("Could not find uncompressed index_html rawliteral in header!")

    html_text = match.group(2)
    html_bytes = html_text.encode("utf-8")
    
    # Deterministic gzip compression (mtime=0)
    gz_bytes = gzip.compress(html_bytes, compresslevel=9, mtime=0)
    
    # Format bytes as C array with 16 bytes per line
    hex_lines = []
    for i in range(0, len(gz_bytes), 16):
        chunk = gz_bytes[i:i+16]
        hex_lines.append("  " + ", ".join(f"0x{b:02x}" for b in chunk))
    c_array_body = ",\n".join(hex_lines)

    new_gz_section = f"const uint8_t index_html_gz[] PROGMEM = {{\n{c_array_body}\n}};\nconst size_t index_html_gz_len = sizeof(index_html_gz);"

    # Replace existing index_html_gz array
    gz_pattern = r'const uint8_t index_html_gz\[\] PROGMEM = \{[\s\S]*?const size_t index_html_gz_len = sizeof\(index_html_gz\);'
    if not re.search(gz_pattern, content):
        raise ValueError("Could not find existing index_html_gz array in header!")

    updated_content = re.sub(gz_pattern, new_gz_section, content)

    with open(header_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"Compressed index_html: {len(html_bytes):,} bytes -> {len(gz_bytes):,} bytes ({100 * (1 - len(gz_bytes)/len(html_bytes)):.1f}% reduction)")
    return len(html_bytes), len(gz_bytes)

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    header_path = os.path.join(base_dir, "firmware", "index_html.h")
    compress_index_html(header_path)
