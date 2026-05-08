# Work Notes Tracker

A lightweight terminal tool for capturing daily work notes by category.
Notes are stored as plain Markdown files, organised by date, ready to be
fed into any summarisation tool later.

---

## Requirements

- **Python 3.10 or newer** — check with `python3 --version`
- No third-party packages needed
- Works on macOS, Linux, and WSL out of the box

---

## Installation

No installation step is required. Just download `notes.py` and run it
from whatever directory you want your notes stored in.

```bash
# put the script somewhere on your PATH (optional but convenient)
cp notes.py ~/bin/notes
chmod +x ~/bin/notes
```

Or run it directly:

```bash
python3 notes.py
```

### Optional: set your preferred editor

If `$EDITOR` is set in your shell, the tool will open it for body text
entry. If not, it falls back to a built-in inline prompt.

```bash
# add to ~/.zshrc or ~/.bashrc
export EDITOR=vim        # or nano, code --wait, etc.
```

---

## Usage

### Open the UI

```bash
python3 notes.py
```

The curses UI shows today's notes and lets you browse, create, view, and
delete notes without leaving the terminal.

#### UI keys

| Key | Action |
|---|---|
| `N` | New note — walks you through category → title → body |
| `↑` / `↓` | Move selection |
| `Enter` / `V` | View the selected note in full |
| `D` | Delete selected note (asks for confirmation) |
| `W` | Toggle between **today** and **week** view |
| `T` | Jump back to today |
| `←` / `→` | Go to previous / next day (or week when in week view) |
| `Q` | Quit |

### Add a note from the shell

Useful for quick captures without opening the UI.

```bash
# fully interactive — prompts for category, title, and body
python3 notes.py new

# skip the category prompt
python3 notes.py new -c insight -t "Redis TTL cuts latency by 40%"

# fully non-interactive (good for scripts or aliases)
python3 notes.py new -c todo -t "Write migration tests" -b "Cover new schema before Thursday."
```

### List notes

```bash
python3 notes.py list              # today (default)
python3 notes.py list --week       # current week (Mon–Sun)
python3 notes.py list --date 2026-05-06
```

### View a note

```bash
python3 notes.py view notes/2026/05/08/insight_redis-ttl-cuts-latency.md
```

---

## Categories

| Category | When to use |
|---|---|
| `general` | Anything that doesn't fit elsewhere — standup notes, updates |
| `insight` | Something you discovered or understood better today |
| `lesson-learned` | What worked, what didn't, what to do differently |
| `todo` | A task or follow-up to track |
| `blocker` | Something blocking progress |
| `decision` | A decision made and the reasoning behind it |

When creating a note interactively you can type the full name, a number,
or just the first letter (`i` → `insight`, `b` → `blocker`, etc.).

---

## File layout

Notes are stored as plain Markdown under a `notes/` folder in whichever
directory you run the script from.

```
notes/
  2026/
    05/
      08/
        insight_redis-ttl-cuts-latency.md
        blocker_prod-deploy-blocked.md
        todo_write-migration-tests.md
  _summaries/          ← reserved for future summary reports
```

Each file has a small YAML front-matter block followed by free-form Markdown:

```markdown
---
title: Redis TTL cuts latency by 40%
category: insight
date: 2026-05-08 09:32
---

Switched the auth endpoint cache TTL from 60 s to 5 min.
Response times dropped from ~180 ms to ~110 ms on p95.
Worth applying the same pattern to the user-profile service.
```

Because everything is plain text you can edit files directly, grep across
them, commit them to Git, or pipe them into any other tool.

---

## Tips

**Daily habit** — run `python3 notes.py` in a dedicated terminal tab and
keep it open alongside your work. Press `N` whenever something is worth
noting; it takes under a minute.

**Quick capture alias** — add to your shell config for fast one-liners:

```bash
alias note='python3 ~/bin/notes new'

# then from anywhere:
note -c insight -t "Learned about CRDT clocks"
```

**Feeding notes to Claude for summaries** — run `python3 notes.py list --week`
to get the file paths, then pass the files to Claude (via Claude Code,
the API, or by pasting the content) and ask for a weekly summary with
insights, lessons learned, and blockers.
