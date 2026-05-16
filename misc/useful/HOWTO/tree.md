# tree — Directory Tree Viewer

Displays directory structure as a visual tree. Good for quick project overviews
and documentation. (`eza --tree` is an alternative with Git integration.)

## Basic usage

```bash
tree                    # tree from current dir
tree /path/to/dir       # specific directory
tree -L 2               # limit depth to 2 levels
tree -a                 # include hidden files
tree -d                 # directories only
```

## Filtering

```bash
tree -I "node_modules"                  # ignore a pattern
tree -I "node_modules|__pycache__|.git" # ignore multiple patterns
tree -P "*.py"                          # show only matching files
```

## Output formatting

```bash
tree -f                 # print full path for each file
tree -s                 # show file sizes
tree -h                 # human-readable sizes
tree --du               # show directory sizes (disk usage)
tree -t                 # sort by modification time
tree -r                 # reverse sort
tree -C                 # force color output (e.g. when piping)
```

## Output to file / markdown

```bash
# Save as plain text
tree -L 2 > structure.txt

# Output without colors for piping/docs
tree --noreport -L 3
```

## Use-cases

```bash
# Document a project structure in a README
tree -L 2 -I "node_modules|.git|__pycache__"

# See what a tarball will contain before extracting
tar tf archive.tar | tree --fromfile

# Find deeply nested directories
tree -d -L 5

# Quick audit of a config directory
tree /etc/nginx
```
