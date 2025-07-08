# h-s_finder

This repository contains a small Python utility to scan a directory for
configuration strings containing `host` or `sni` parameters and outputs
the extracted values.

## Usage

```bash
python extract_hosts.py <directory>
```

The script will recursively search all files under the provided directory
and print each host or SNI value it finds.

