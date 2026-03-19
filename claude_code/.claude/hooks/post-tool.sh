#!/usr/bin/env bash
# .claude/hooks/post-tool.sh
#
# PostToolUse hook — fires AFTER every Write tool call (file created/edited).
# Use this for logging, auto-formatting, notifications, etc.
# Exit code here does NOT block anything — the write already happened.

LOG="$CLAUDE_PROJECT_DIR/logs/claude-activity.log"
mkdir -p "$(dirname "$LOG")"

# Parse the file path written from the JSON stdin payload
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c \
  "import sys, json; print(json.load(sys.stdin)['tool_input'].get('file_path', '?'))" 2>/dev/null)

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] POST-TOOL | Write | $FILE" >> "$LOG"

# --- Demo: auto-format Python files after write ---
if [[ "$FILE" == *.py ]]; then
  if command -v black &>/dev/null; then
    black "$FILE" --quiet 2>/dev/null
    echo "[$TIMESTAMP] AUTO-FMT  | black | $FILE" >> "$LOG"
  fi
fi

exit 0
