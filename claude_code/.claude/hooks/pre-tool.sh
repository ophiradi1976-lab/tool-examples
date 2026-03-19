#!/usr/bin/env bash
# .claude/hooks/pre-tool.sh
#
# PreToolUse hook — fires BEFORE every Bash tool call.
# Claude Code pipes JSON to stdin. Exit 2 to BLOCK the command
# and send the error message back to Claude as context.

LOG="$CLAUDE_PROJECT_DIR/logs/claude-activity.log"
mkdir -p "$(dirname "$LOG")"

# Parse the bash command out of the JSON stdin payload
INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c \
  "import sys, json; print(json.load(sys.stdin)['tool_input']['command'])" 2>/dev/null)

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log every Bash command Claude is about to run
echo "[$TIMESTAMP] PRE-TOOL  | Bash | $CMD" >> "$LOG"

# --- Safety rule: block rm -rf ---
if echo "$CMD" | grep -qE 'rm\s+-rf'; then
  MSG="BLOCKED: rm -rf is not allowed. Use rm -i instead."
  echo "[$TIMESTAMP] $MSG" >> "$LOG"
  echo "$MSG" >&2
  exit 2   # exit 2 = block + feed error back to Claude
fi

# --- Safety rule: block commits of .env files ---
if echo "$CMD" | grep -qE 'git add.*\.env'; then
  MSG="BLOCKED: Do not stage .env files."
  echo "[$TIMESTAMP] $MSG" >> "$LOG"
  echo "$MSG" >&2
  exit 2
fi

# All clear — allow the command
exit 0
