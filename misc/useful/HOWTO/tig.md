# tig — Text-mode Git Browser

An ncurses Git log and diff browser. Great for exploring history, reviewing
commits, and navigating blame without leaving the terminal.

## Launch

```bash
tig                     # log view for current branch
tig --all               # all branches
tig path/to/file        # log for a specific file
tig blame path/to/file  # blame view
tig show HEAD~3         # show a specific commit
tig status              # status view (like git status + diff)
tig stash               # browse stashes
```

## Views and navigation

| Key | Action |
|-----|--------|
| `Enter` | Open diff for selected commit |
| `Tab` | Switch between log and diff panels |
| `j` / `k` | Move down / up |
| `q` | Close current view |
| `Q` | Quit tig |
| `h` | Help |
| `/` | Search |
| `n` / `N` | Next / previous search result |

## View shortcuts

| Key | View |
|-----|------|
| `m` | Main log view |
| `d` | Diff view |
| `l` | Log view |
| `b` | Blame view |
| `t` | Tree view (file browser) |
| `s` | Status view |
| `S` | Stage view |
| `y` | Stash view |

## Staging (status view)

```bash
tig status    # shows staged and unstaged changes
```

In the status view:
- `u` — stage / unstage file
- `Enter` — view diff for file
- `C` — commit staged changes

## Use-cases

- Exploring a repo's history visually without a GUI tool
- Quickly blaming a file: `tig blame src/main.py`
- Reviewing a file's change history: `tig src/api.py`
- Browsing stashes: `tig stash`
- Staging hunks interactively in the status view
