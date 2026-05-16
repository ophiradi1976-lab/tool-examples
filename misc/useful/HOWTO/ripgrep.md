# ripgrep (rg) — Fast Recursive Grep

A grep replacement written in Rust. Faster than grep/ag, respects `.gitignore`
by default, and has sane defaults for code search. Required by Telescope in Neovim.

## Basic usage

```bash
rg "pattern"                    # search current directory recursively
rg "pattern" src/               # search a specific directory
rg "pattern" file.py            # search a specific file
rg "def authenticate"           # find function definitions
```

## Common flags

| Flag | Meaning |
|------|---------|
| `-i`         | Case-insensitive |
| `-n`         | Show line numbers (on by default) |
| `-l`         | Show only filenames with matches |
| `-c`         | Count matches per file |
| `-w`         | Whole word match |
| `-v`         | Invert match (exclude pattern) |
| `-A N`       | N lines after match |
| `-B N`       | N lines before match |
| `-C N`       | N lines context (before + after) |
| `--no-ignore`| Don't respect .gitignore |
| `-u`         | One `-u` = include hidden; `-uu` = include binaries |
| `-g "glob"`  | Include/exclude by glob pattern |
| `-t type`    | Filter by file type |
| `--stats`    | Show match statistics |

## File type filtering

```bash
rg "import" -t py               # Python files only
rg "console.log" -t js          # JavaScript only
rg "SELECT" -t sql              # SQL files only
rg --type-list                  # see all supported types
rg "TODO" -g "*.ts"             # glob pattern
rg "TODO" -g "!vendor/"         # exclude a directory
```

## Patterns

```bash
# Find all TODOs with context
rg "TODO|FIXME|HACK" -C 2

# Search for a function definition across Python files
rg "^def " -t py

# Find files containing a pattern (no line output)
rg -l "deprecated"

# Count occurrences per file
rg -c "console.log" -t js

# Search hidden files (e.g. dotfiles)
rg -u "API_KEY"

# Case-insensitive whole-word search
rg -iw "error"

# Search in a specific set of files
rg "pattern" src/ -g "*.{py,yml}"
```

## With fzf (interactive search)

```bash
rg --line-number '' | fzf --delimiter ':' \
  --preview 'bat --color=always {1} --highlight-line {2}'
```

## In Neovim (Telescope)

```vim
:Telescope live_grep         " uses rg under the hood
:Telescope grep_string       " search for word under cursor
```

## Use-cases

- Finding all usages of a function across a codebase
- Locating TODO/FIXME comments: `rg "TODO|FIXME"`
- Auditing for hardcoded secrets: `rg -i "password|api_key|secret"`
- Searching across file types in a monorepo
- Fast log file searching: `rg "ERROR" --no-ignore app.log`
