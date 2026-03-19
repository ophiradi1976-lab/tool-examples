# Claude Code — Barebones Demo Setup

Demonstrates all four Claude Code extension layers in one minimal project.

---

## Folder Structure

```
my-project/
├── CLAUDE.md                        ← Always-loaded project rules & context
├── .claude/
│   ├── settings.json                ← Hook wiring (which scripts fire on which events)
│   ├── skills/
│   │   └── git-commit.md            ← Skill: repeatable git commit workflow
│   ├── agents/
│   │   └── code-reviewer.md         ← Sub-agent: isolated code review worker
│   └── hooks/
│       ├── pre-tool.sh              ← PreToolUse: runs before Bash calls (can block)
│       └── post-tool.sh             ← PostToolUse: runs after Write calls (logging/fmt)
└── logs/
    └── claude-activity.log          ← Auto-created by hooks
```

---

## What Each Layer Does

| Layer | File(s) | When it runs | Can block Claude? |
|---|---|---|---|
| **CLAUDE.md** | `CLAUDE.md` | Always, at session start | N/A — it's instructions |
| **Skill** | `.claude/skills/*.md` | When Claude's context matches the description | No |
| **Sub-agent** | `.claude/agents/*.md` | When Claude or you delegates a task to it | No |
| **Hook** | `.claude/hooks/*.sh` + `settings.json` | On every matching tool event | Yes (exit 2) |

---

## Setup & Run

```bash
# 1. Install Claude Code (requires Node 18+)
npm install -g @anthropic-ai/claude-code

# 2. Go to your project
cd my-project

# 3. Make hooks executable (required — hooks won't fire otherwise)
chmod +x .claude/hooks/pre-tool.sh
chmod +x .claude/hooks/post-tool.sh

# 4. Launch Claude Code
claude
```

---

## Track Output in Real Time

Open a **second terminal** and run:

```bash
# Stream the activity log as Claude works
tail -f logs/claude-activity.log
```

Example log output:
```
[2026-03-19 14:02:11] PRE-TOOL  | Bash | git status
[2026-03-19 14:02:12] PRE-TOOL  | Bash | git diff
[2026-03-19 14:02:15] POST-TOOL | Write | src/api.py
[2026-03-19 14:02:15] AUTO-FMT  | black | src/api.py
[2026-03-19 14:02:20] PRE-TOOL  | Bash | rm -rf tmp/
[2026-03-19 14:02:20] BLOCKED: rm -rf is not allowed. Use rm -i instead.
```

---

## Try These Prompts Inside Claude Code

```
# Trigger the skill
"Commit my changes"

# Trigger the sub-agent
"Review src/api.py"

# Trigger the pre-tool block
"Delete the tmp folder with rm -rf"

# Watch post-tool hook auto-format
"Write a basic Python hello world to hello.py"
```

---

## Try running as one-off
```
# Will need git permission
claude -p "Commit the files, including under .claude but not under logs" --allowedTools "Bash(git add:*)" "Bash(git commit:*)" "Bash(git status)" "Bash(git diff)"

# Will need and write permissions
claude -p "Create .gitignore, add logs/ to it and commit the .gitignore" --allowedTools "Bash" "write"
```

---
## How Hooks Block Commands

In `pre-tool.sh`, `exit 2` blocks the command and sends your stderr message
back to Claude as an error — Claude will see it and adjust its approach.

```bash
echo "BLOCKED: rm -rf is not allowed." >&2
exit 2   # ← this is the magic
```

`exit 0` = allow, `exit 2` = block + explain.

---

## Notes

- `$CLAUDE_PROJECT_DIR` is injected by Claude Code into hook environments
- Sub-agents get their own isolated context window — they cannot see the main conversation
- Skills are loaded progressively (only when the description matches), keeping context clean
- CLAUDE.md is always loaded at session start, so keep it short and high-signal
