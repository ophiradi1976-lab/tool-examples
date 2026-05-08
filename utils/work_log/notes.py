#!/usr/bin/env python3
"""
notes.py — Work notes tracker.

  python notes.py                              Open curses UI
  python notes.py new [-c CATEGORY] [-t TITLE] [-b "body text"]
  python notes.py list [--week | --date YYYY-MM-DD]
  python notes.py view PATH

Categories: general, insight, lesson-learned, todo, blocker, decision

Notes are stored as Markdown under:
  notes/YYYY/MM/DD/{category}_{slug-title}.md
"""

import argparse
import curses
import os
import re
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

NOTES_DIR = Path("notes")

CATEGORIES = [
    "general",
    "insight",
    "lesson-learned",
    "todo",
    "blocker",
    "decision",
]

CAT_ABBR = {c[0]: c for c in CATEGORIES}   # g→general, i→insight, …
# collision: none in this list

CAT_ICON = {
    "general":        "📝",
    "insight":        "💡",
    "lesson-learned": "🎓",
    "todo":           "✅",
    "blocker":        "🚧",
    "decision":       "⚖️ ",
}

# ─────────────────────────────────────────────
# File helpers
# ─────────────────────────────────────────────

def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text)[:48].strip("-")


def _note_path(category: str, title: str, when: date | None = None) -> Path:
    when = when or date.today()
    folder = NOTES_DIR / when.strftime("%Y/%m/%d")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{category}_{_slugify(title)}.md"


def _write_note(path: Path, category: str, title: str, body: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    path.write_text(
        f"---\ntitle: {title}\ncategory: {category}\ndate: {now}\n---\n\n{body.strip()}\n"
    )


def _parse_note(path: Path) -> dict:
    text  = path.read_text()
    meta  = {"title": path.stem, "category": "general", "date": "", "body": ""}
    in_fm = past_fm = False
    body_lines: list[str] = []

    for line in text.splitlines():
        if line.strip() == "---":
            if not in_fm and not past_fm:
                in_fm = True
            elif in_fm:
                in_fm = False; past_fm = True
            continue
        if in_fm:
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip()
        elif past_fm:
            body_lines.append(line)

    meta["body"] = "\n".join(body_lines).strip()
    meta["path"] = str(path)
    return meta


def _collect(start: date, end: date) -> list[dict]:
    notes: list[dict] = []
    cur = start
    while cur <= end:
        folder = NOTES_DIR / cur.strftime("%Y/%m/%d")
        if folder.exists():
            for f in sorted(folder.glob("*.md")):
                notes.append(_parse_note(f))
        cur += timedelta(days=1)
    return notes


def _week_of(ref: date | None = None) -> tuple[date, date]:
    ref = ref or date.today()
    start = ref - timedelta(days=ref.weekday())
    return start, start + timedelta(days=6)

# ─────────────────────────────────────────────
# Text-entry helpers  (used both by UI and CLI)
# ─────────────────────────────────────────────

def get_body(title: str) -> str:
    """Open $EDITOR if set, otherwise fall back to inline prompt."""
    editor = os.environ.get("EDITOR", "")
    if editor:
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False) as f:
            f.write(f"# {title}\n\n")
            tmp = f.name
        try:
            subprocess.run([editor, tmp], check=True)
            lines = Path(tmp).read_text().splitlines()
            if lines and lines[0].startswith("# "):
                lines = lines[1:]
            return "\n".join(lines).strip()
        except Exception:
            pass
        finally:
            os.unlink(tmp)
    return get_body_inline()


def get_body_inline() -> str:
    W = 58
    print(f"\n  ┌{'─'*W}┐")
    print(f"  │  Enter note body. Finish with a line containing{' '*(W-48)}│")
    print(f"  │  only 'END', or Ctrl+D.{' '*(W-24)}│")
    print(f"  ├{'─'*W}┤")
    lines: list[str] = []
    try:
        while True:
            raw = input("  │ ")
            if raw.strip().upper() == "END":
                break
            lines.append(raw)
    except EOFError:
        pass
    print(f"  └{'─'*W}┘")
    return "\n".join(lines)


