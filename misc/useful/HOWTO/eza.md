# eza — Modern ls Replacement

A modern, colorful `ls` with Git status, icons, and tree view.
Aliased in this setup: `ls`, `ll`, `lt`.

## Aliases set up by playbook

```bash
ls   → eza                    # basic listing, colorized
ll   → eza -lah --git         # long format, hidden files, human sizes, Git status
lt   → eza --tree             # tree view
```

## Basic usage

```bash
eza                        # list current directory
eza /etc                   # list a specific path
eza -l                     # long format
eza -a                     # include hidden files (dotfiles)
eza -lah                   # long + all + human-readable sizes
eza --git                  # show Git status column
```

## Tree view

```bash
eza --tree                 # tree from current dir
eza --tree --level=2       # limit depth
eza --tree -l              # tree with long format
eza --tree --git           # tree + git status
```

## Sorting and filtering

```bash
eza --sort=size            # sort by file size
eza --sort=modified        # sort by modification time
eza --sort=ext             # sort by extension
eza -r                     # reverse sort
eza --only-dirs            # show directories only
```

## Git status column

When using `--git`, eza shows a two-character Git status per file:

| Symbol | Meaning |
|--------|---------|
| `N`    | New (untracked) |
| `M`    | Modified |
| `D`    | Deleted |
| `-`    | Unmodified |
| `I`    | Ignored |

## Use-cases

```bash
# Quick overview of a project
ll

# See what changed in a repo at a glance
ll --git

# Explore directory structure
lt --level=3

# Find the largest files
eza -lah --sort=size --reverse
```
