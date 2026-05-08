#!/usr/bin/env python3
"""
tracker.py — Terminal task tracker with time logging.

Usage:
  python tracker.py                              # Launch curses UI
  python tracker.py add -n NAME [-d DESC] [-l LINK]
  python tracker.py remove ID
  python tracker.py done ID
  python tracker.py summary
"""

import curses
import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

TASKS_FILE = "tasks.md"
LOG_FILE   = "log.md"

TASK_HEADERS = ["ID", "Date", "Name", "Description", "Link", "Status"]
LOG_HEADERS  = ["TaskID", "Event", "Timestamp"]

TS_FMT = "%Y-%m-%d %H:%M:%S"

# ─────────────────────────────────────────────
# Markdown table helpers
# ─────────────────────────────────────────────

def _parse_md_table(filepath: str) -> list[dict]:
    p = Path(filepath)
    if not p.exists():
        return []
    lines = [l.rstrip() for l in p.read_text().splitlines() if l.strip().startswith("|")]
    if len(lines) < 3:
        return []
    headers = [h.strip() for h in lines[0].split("|")[1:-1]]
    rows = []
    for line in lines[2:]:
        vals = [v.strip() for v in line.split("|")[1:-1]]
        if len(vals) == len(headers):
            rows.append(dict(zip(headers, vals)))
    return rows


def _write_md_table(filepath: str, headers: list, rows: list[dict], title: str | None = None):
    if not rows:
        col_widths = [max(6, len(h)) for h in headers]
    else:
        col_widths = [
            max(len(h), max(len(str(r.get(h, ""))) for r in rows))
            for h in headers
        ]

    def fmt(vals):
        return "| " + " | ".join(str(v).ljust(w) for v, w in zip(vals, col_widths)) + " |"

    sep = "| " + " | ".join("-" * w for w in col_widths) + " |"
    lines = []
    if title:
        lines += [f"# {title}", ""]
    lines.append(fmt(headers))
    lines.append(sep)
    for row in rows:
        lines.append(fmt([row.get(h, "") for h in headers]))
    Path(filepath).write_text("\n".join(lines) + "\n")


# ─────────────────────────────────────────────
# Task Manager
# ─────────────────────────────────────────────