def pick_category_inline() -> str:
    print("\n  Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {CAT_ICON.get(cat,'  ')} {cat}")
    print()
    while True:
        raw = input("  Choose (number, name, or first letter) [general]: ").strip().lower()
        if not raw:
            return "general"
        if raw.isdigit() and 1 <= int(raw) <= len(CATEGORIES):
            return CATEGORIES[int(raw) - 1]
        if raw in CATEGORIES:
            return raw
        if raw in CAT_ABBR:
            return CAT_ABBR[raw]
        matches = [c for c in CATEGORIES if c.startswith(raw)]
        if len(matches) == 1:
            return matches[0]
        print(f"  Not recognised. Pick 1–{len(CATEGORIES)}, type a name, or a first letter.")

# ─────────────────────────────────────────────
# Curses colour pairs
# ─────────────────────────────────────────────

C_HEADER  = 1
C_GREEN   = 2
C_YELLOW  = 3
C_CYAN    = 4
C_DIM     = 5
C_SEL     = 6
C_RED     = 7

CAT_COLOR = {
    "general":        C_CYAN,
    "insight":        C_GREEN,
    "lesson-learned": C_YELLOW,
    "todo":           C_CYAN,
    "blocker":        C_RED,
    "decision":       C_YELLOW,
}

# ─────────────────────────────────────────────
# Curses UI
# ─────────────────────────────────────────────

