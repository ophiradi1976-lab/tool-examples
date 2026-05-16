# pv — Pipe Viewer

Shows progress, throughput, and ETA for data moving through a Unix pipe.
Drop it into any pipeline between two commands.

## Basic usage

```bash
pv file.txt | gzip > file.txt.gz          # compress with progress
pv large.sql | mysql -u root mydb         # DB import with progress
cat file.iso | pv | dd of=/dev/sdb        # write ISO to disk with progress
```

## Output shows

```
500MB 0:00:42 [12.3MB/s] [===========>   ] 62% ETA 0:00:25
```

- Data transferred
- Elapsed time
- Throughput
- Progress bar (if total size is known)
- ETA

## Flags

| Flag | Meaning |
|------|---------|
| `-s SIZE`   | Expected size (enables %, ETA) — e.g. `-s 1G` or `-s $(wc -c < file)` |
| `-l`        | Count lines instead of bytes |
| `-n`        | Show only percentage (no bar, for use in scripts) |
| `-q`        | Quiet — suppress output (useful when just rate-limiting) |
| `-L RATE`   | Limit throughput — e.g. `-L 1m` for 1 MB/s |
| `-b`        | Show only bytes transferred |
| `-t`        | Show only elapsed time |

## Common patterns

```bash
# Compress a large file with progress
pv bigfile.tar | gzip > bigfile.tar.gz

# Copy with known size for accurate ETA
pv -s $(du -sb file.iso | cut -f1) file.iso | dd of=/dev/sdb bs=4M

# Database dump + import pipeline with progress
mysqldump mydb | pv | gzip > backup.sql.gz
pv backup.sql.gz | gunzip | mysql -u root mydb

# Rate-limit a transfer to 500 KB/s
pv -L 500k input.dat > /dev/null

# Count lines processed from a large log
pv --line-mode access.log | awk '{print $1}' | sort | uniq -c

# Progress on a long grep
pv large.log | grep "ERROR" > errors.txt
```

## Use-cases

- Long-running data imports/exports where you need an ETA
- Throttling I/O so you don't saturate network or disk
- Monitoring throughput in a pipeline for performance tuning
