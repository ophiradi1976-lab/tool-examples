# watchexec — File Watcher and Command Runner

Like `entr` but with more features: recursive watching, filtering by extension,
debouncing, ignore patterns, and shell integration.

## Basic usage

```bash
watchexec pytest                          # re-run pytest on any file change
watchexec -e py pytest                    # only watch .py files
watchexec -e py,html,css pytest           # watch multiple extensions
watchexec -w src/ pytest                  # watch a specific directory
```

## Key flags

| Flag | Meaning |
|------|---------|
| `-e ext`      | Watch only files with this extension |
| `-w path`     | Watch a specific path (default: current dir) |
| `-r`          | Restart long-running process on change |
| `-c`          | Clear terminal before each run |
| `--no-vcs-ignore` | Don't respect .gitignore |
| `--ignore pattern` | Ignore additional paths/patterns |
| `--debounce ms`    | Wait N ms after last change before running |
| `-s signal`   | Signal to send to process before restart (default: SIGTERM) |

## Patterns

```bash
# Watch Python files and restart a server
watchexec -r -e py -- python app.py

# Watch src/ and run build on change, clearing screen
watchexec -c -w src/ make build

# Run tests only on .go files, ignoring vendor/
watchexec -e go --ignore vendor/ go test ./...

# Watch for changes and run linter + tests
watchexec -e ts -- sh -c 'eslint . && jest'

# Restart a Node process, sending SIGKILL instead of SIGTERM
watchexec -r -s SIGKILL -e js node server.js

# Debounce: wait 500ms of inactivity before running
watchexec --debounce 500 -e py pytest
```

## vs entr

| Feature | entr | watchexec |
|---------|------|-----------|
| Recursive watch | via `find` | built-in |
| Extension filter | manual | `-e` flag |
| .gitignore aware | no | yes |
| Debouncing | no | yes |
| Restart process | `-r` | `-r` |
| File list input | stdin | no (uses dirs) |

## Use-cases

- Development servers that need restarting: `watchexec -r -e py python app.py`
- Continuous test running during development
- Auto-rebuild on save without a framework watcher
- Watching generated files and triggering downstream processing
