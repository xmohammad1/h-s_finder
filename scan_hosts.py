import os
import re
import argparse
from urllib.parse import unquote


def extract_hosts_sni(text: str):
    pattern = re.compile(r"(?:[?&](host|sni)=)([^&#\s]+)")
    matches = pattern.findall(text)
    return [unquote(val) for _, val in matches]


def scan_directory(directory: str):
    results = []
    for root, _, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    results.extend(extract_hosts_sni(content))
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
