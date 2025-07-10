import os
import re
import json
import base64
import argparse
from urllib.parse import unquote


def extract_hosts_sni(text: str):
    pattern = re.compile(r"(?:[?&](host|sni)=)([^&#\s]+)")
    matches = pattern.findall(text)
    return [unquote(val) for _, val in matches]


def extract_vmess_hosts(text: str):
    """Extract host or sni values from vmess links."""
    results = []
    for b64 in re.findall(r"vmess://([A-Za-z0-9+/=]+)", text):
        # fix padding if necessary
        padding = '=' * (-len(b64) % 4)
        try:
            decoded = base64.b64decode(b64 + padding)
            data = json.loads(decoded.decode('utf-8', errors='ignore'))
        except Exception:
            continue
        for key in ('host', 'sni', 'add'):
            val = data.get(key)
            if val:
                results.append(val)
    return results


def scan_directory(directory: str):
    results = []
    for root, _, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    results.extend(extract_hosts_sni(content))
                    results.extend(extract_vmess_hosts(content))
            except Exception:
                # ignore non-text or unreadable files
                continue
    return results


def main():
    parser = argparse.ArgumentParser(description="Scan directory for host or sni values")
    parser.add_argument('path', help='Path to scan')
    parser.add_argument('-o', '--output', default='results.txt', help='Output file')
    args = parser.parse_args()

    extracted = scan_directory(args.path)

    # write output using UTF-8 to avoid UnicodeEncodeError on Windows
    with open(args.output, 'w', encoding='utf-8') as out_file:
        for item in extracted:
            out_file.write(item + '\n')
    for item in extracted:
        print(item)


if __name__ == '__main__':
    main()
