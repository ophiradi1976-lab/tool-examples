# bat — Better cat

`cat` replacement with syntax highlighting, line numbers, Git integration, and paging.
Aliased to `cat` in this setup.

## Basic usage

```bash
bat file.py          # Syntax-highlighted output
bat file1 file2      # Multiple files with headers
bat -n file.py       # Show line numbers only (no other decorations)
bat -A file.txt      # Show non-printable characters
```

## Useful flags

```bash
bat --plain file.py          # No decorations (just highlighting) — good for piping
bat --language=python file   # Force a language
bat --list-languages         # See all supported languages
bat --list-themes            # See available color themes
bat --theme=TwoDark file.py  # Use a specific theme
bat -r 10:20 file.py         # Show only lines 10–20
```

## Piping and composition

```bash
# bat still works fine in pipes — use --plain or -p to strip decorations
cat large.json | python -m json.tool | bat -l json

# Use as a man pager
export MANPAGER="sh -c 'col -bx | bat -l man -p'"

# Tail a log with highlighting
tail -f app.log | bat --paging=never -l log
```

## Git integration

bat shows `+`, `-`, `~` in the gutter for added/removed/modified lines compared to the
last Git commit — no extra flags needed, it's automatic in a Git repo.

## Use-cases

- Reading source files: `bat src/main.py`
- Quick JSON inspection: `bat response.json`
- Reviewing config files: `bat ~/.zshrc`
- Piping into fzf previews: `fzf --preview 'bat --color=always {}'`

## Tip

Since `cat` is aliased to `bat`, use `/bin/cat` or `command cat` when you explicitly
need raw output (e.g., when feeding binary data through a pipe).
