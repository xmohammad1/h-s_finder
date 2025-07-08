# h-s_finder

This repository contains a small utility script for scanning a directory and
extracting any `host` or `sni` parameters found inside the files. The script
prints each value it finds and also stores them in a text file using UTF-8
encoding so that special characters are preserved across platforms.

### Usage

```bash
python3 scan_hosts.py PATH_TO_SCAN -o results.txt
```

Replace `PATH_TO_SCAN` with the directory you want to search. The optional `-o`
argument specifies the output file (defaults to `results.txt`).
