# just — Command Runner

A `make` replacement for project-specific commands. Simpler syntax, no
dependency tracking, no implicit rules — just named recipes.

## Basic usage

```bash
just              # list available recipes
just build        # run the 'build' recipe
just test foo     # run 'test' recipe with argument
just --list       # show all recipes with descriptions
```

## justfile format

Create a file named `justfile` (or `Justfile`) in your project root:

```just
# Build the project
build:
    cargo build --release

# Run tests
test filter="":
    pytest {{ filter }} -v

# Start dev server
serve port="8080":
    uvicorn app:main --reload --port {{ port }}

# Clean build artifacts
clean:
    rm -rf dist/ __pycache__/ .pytest_cache/

# Run lint + test together
ci: lint test

lint:
    ruff check .
    mypy src/
```

## Variables and env

```just
export DATABASE_URL := "postgres://localhost/dev"

db-migrate:
    python manage.py migrate
```

## Conditionals and shell

```just
deploy env="staging":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ "{{ env }}" = "production" ]; then
        echo "Deploying to production!"
    fi
    ./deploy.sh {{ env }}
```

## Use-cases

- Standardizing project commands across a team (`just test`, `just deploy`)
- Replacing npm scripts or Makefile boilerplate
- Documenting common workflows in one file
- Parameterized commands without shell function overhead

```bash
# Common project workflow
just build
just test "tests/unit"
just serve 3000
```

## Tips

- `just --dry-run` shows what would be executed without running it
- `just --list` shows all recipes — works as built-in docs
- Multiple justfiles can be loaded with `--justfile path/to/justfile`
