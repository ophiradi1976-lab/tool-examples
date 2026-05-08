# Task Tracker

A minimal terminal task tracker with time logging, written in Python.  
Tracks time spent per task across sessions — useful for focused work and Pomodoro-style timing.

---

## Quick start

```bash
# Add your first tasks
python tracker.py add -n "Fix login bug" -d "OAuth flow broken on mobile" -l "https://jira.example.com/T-1"
python tracker.py add -n "Write unit tests"

# Open the live UI
python tracker.py
```

---

## CLI commands

All commands are run from the shell (outside the UI).

| Command | Description |
|---|---|
| `python tracker.py` | Open the curses UI |
| `python tracker.py add -n NAME` | Add a task (name required) |
| `python tracker.py add -n NAME -d "Description" -l "https://..."` | Add with description and link |
| `python tracker.py remove ID` | Delete a task by ID |
| `python tracker.py done ID` | Mark a task as done from the shell |
| `python tracker.py summary` | Print time totals for all tasks |

---

## UI keys

Open the UI with `python tracker.py`, then:

| Key | Action |
|---|---|
| `↑` / `↓` | Move selection |
| `Enter` or `S` | Start the selected task (auto-pauses any currently running task) |
| `P` | Pause the active task |
| `D` | Mark the selected task as done |
| `H` or `?` | Show help overlay |
| `Q` | Quit |

---

## What the UI shows

```
 TASK TRACKER                                        14:32:07
▶ Fix login bug
  session 00:12  total 1:04:38  (3 sessions)
  https://jira.example.com/T-1
────────────────────────────────────────────────────────────
  # Name                           Status          Time
  1 Fix login bug                  ▶ IN PROGRESS   1:04:38
  2 Write unit tests               ⏸ PAUSED        00:25
  3 Update README                    PENDING        --:--
  4 Refactor auth module           ✓ DONE          2:10:04
────────────────────────────────────────────────────────────
 ↑↓ select   Enter start   P pause   D done   H help   Q quit
```

- **Top panel** — active task name, live session timer, cumulative total time, and link if set.
- **Task list** — colour-coded: green = running, yellow = paused, dim = done.
- The timer refreshes every 500 ms.

---

## Data files

Two Markdown files are created automatically in the directory you run the script from.  
You can edit them directly in any text editor — changes are picked up the next time the UI refreshes.

### `tasks.md`

| ID | Date | Name | Description | Link | Status |
|----|------|------|-------------|------|--------|
| 1 | 2026-05-08 | Fix login bug | OAuth flow | https://jira.example.com/T-1 | in_progress |

**Status values:** `pending` · `in_progress` · `paused` · `done`

### `log.md`

| TaskID | Event | Timestamp |
|--------|-------|-----------|
| 1 | start | 2026-05-08 09:00:00 |
| 1 | pause | 2026-05-08 09:25:00 |

**Events:** `start` · `pause`  
The log is append-only. Time totals are computed from this file.

---

## Summary output

```bash
python tracker.py summary
```

```
══════════════════════════════════════════════════════════════════
  TASK SUMMARY  ·  2026-05-08 14:35
══════════════════════════════════════════════════════════════════

  ── IN PROGRESS ─────────────────────────────────
  #  1  Fix login bug                      1h 04m 38s   3 session(s)

  ── PAUSED ──────────────────────────────────────
  #  2  Write unit tests                   0h 25m 00s   1 session(s)

  ── PENDING ─────────────────────────────────────
  #  3  Update README                      0h 00m 00s   0 session(s)

  ── DONE ────────────────────────────────────────
  #  4  Refactor auth module               2h 10m 04s   5 session(s)
```
