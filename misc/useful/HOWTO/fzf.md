# fzf — Fuzzy Finder

Interactive fuzzy search over any list of lines.

## Basic usage

```bash
# Browse files in current directory
fzf

# Open selected file in vim
vim $(fzf)

# Pipe anything into it
ls | fzf
cat /etc/hosts | fzf
```

## Shell keybindings (installed by playbook)

| Shortcut | Action |
|----------|--------|
| `Ctrl+R` | Fuzzy search shell history |
| `Ctrl+T` | Fuzzy-paste a file path into current command |
| `Alt+C`  | Fuzzy cd into a subdirectory |

## File preview

```bash
# Preview with cat
fzf --preview 'cat {}'

# Preview with bat (syntax highlighted)
fzf --preview 'bat --color=always {}'

# Preview with line numbers and scroll
fzf --preview 'bat --color=always --line-range :100 {}'
```

## Common use-cases

```bash
# Interactively kill a process
kill $(ps aux | fzf | awk '{print $2}')

# Checkout a git branch
git checkout $(git branch | fzf)

# SSH into a known host
ssh $(cat ~/.ssh/config | grep "^Host " | awk '{print $2}' | fzf)

# Open a recently modified file
vim $(find . -type f -newer ~/.zshrc | fzf)

# cd into any subdirectory
cd $(find . -type d | fzf)

# Search ripgrep results interactively
rg --line-number '' | fzf --delimiter ':' \
  --preview 'bat --color=always {1} --highlight-line {2}'
```

## Useful flags

```bash
fzf --multi            # Tab to select multiple items
fzf --reverse          # Prompt at top
fzf --height 40%       # Don't take full screen
fzf --query "foo"      # Pre-fill search query
fzf --exact            # Exact match instead of fuzzy
fzf --no-sort          # Keep input order (good for history)
```
