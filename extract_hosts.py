import os
import re
import sys

pattern = re.compile(r"(?:host|sni)=([^\s&#]+)")

def search_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return []
    return pattern.findall(content)

def scan_directory(root_dir):
    results = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            matches = search_file(filepath)
            results.extend(matches)
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_hosts.py <directory>")
        sys.exit(1)
    directory = sys.argv[1]
    hosts = scan_directory(directory)
    for host in hosts:
        print(host)