class TaskManager:

    # ── persistence ──────────────────────────

    def load_tasks(self) -> list[dict]:
        return _parse_md_table(TASKS_FILE)

    def _save_tasks(self, tasks: list[dict]):
        _write_md_table(TASKS_FILE, TASK_HEADERS, tasks, title="Tasks")

    def load_log(self) -> list[dict]:
        return _parse_md_table(LOG_FILE)

    def _append_log(self, task_id: str, event: str):
        logs = self.load_log()
        logs.append({
            "TaskID":    str(task_id),
            "Event":     event,
            "Timestamp": datetime.now().strftime(TS_FMT),
        })
        _write_md_table(LOG_FILE, LOG_HEADERS, logs, title="Work Log")

    # ── queries ───────────────────────────────

    def _next_id(self) -> int:
        tasks = self.load_tasks()
        return max((int(t["ID"]) for t in tasks), default=0) + 1

    def active_task(self) -> dict | None:
        return next((t for t in self.load_tasks() if t["Status"] == "in_progress"), None)

    def compute_time(self, task_id: str) -> tuple[int, int]:
        """Return (total_seconds, session_count) for a task, including live time."""
        logs = [l for l in self.load_log() if l["TaskID"] == str(task_id)]
        total, sessions, start_ts = 0, 0, None
        for entry in logs:
            ts = datetime.strptime(entry["Timestamp"], TS_FMT)
            if entry["Event"] == "start":
                start_ts = ts
                sessions += 1
            elif entry["Event"] == "pause" and start_ts:
                total += int((ts - start_ts).total_seconds())
                start_ts = None
        if start_ts:                                    # task still running
            total += int((datetime.now() - start_ts).total_seconds())
        return total, sessions

    def last_start_ts(self, task_id: str) -> datetime | None:
        """Timestamp of the most recent 'start' event for a task."""
        logs = [l for l in self.load_log() if l["TaskID"] == str(task_id)]
        for entry in reversed(logs):
            if entry["Event"] == "start":
                return datetime.strptime(entry["Timestamp"], TS_FMT)
        return None

    # ── mutations ─────────────────────────────

    def add_task(self, name: str, description: str = "", link: str = ""):
        tasks = self.load_tasks()
        task = {
            "ID":          str(self._next_id()),
            "Date":        datetime.now().strftime("%Y-%m-%d"),
            "Name":        name,
            "Description": description,
            "Link":        link,
            "Status":      "pending",
        }
        tasks.append(task)
        self._save_tasks(tasks)
        print(f"Added task #{task['ID']}: {name}")

    def remove_task(self, task_id: int):
        tasks = self.load_tasks()
        new = [t for t in tasks if t["ID"] != str(task_id)]
        if len(new) == len(tasks):
            print(f"Task #{task_id} not found.")
            return
        self._save_tasks(new)
        print(f"Removed task #{task_id}.")

    def start_task(self, task_id: str) -> bool:
        tasks = self.load_tasks()
        # auto-pause any running task
        for t in tasks:
            if t["Status"] == "in_progress":
                t["Status"] = "paused"
                self._append_log(t["ID"], "pause")
        # start selected
        target = next((t for t in tasks if t["ID"] == str(task_id)), None)
        if target is None or target["Status"] == "done":
            self._save_tasks(tasks)
            return False
        target["Status"] = "in_progress"
        self._save_tasks(tasks)
        self._append_log(task_id, "start")
        return True

    def pause_task(self, task_id: str) -> bool:
        tasks = self.load_tasks()
        target = next((t for t in tasks if t["ID"] == str(task_id)), None)
        if target is None or target["Status"] != "in_progress":
            return False
        target["Status"] = "paused"
        self._save_tasks(tasks)
        self._append_log(task_id, "pause")
        return True

    def mark_done(self, task_id: int):
        tasks = self.load_tasks()
        target = next((t for t in tasks if t["ID"] == str(task_id)), None)
        if target is None:
            print(f"Task #{task_id} not found.")
            return
        if target["Status"] == "in_progress":
            self._append_log(str(task_id), "pause")
        target["Status"] = "done"
        self._save_tasks(tasks)
        print(f"Task #{task_id} marked as done.")

    # ── summary ───────────────────────────────

    def summary(self):
        tasks = self.load_tasks()
        if not tasks:
            print("No tasks found.")
            return

        def fmt(secs):
            h, r = divmod(secs, 3600)
            m, s = divmod(r, 60)
            return f"{h}h {m:02d}m {s:02d}s"

        groups = [
            ("IN PROGRESS", [t for t in tasks if t["Status"] == "in_progress"]),
            ("PAUSED",      [t for t in tasks if t["Status"] == "paused"]),
            ("PENDING",     [t for t in tasks if t["Status"] == "pending"]),
            ("DONE",        [t for t in tasks if t["Status"] == "done"]),
        ]

        print(f"\n{'═'*66}")
        print(f"  TASK SUMMARY  ·  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'═'*66}")

        for label, group in groups:
            if not group:
                continue
            print(f"\n  ── {label} {'─'*(50-len(label))}")
            for t in group:
                secs, sessions = self.compute_time(t["ID"])
                link = f"  {t['Link']}" if t.get("Link") else ""
                name = t["Name"][:35]
                print(f"  #{t['ID']:>3}  {name:<36} {fmt(secs):>14}  {sessions} session(s){link}")

        print()


# ─────────────────────────────────────────────
# Curses UI
# ─────────────────────────────────────────────

# color pair indices
C_DEFAULT  = 0
C_GREEN    = 1   # in_progress
C_YELLOW   = 2   # paused / flash message
C_DIM      = 3   # done / hints
C_CYAN     = 4   # links / accent
C_SEL      = 5   # selected row (reverse)
C_HEADER   = 6   # top bar

