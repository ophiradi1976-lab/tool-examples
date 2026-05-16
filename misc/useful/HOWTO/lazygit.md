# lazygit — Terminal UI for Git

A fast, keyboard-driven Git interface that replaces most `git` CLI commands with
a visual panel layout.

## Launch

```bash
lazygit        # open in current repo
```

## Panel layout

```
┌─────────────┬──────────────────────────────┐
│  1 Status   │                              │
├─────────────┤       Main panel             │
│  2 Files    │   (diff / log / content)     │
├─────────────┤                              │
│  3 Branches │                              │
├─────────────┼──────────────────────────────┤
│  4 Commits  │                              │
├─────────────┤                              │
│  5 Stash    │                              │
└─────────────┴──────────────────────────────┘
```

Switch panels with number keys `1–5` or `Tab` / `Shift+Tab`.

## Essential keybindings

### Files panel (staging)
| Key | Action |
|-----|--------|
| `Space` | Stage / unstage file |
| `a` | Stage all |
| `c` | Commit |
| `A` | Amend last commit |
| `d` | Discard changes |
| `e` | Open file in editor |

### Branches panel
| Key | Action |
|-----|--------|
| `Space` | Checkout branch |
| `n` | New branch |
| `d` | Delete branch |
| `M` | Merge into current branch |
| `r` | Rebase current onto selected |

### Commits panel
| Key | Action |
|-----|--------|
| `r` | Reword commit message |
| `s` | Squash into previous commit |
| `d` | Drop commit |
| `Space` | Cherry-pick |
| `p` | Pick (during rebase) |

### Global
| Key | Action |
|-----|--------|
| `P` | Push |
| `p` | Pull |
| `?` | Show all keybindings |
| `q` | Quit |
| `/` | Filter current panel |

## Use-cases

- Staging hunks interactively (press `e` on a file, then select lines)
- Interactive rebase without memorizing `git rebase -i` syntax
- Quickly squashing WIP commits before a PR
- Resolving merge conflicts with a split-pane diff view
