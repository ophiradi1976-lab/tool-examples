# entr — Run Commands on File Change

Watches a list of files and re-runs a command whenever any of them change.
Simple, fast, UNIX-style.

## Basic usage

```bash
# Re-run tests when any .py file changes
ls *.py | entr pytest

# Rebuild when source changes
ls src/**/*.go | entr go build

# Restart a server when config changes
echo config.yaml | entr -r ./start-server.sh
```

## Key flags

| Flag | Meaning |
|------|---------|
| `-r`  | Restart a long-running process (kills + restarts on change) |
| `-c`  | Clear the screen before each run |
| `-d`  | Exit when a new file is added to a watched directory |
| `-p`  | Postpone — don't run on startup, only on first change |
| `/_`  | Pass the changed filename to the command |

## Patterns

```bash
# Watch all Python files recursively (using find)
find . -name "*.py" | entr pytest -x

# Clear screen + run tests
find . -name "*.py" | entr -c pytest

# Restart a Flask server on code change
find . -name "*.py" | entr -r python app.py

# Recompile and run on any .c change
ls *.c | entr sh -c 'make && ./myapp'

# Pass changed filename to command
ls *.md | entr -p pandoc /_ -o output.html

# Watch a log file and run a parser
echo app.log | entr -p python parse_log.py
```

## Use-cases

- TDD loop: watch source files, re-run tests instantly on save
- Auto-reload a dev server without a framework's built-in watcher
- Trigger a build/lint whenever files change
- Watch a config file and reload a service

## Tip

Combine with `find` for recursive watching:

```bash
find . -name "*.ts" ! -path "*/node_modules/*" | entr -c tsc --noEmit
```