STATUS_COLOR = {
    "in_progress": C_GREEN,
    "paused":      C_YELLOW,
    "pending":     C_DEFAULT,
    "done":        C_DIM,
}

STATUS_LABEL = {
    "in_progress": "▶ IN PROGRESS",
    "paused":      "⏸ PAUSED",
    "pending":     "  PENDING",
    "done":        "✓ DONE",
}


def _fmt_dur(seconds: int) -> str:
    h, r = divmod(seconds, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


class TrackerUI:

    REFRESH_MS = 500      # timer tick

    def __init__(self, stdscr, mgr: TaskManager):
        self.scr  = stdscr
        self.mgr  = mgr
        self.sel  = 0
        self.tasks: list[dict] = []
        self.active_start: datetime | None = None
        self._msg      = ""
        self._msg_time = 0.0
        self._scroll   = 0          # top-visible row index

    # ── setup ────────────────────────────────

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(C_GREEN,  curses.COLOR_GREEN,  -1)
        curses.init_pair(C_YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(C_DIM,    8 if curses.COLORS >= 256 else curses.COLOR_WHITE, -1)
        curses.init_pair(C_CYAN,   curses.COLOR_CYAN,   -1)
        curses.init_pair(C_SEL,    curses.COLOR_BLACK,  curses.COLOR_WHITE)
        curses.init_pair(C_HEADER, curses.COLOR_BLACK,  curses.COLOR_WHITE)

    # ── data ─────────────────────────────────

    def reload(self):
        self.tasks = self.mgr.load_tasks()
        self.sel   = min(self.sel, max(0, len(self.tasks) - 1))
        active = next((t for t in self.tasks if t["Status"] == "in_progress"), None)
        if active:
            self.active_start = self.mgr.last_start_ts(active["ID"])
        else:
            self.active_start = None
        self._clamp_scroll()

    def _active(self) -> dict | None:
        return next((t for t in self.tasks if t["Status"] == "in_progress"), None)

    # ── drawing ───────────────────────────────

    def _clamp_scroll(self):
        h, _ = self.scr.getmaxyx()
        list_h = max(1, h - 9)                 # rows available for task list
        if self.sel < self._scroll:
            self._scroll = self.sel
        elif self.sel >= self._scroll + list_h:
            self._scroll = self.sel - list_h + 1

    def _safe_addstr(self, row, col, text, attr=0):
        h, w = self.scr.getmaxyx()
        if row < 0 or row >= h:
            return
        max_len = w - col - 1
        if max_len <= 0:
            return
        try:
            self.scr.addstr(row, col, text[:max_len], attr)
        except curses.error:
            pass

    def draw(self):
        self.scr.erase()
        h, w = self.scr.getmaxyx()
        now  = datetime.now()
        active = self._active()

        # ── top bar ──────────────────────────
        clock = now.strftime(" %H:%M:%S ")
        title = " TASK TRACKER"
        bar   = title + " " * max(0, w - len(title) - len(clock)) + clock
        self._safe_addstr(0, 0, bar[:w], curses.color_pair(C_HEADER))

        # ── active task panel (rows 1–4) ──────
        if active:
            elapsed_s = int((now - self.active_start).total_seconds()) if self.active_start else 0
            total_s, sessions = self.mgr.compute_time(active["ID"])

            # row 1: task name
            label = "▶ "
            name  = active["Name"]
            self._safe_addstr(1, 1, label, curses.color_pair(C_GREEN) | curses.A_BOLD)
            self._safe_addstr(1, 3, name, curses.color_pair(C_GREEN) | curses.A_BOLD)

            # row 2: session timer  |  cumulative
            session_str = f"  session {_fmt_dur(elapsed_s)}   total {_fmt_dur(total_s)}   ({sessions} session{'s' if sessions != 1 else ''})"
            self._safe_addstr(2, 1, session_str, curses.color_pair(C_GREEN))

            # row 3: link if any
            if active.get("Link"):
                self._safe_addstr(3, 3, active["Link"], curses.color_pair(C_CYAN))
        else:
            self._safe_addstr(1, 1, "No active task", curses.color_pair(C_YELLOW))
            self._safe_addstr(2, 1, "Press Enter to start the selected task", curses.A_DIM)

        # ── divider ───────────────────────────
        self._safe_addstr(4, 0, "─" * w)

        # ── column headers ────────────────────
        id_w   = 3
        st_w   = 14
        tm_w   = 7
        name_w = max(10, w - id_w - st_w - tm_w - 7)

        hdr = f" {'#':>{id_w}}  {'Name':<{name_w}}  {'Status':<{st_w}}  {'Time':>{tm_w}} "
        self._safe_addstr(5, 0, hdr, curses.A_DIM)

        # ── task rows ─────────────────────────
        list_row = 6
        list_h   = max(1, h - list_row - 2)
        self._clamp_scroll()

        for i in range(list_h):
            idx = self._scroll + i
            if idx >= len(self.tasks):
                break
            t      = self.tasks[idx]
            secs, _ = self.mgr.compute_time(t["ID"])
            sl     = STATUS_LABEL.get(t["Status"], t["Status"])
            tm     = _fmt_dur(secs) if secs else "--:--"
            name   = t["Name"][:name_w]
            line   = f" {t['ID']:>{id_w}}  {name:<{name_w}}  {sl:<{st_w}}  {tm:>{tm_w}} "

            if idx == self.sel:
                attr = curses.color_pair(C_SEL) | curses.A_BOLD
            else:
                attr = curses.color_pair(STATUS_COLOR.get(t["Status"], C_DEFAULT))
                if t["Status"] == "done":
                    attr |= curses.A_DIM

            self._safe_addstr(list_row + i, 0, line, attr)

        # ── flash message ─────────────────────
        msg_row = h - 2
        if self._msg and (time.time() - self._msg_time) < 3:
            self._safe_addstr(msg_row, 1, self._msg, curses.color_pair(C_YELLOW))

        # ── help bar ─────────────────────────
        help_str = " ↑↓ select   Enter start   P pause   D done   H help   Q quit "
        self._safe_addstr(h - 1, 0, help_str.ljust(w)[:w], curses.A_REVERSE | curses.A_DIM)

        self.scr.refresh()

    # ── help overlay ──────────────────────────

    HELP_LINES = [
        ("UI KEYS", None),
        ("↑ / ↓",        "Select a task"),
        ("Enter / S",    "Start selected task  (auto-pauses current)"),
        ("P",            "Pause the active task"),
        ("D",            "Mark selected task as done"),
        ("H / ?",        "Show this help screen"),
        ("Q",            "Quit"),
        ("", None),
        ("CLI COMMANDS", None),
        ("tracker.py add -n NAME [-d DESC] [-l URL]", "Add a task"),
        ("tracker.py remove ID",                      "Delete a task"),
        ("tracker.py done ID",                        "Mark a task done"),
        ("tracker.py summary",                        "Print time summary"),
        ("", None),
        ("FILES", None),
        ("tasks.md",  "Task list  (editable directly)"),
        ("log.md",    "Append-only event log  (start / pause)"),
    ]

    def _show_help(self):
        """Draw a centered modal overlay and wait for any key to dismiss."""
        h, w = self.scr.getmaxyx()

        box_w = min(68, w - 4)
        box_h = len(self.HELP_LINES) + 4
        top   = max(0, (h - box_h) // 2)
        left  = max(0, (w - box_w) // 2)

        # shadow + box fill
        for r in range(box_h):
            self._safe_addstr(top + r, left, " " * box_w, curses.A_REVERSE)

        # border lines
        self._safe_addstr(top,           left, "┌" + "─" * (box_w - 2) + "┐", curses.A_REVERSE)
        self._safe_addstr(top + box_h-1, left, "└" + "─" * (box_w - 2) + "┘", curses.A_REVERSE)

        title = "  HELP  "
        self._safe_addstr(top, left + (box_w - len(title)) // 2, title,
                          curses.A_REVERSE | curses.A_BOLD)

        inner_w = box_w - 4
        key_col  = 34           # width reserved for the key/command column

        for i, entry in enumerate(self.HELP_LINES):
            row = top + 2 + i
            key, desc = entry

            if desc is None:
                # section header
                self._safe_addstr(row, left + 2, f"│ {key:<{inner_w}} │",
                                  curses.A_REVERSE | curses.A_BOLD)
            elif key == "":
                self._safe_addstr(row, left + 2, f"│ {'':<{inner_w}} │", curses.A_REVERSE)
            else:
                cell = f"{key:<{key_col}}{desc}"
                self._safe_addstr(row, left + 2, f"│ {cell:<{inner_w}} │", curses.A_REVERSE)

        dismiss = "  press any key to close  "
        self._safe_addstr(top + box_h - 1,
                          left + (box_w - len(dismiss)) // 2,
                          dismiss, curses.A_REVERSE | curses.A_DIM)

        self.scr.refresh()
        self.scr.timeout(-1)        # block until a key is pressed
        self.scr.getch()
        self.scr.timeout(self.REFRESH_MS)
        self.scr.clear()            # force full redraw

    # ── input ─────────────────────────────────

    def _flash(self, msg: str):
        self._msg      = msg
        self._msg_time = time.time()

    def handle_key(self, key: int):
        n = len(self.tasks)

        if key == curses.KEY_UP and n:
            self.sel = max(0, self.sel - 1)

        elif key == curses.KEY_DOWN and n:
            self.sel = min(n - 1, self.sel + 1)

        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r"), ord("s"), ord("S")):
            if n:
                t = self.tasks[self.sel]
                if t["Status"] == "done":
                    self._flash("Task is already done.")
                else:
                    self.mgr.start_task(t["ID"])
                    self.reload()
                    self._flash(f"Started: {t['Name']}")

        elif key in (ord("p"), ord("P")):
            active = self._active()
            if active:
                self.mgr.pause_task(active["ID"])
                self.reload()
                self._flash(f"Paused: {active['Name']}")
            else:
                self._flash("No active task.")

        elif key in (ord("d"), ord("D")):
            if n:
                t = self.tasks[self.sel]
                self.mgr.mark_done(int(t["ID"]))
                self.reload()
                self._flash(f"Done: {t['Name']}")

        elif key in (ord("h"), ord("H"), ord("?")):
            self._show_help()

        elif key == curses.KEY_RESIZE:
            self.scr.clear()

    # ── main loop ─────────────────────────────

    def run(self):
        self._init_colors()
        curses.curs_set(0)
        self.scr.timeout(self.REFRESH_MS)
        self.reload()

        while True:
            self.draw()
            key = self.scr.getch()
            if key in (ord("q"), ord("Q")):
                break
            if key != -1:
                self.handle_key(key)


# ─────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tracker",
        description="Terminal task tracker. Run without arguments to open the UI.",
    )
    sub = p.add_subparsers(dest="cmd")

    # add
    a = sub.add_parser("add", help="Add a task")
    a.add_argument("-n", "--name",  required=True, help="Task name")
    a.add_argument("-d", "--desc",  default="",   help="Description")
    a.add_argument("-l", "--link",  default="",   help="Jira/tool URL")

    # remove
    r = sub.add_parser("remove", help="Remove a task by ID")
    r.add_argument("id", type=int)

    # done
    d = sub.add_parser("done", help="Mark task as done")
    d.add_argument("id", type=int)

    # summary
    sub.add_parser("summary", help="Print a time summary")

    return p


def main():
    args = build_parser().parse_args()
    mgr  = TaskManager()

    if args.cmd == "add":
        mgr.add_task(args.name, args.desc, args.link)
    elif args.cmd == "remove":
        mgr.remove_task(args.id)
    elif args.cmd == "done":
        mgr.mark_done(args.id)
    elif args.cmd == "summary":
        mgr.summary()
    else:
        curses.wrapper(lambda s: TrackerUI(s, mgr).run())


if __name__ == "__main__":
    main()

