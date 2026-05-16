# claude (Claude Code) — AI Coding Agent in the Terminal

An agentic coding tool from Anthropic. Reads your codebase, writes and edits
files, runs commands, and helps with complex multi-step engineering tasks.
Installed via npm (`@anthropic-ai/claude-code`). Requires Node 18+.

## Launch

```bash
claude                          # start interactive session in current directory
claude "explain this codebase"  # one-shot prompt
claude -p "add error handling to src/api.py"  # non-interactive (print mode)
```

## First run

```bash
claude          # prompts you to authenticate via browser on first launch
```

## What it can do

- Read files and understand the codebase structure
- Write new files and edit existing ones
- Run shell commands (with your approval)
- Search the web (when needed)
- Debug errors iteratively
- Explain unfamiliar code

## Common use-cases

```bash
# Understand a new codebase
claude "give me an overview of this project's architecture"

# Write code
claude "add a /health endpoint to the Flask app in src/app.py"

# Fix a bug
claude "the tests in tests/test_auth.py are failing — investigate and fix"

# Refactor
claude "refactor the UserService class to use dependency injection"

# Write tests
claude "write pytest unit tests for src/utils.py"

# Review code
claude "review this PR diff for security issues"
```

## Slash commands (interactive mode)

```
/help           show available commands
/clear          clear conversation history
/compact        condense history to save context
/cost           show token usage and cost for this session
/model          switch model
/add-dir path   add another directory to context
/review         start a code review workflow
```

## Useful flags

```bash
claude --model claude-opus-4-5     # use a specific model
claude -p "..." --output-format json  # structured output
claude --no-tools                   # disable file/shell tools (chat only)
claude --allowedTools "Bash,Write"  # restrict which tools can be used
```

## Tips

- Run from the root of your project so it has full context
- Be specific in prompts — include file names, function names, error messages
- Use `--print` / `-p` for scripting and non-interactive automation
- It reads `.gitignore` and respects it when exploring files
- You approve file writes and shell commands before they execute

## Config

```bash
~/.claude/          # config and conversation history directory
```