class NotesUI:

    HELP = (
        " N new   ↑↓ select   Enter view   D delete   "
        "W week/today   ← → prev/next day   H help   Q quit "
    )

    def __init__(self, stdscr):
        self.scr    = stdscr
        self.mgr    = TaskManager()
        self.notes: list[dict] = []
        self.sel    = 0
        self.scroll = 0
        self.view_week  = False
        self.ref_date   = date.today()
        self._msg       = ""
        self._msg_err   = False

    # ── colours ───────────────────────────────

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(C_HEADER, curses.COLOR_BLACK,  curses.COLOR_WHITE)
        curses.init_pair(C_GREEN,  curses.COLOR_GREEN,  -1)
        curses.init_pair(C_YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(C_CYAN,   curses.COLOR_CYAN,   -1)
        curses.init_pair(C_DIM,    curses.COLOR_WHITE,  -1)
        curses.init_pair(C_SEL,    curses.COLOR_BLACK,  curses.COLOR_WHITE)
        curses.init_pair(C_RED,    curses.COLOR_RED,    -1)

    # ── data ──────────────────────────────────

    def reload(self):
        if self.view_week:
            start, end = _week_of(self.ref_date)
        else:
            start = end = self.ref_date
        self.notes = _collect(start, end)
        self.sel   = min(self.sel, max(0, len(self.notes) - 1))
        self._clamp_scroll()

    def _clamp_scroll(self):
        h, _ = self.scr.getmaxyx()
        list_h = max(1, h - 7)
        if self.sel < self.scroll:
            self.scroll = self.sel
        elif self.sel >= self.scroll + list_h:
            self.scroll = self.sel - list_h + 1

    # ── drawing ───────────────────────────────

    def _put(self, row, col, text, attr=0):
        h, w = self.scr.getmaxyx()
        if row < 0 or row >= h or col < 0:
            return
        avail = w - col - 1
        if avail <= 0:
            return
        try:
            self.scr.addstr(row, col, text[:avail], attr)
        except curses.error:
            pass

    def draw(self):
        self.scr.erase()
        h, w = self.scr.getmaxyx()

        # ── header ────────────────────────────
        if self.view_week:
            start, end = _week_of(self.ref_date)
            period = f"Week {start.strftime('%Y-W%V')}  ({start} → {end})"
        else:
            period = self.ref_date.strftime("%A, %Y-%m-%d")
        clock  = datetime.now().strftime(" %H:%M ")
        title  = f" WORK NOTES  ·  {period}"
        bar    = title + " " * max(0, w - len(title) - len(clock)) + clock
        self._put(0, 0, bar[:w], curses.color_pair(C_HEADER))

        # ── note count ────────────────────────
        n = len(self.notes)
        count_str = f"  {n} note{'s' if n != 1 else ''}"
        self._put(1, 1, count_str, curses.A_DIM)

        # ── divider ───────────────────────────
        self._put(2, 0, "─" * w)

        # ── column headers ────────────────────
        cat_w  = 16
        date_w = 11 if self.view_week else 0
        name_w = max(10, w - cat_w - date_w - 4)

        hdr_date = f"{'Date':<{date_w}}" if self.view_week else ""
        hdr = f" {hdr_date}{'Category':<{cat_w}}{'Title':<{name_w}}"
        self._put(3, 0, hdr, curses.A_DIM)

        # ── list ──────────────────────────────
        list_row = 4
        list_h   = max(1, h - list_row - 3)
        self._clamp_scroll()

        for i in range(list_h):
            idx = self.scroll + i
            if idx >= len(self.notes):
                break
            note = self.notes[idx]
            cat  = note["category"]

            date_col = f"{note['date'][:10]:<{date_w}}" if self.view_week else ""
            cat_col  = f"{cat:<{cat_w}}"
            title_col = note["title"][: name_w]
            line = f" {date_col}{cat_col}{title_col}"

            if idx == self.sel:
                attr = curses.color_pair(C_SEL) | curses.A_BOLD
            else:
                attr = curses.color_pair(CAT_COLOR.get(cat, C_DIM))

            self._put(list_row + i, 0, line, attr)

        # ── message ───────────────────────────
        if self._msg:
            attr = curses.color_pair(C_RED if self._msg_err else C_YELLOW)
            self._put(h - 2, 1, self._msg, attr)

        # ── help bar ──────────────────────────
        self._put(h - 1, 0, self.HELP.ljust(w)[:w], curses.A_REVERSE | curses.A_DIM)

        self.scr.refresh()

    # ── flash ─────────────────────────────────

    def flash(self, msg: str, err: bool = False):
        self._msg     = msg
        self._msg_err = err

    def clear_msg(self):
        self._msg = ""

    # ── actions (suspend curses, do I/O, resume) ──

    def action_new(self):
        """Suspend curses → interactive note creation → resume."""
        curses.endwin()
        print("\n  ── New Note " + "─" * 44)
        category = pick_category_inline()
        title    = input("\n  Title: ").strip()
        if not title:
            print("  Title cannot be empty — cancelled.\n")
            input("  Press Enter to return…")
            self.scr.refresh()
            return

        icon = CAT_ICON.get(category, "")
        print(f"\n  {icon} [{category}]  {title}")
        body = get_body(title)

        if not body.strip():
            print("\n  Empty body — note not saved.\n")
            input("  Press Enter to return…")
            self.scr.refresh()
            return

        path = _note_path(category, title)
        _write_note(path, category, title, body)
        print(f"\n  ✓ Saved → {path}")
        input("\n  Press Enter to return…")
        self.reload()
        self.flash(f"Saved: {title}")
        self.scr.refresh()

    def action_view(self):
        if not self.notes:
            return
        note = self.notes[self.sel]
        curses.endwin()
        icon = CAT_ICON.get(note["category"], "")
        W    = 60
        print(f"\n  {icon} {note['title']}")
        print(f"  [{note['category']}]  {note['date']}")
        print(f"  {'─'*W}")
        print()
        for line in note["body"].splitlines():
            print(f"  {line}")
        print(f"\n  {'─'*W}")
        input("\n  Press Enter to return…")
        self.scr.refresh()

    def action_delete(self):
        if not self.notes:
            return
        note = self.notes[self.sel]
        curses.endwin()
        print(f"\n  Delete note: {note['title']}  [{note['category']}]")
        confirm = input("  Confirm? (y/N): ").strip().lower()
        if confirm == "y":
            Path(note["path"]).unlink(missing_ok=True)
            self.reload()
            self.flash(f"Deleted: {note['title']}")
        else:
            self.flash("Delete cancelled.")
        self.scr.refresh()

    # ── help overlay ──────────────────────────

    HELP_LINES = [
        ("UI KEYS",                    None),
        ("↑ / ↓",                      "Move selection"),
        ("Enter / V",                  "View selected note in full"),
        ("N",                          "New note  (category → title → body)"),
        ("D",                          "Delete selected note  (asks confirmation)"),
        ("W",                          "Toggle today ↔ week view"),
        ("T",                          "Jump back to today"),
        ("← / →",                      "Previous / next day  (or week in week view)"),
        ("H / ?",                      "Show this help screen"),
        ("Q",                          "Quit"),
        ("", None),
        ("SHELL COMMANDS",             None),
        ("notes.py new",               "Fully interactive — prompts for everything"),
        ("notes.py new -c CAT -t TTL", "Skip prompts for category and title"),
        ("notes.py new … -b 'text'",   "Non-interactive, body inline"),
        ("notes.py list",              "List today's notes"),
        ("notes.py list --week",       "List this week's notes"),
        ("notes.py list --date DATE",  "List notes for a specific date"),
        ("notes.py view PATH",         "Print a note to the terminal"),
        ("", None),
        ("CATEGORIES",                 None),
        ("general  (g)",               "Standup notes, updates, anything general"),
        ("insight  (i)",               "Something discovered or understood today"),
        ("lesson-learned  (l)",        "What worked, what didn't, what to change"),
        ("todo  (t)",                  "Task or follow-up to track"),
        ("blocker  (b)",               "Something blocking progress"),
        ("decision  (d)",              "A decision made and its reasoning"),
        ("", None),
        ("FILES",                      None),
        ("notes/YYYY/MM/DD/",          "One folder per day"),
        ("{category}_{slug}.md",       "One Markdown file per note"),
    ]

    def _show_help(self):
        h, w = self.scr.getmaxyx()

        box_w = min(72, w - 4)
        box_h = len(self.HELP_LINES) + 4
        top   = max(0, (h - box_h) // 2)
        left  = max(0, (w - box_w) // 2)

        for r in range(box_h):
            self._put(top + r, left, " " * box_w, curses.A_REVERSE)

        self._put(top,           left, "┌" + "─" * (box_w - 2) + "┐", curses.A_REVERSE)
        self._put(top + box_h-1, left, "└" + "─" * (box_w - 2) + "┘", curses.A_REVERSE)

        title = "  HELP  "
        self._put(top, left + (box_w - len(title)) // 2, title,
                  curses.A_REVERSE | curses.A_BOLD)

        inner_w = box_w - 4
        key_col = 28

        for i, (key, desc) in enumerate(self.HELP_LINES):
            row = top + 2 + i
            if desc is None:
                self._put(row, left + 2, f"│ {key:<{inner_w}} │",
                          curses.A_REVERSE | curses.A_BOLD)
            elif key == "":
                self._put(row, left + 2, f"│ {'':<{inner_w}} │", curses.A_REVERSE)
            else:
                cell = f"{key:<{key_col}}{desc}"
                self._put(row, left + 2, f"│ {cell:<{inner_w}} │", curses.A_REVERSE)

        dismiss = "  press any key to close  "
        self._put(top + box_h - 1,
                  left + (box_w - len(dismiss)) // 2,
                  dismiss, curses.A_REVERSE | curses.A_DIM)

        self.scr.refresh()
        self.scr.timeout(-1)
        self.scr.getch()
        self.scr.timeout(30_000)
        self.scr.clear()

    # ── key handling ──────────────────────────

    def handle_key(self, key: int):
        self.clear_msg()
        n = len(self.notes)

        if key == curses.KEY_UP and n:
            self.sel = max(0, self.sel - 1)

        elif key == curses.KEY_DOWN and n:
            self.sel = min(n - 1, self.sel + 1)

        elif key in (curses.KEY_LEFT,):
            self.ref_date -= timedelta(days=7 if self.view_week else 1)
            self.sel = 0
            self.reload()

        elif key in (curses.KEY_RIGHT,):
            self.ref_date += timedelta(days=7 if self.view_week else 1)
            self.sel = 0
            self.reload()

        elif key in (ord("n"), ord("N")):
            self.action_new()

        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r"), ord("v"), ord("V")):
            self.action_view()

        elif key in (ord("d"), ord("D")):
            self.action_delete()

        elif key in (ord("w"), ord("W")):
            self.view_week = not self.view_week
            self.sel = 0
            self.reload()

        elif key in (ord("t"), ord("T")):
            self.ref_date  = date.today()
            self.view_week = False
            self.sel = 0
            self.reload()

        elif key in (ord("h"), ord("H"), ord("?")):
            self._show_help()

        elif key == curses.KEY_RESIZE:
            self.scr.clear()

    # ── main loop ─────────────────────────────

    def run(self):
        self._init_colors()
        curses.curs_set(0)
        self.scr.timeout(30_000)   # refresh every 30 s (clock update)
        self.reload()

        while True:
            self.draw()
            key = self.scr.getch()
            if key in (ord("q"), ord("Q")):
                break
            if key != -1:
                self.handle_key(key)


# ─────────────────────────────────────────────
# Dummy shim so NotesUI can reference TaskManager
# (kept in case tracker.py is imported later)
# ─────────────────────────────────────────────

class TaskManager:
    pass


# ─────────────────────────────────────────────
# CLI commands
# ─────────────────────────────────────────────

def cmd_new(args):
    category = args.category
    if category and category not in CATEGORIES:
        sys.exit(f"Unknown category '{category}'. Valid: {', '.join(CATEGORIES)}")
    if not category:
        category = pick_category_inline()

    title = args.title or input("\n  Title: ").strip()
    if not title:
        sys.exit("Title cannot be empty.")

    if args.body:
        body = args.body
    else:
        icon = CAT_ICON.get(category, "")
        print(f"\n  {icon} [{category}]  {title}")
        body = get_body(title)

    if not body.strip():
        print("  Empty body — note not saved.")
        return

    path = _note_path(category, title)
    _write_note(path, category, title, body)
    print(f"\n  ✓ Saved → {path}\n")


def cmd_list(args):
    if args.week:
        start, end = _week_of()
        label = f"week {start.strftime('%Y-W%V')}  ({start} → {end})"
    elif args.date:
        d = date.fromisoformat(args.date)
        start = end = d
        label = args.date
    else:
        start = end = date.today()
        label = f"today ({date.today()})"

    notes = _collect(start, end)
    if not notes:
        print(f"\n  No notes for {label}.\n")
        return

    print(f"\n  Notes — {label}  [{len(notes)} total]")
    cur_day = None
    for n in notes:
        day = n["date"][:10]
        if day != cur_day:
            print(f"\n  ── {day} {'─'*42}")
            cur_day = day
        icon = CAT_ICON.get(n["category"], "  ")
        print(f"    {icon} [{n['category']:<15}]  {n['title']}")
        print(f"       {n['path']}")
    print()


def cmd_view(args):
    p = Path(args.path)
    if not p.exists():
        sys.exit(f"File not found: {p}")
    n    = _parse_note(p)
    icon = CAT_ICON.get(n["category"], "")
    print(f"\n  {icon} {n['title']}")
    print(f"  [{n['category']}]  {n['date']}")
    print(f"  {'─'*58}")
    print()
    for line in n["body"].splitlines():
        print(f"  {line}")
    print()


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

def main():
    p   = argparse.ArgumentParser(
        prog="notes",
        description="Work notes tracker. Run without arguments to open the UI.",
    )
    sub = p.add_subparsers(dest="cmd")

    # new
    n = sub.add_parser("new", help="Add a note (non-interactive)")
    n.add_argument("-c", "--category", help=f"One of: {', '.join(CATEGORIES)}")
    n.add_argument("-t", "--title",    help="Note title")
    n.add_argument("-b", "--body",     help="Body text (skips editor/prompt)")

    # list
    ls  = sub.add_parser("list", help="List notes")
    grp = ls.add_mutually_exclusive_group()
    grp.add_argument("--week", action="store_true", help="Current week")
    grp.add_argument("--date", metavar="YYYY-MM-DD", help="Specific date")

    # view
    v = sub.add_parser("view", help="View a note by file path")
    v.add_argument("path")

    args = p.parse_args()

    if args.cmd == "new":
        cmd_new(args)
    elif args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "view":
        cmd_view(args)
    else:
        curses.wrapper(lambda s: NotesUI(s).run())


if __name__ == "__main__":
    main()
