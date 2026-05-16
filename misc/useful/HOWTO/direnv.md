# direnv — Automatic Environment Variables

Automatically loads and unloads environment variables when you `cd` into (or
out of) a directory. Hook added to `~/.zshrc` by the playbook.

## How it works

1. Create a `.envrc` file in a project directory
2. Run `direnv allow` once to trust it
3. Every time you `cd` into that directory, the env is loaded automatically
4. When you `cd` out, it's unloaded

## Basic .envrc examples

```bash
# Set env vars
export DATABASE_URL="postgres://localhost/mydb"
export API_KEY="dev-key-abc123"
export ENVIRONMENT="development"

# Add a local bin to PATH
export PATH="$PWD/bin:$PATH"

# Load a .env file (common pattern)
dotenv
# or dotenv_if_exists .env.local
```

## Commands

```bash
direnv allow          # trust and load the .envrc in current dir
direnv deny           # revoke trust
direnv edit           # open .envrc in $EDITOR, then auto-allow
direnv status         # show current status
direnv reload         # force reload current .envrc
```

## Use-cases

### Python virtualenv per project

```bash
# .envrc
layout python3
# → creates/activates a .venv automatically
```

### Node version via .nvmrc

```bash
# .envrc
use node 20
```

### AWS profile switching

```bash
# .envrc
export AWS_PROFILE=staging
export AWS_REGION=us-east-1
```

### Different DB per project

```bash
# project-a/.envrc
export DATABASE_URL="postgres://localhost/project_a"

# project-b/.envrc
export DATABASE_URL="postgres://localhost/project_b"
```

## Tips

- Never commit `.envrc` files containing secrets — add to `.gitignore`
- Use `.envrc` for non-secret config; use a secrets manager for credentials
- `direnv edit` is safer than editing manually — it auto-re-allows after save
- Inherits from parent dirs, so you can have a root `.envrc` + project-level ones
