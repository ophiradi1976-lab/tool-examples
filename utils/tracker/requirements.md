# Requirements

## Python version

Python **3.10 or newer** is required.  
The script uses built-in type-hint syntax (`list[dict]`, `X | None`) introduced in 3.10.

Check your version:

```bash
python3 --version
```

If you are on an older version, upgrade via your system package manager or [python.org](https://www.python.org/downloads/).

---

## Dependencies

**No third-party packages are needed.**  
The script uses only Python standard-library modules:

| Module     | Purpose                        |
|------------|-------------------------------|
| `curses`   | Terminal UI                    |
| `argparse` | CLI argument parsing           |
| `pathlib`  | File path handling             |
| `datetime` | Timestamps and duration math   |
| `time`     | Flash-message expiry           |

---

## Platform notes

### macOS / Linux
Works out of the box. `curses` is included in the standard library on all Unix-like systems.

### Windows
The `curses` module is **not** included in the Windows Python distribution.  
Install the drop-in replacement before running:

```bash
pip install windows-curses
```

No other changes to the script are needed.

### Windows Subsystem for Linux (WSL)
Treat it like Linux — no extra steps required.

---

## Files created at runtime

The tracker creates two Markdown files in the **same directory you run it from**:

| File        | Contents                              |
|-------------|--------------------------------------|
| `tasks.md`  | Task list (ID, name, status, …)      |
| `log.md`    | Append-only event log (start/pause)  |

Both files are plain Markdown tables and can be edited directly in any text editor.
