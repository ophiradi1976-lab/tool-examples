# Development Environment Playbook

Ansible playbook to install and configure the tools in this repo on a Mac.

---

## Installing Ansible

### Option 1 — Homebrew (recommended)

```bash
brew install ansible
```

### Option 2 — pip

```bash
pip3 install ansible
```

Verify the installation:

```bash
ansible --version
```

---

## What the playbook installs

| Tool | Purpose |
|------|---------|
| **git** | Version control |
| **gh** | GitHub CLI — PRs, issues, auth |
| **neovim** | Terminal editor |
| **ripgrep** | Fast text search; required by Telescope inside Neovim |
| **rbenv + ruby-build** | Ruby version manager |
| **Ruby 3.3.0** | Installed via rbenv, set as global default |
| **ruby-lsp** | Ruby language server for LSP/autocomplete in Neovim |
| **node** | Node.js 18+ runtime; required by Claude Code |
| **Claude Code** *(home only)* | Anthropic's CLI for Claude (`@anthropic-ai/claude-code`) |
| **GitHub Copilot CLI** | AI shell assistant (`copilot-cli`) |
| **plantuml** | Diagram generation from `.puml` files |
| **graphviz** | Graph layout engine; required by PlantUML |

### Config files and scripts installed

| Source (in this repo) | Destination |
|-----------------------|-------------|
| `development/vim/init.lua` | `~/.config/nvim/init.lua` |
| `utils/work_log/notes.py` | `~/bin/notes` |
| `utils/tracker/tracker.py` | `~/bin/tracker` |

### Shell changes added to `~/.zshrc`

- rbenv initialisation and shims on `PATH`
- Homebrew Ruby on `PATH`
- `~/bin` on `PATH`
- `$EDITOR=nvim`

---

## Running the playbook

Tasks are tagged by environment:

| Tag | What runs |
|-----|-----------|
| `common` | Everything except Claude Code — safe to run on any machine |
| `home` | Claude Code only |

```bash
cd ansible

# All environments — skips Claude Code
ansible-playbook -i inventory.yml playbook.yml --tags common

# Home environment — runs everything (common + Claude Code)
ansible-playbook -i inventory.yml playbook.yml

# Dry run — shows what would change without touching anything
ansible-playbook -i inventory.yml playbook.yml --check
```

If Ansible prompts for your password (for `sudo`), add `-K`:

```bash
ansible-playbook -i inventory.yml playbook.yml -K
```

---

## Post-install steps

These require interactive authentication and cannot be automated.

**1. Reload your shell**
```bash
source ~/.zshrc
```

**2. Install Neovim plugins**

Open Neovim — lazy.nvim bootstraps itself on first launch and installs all plugins automatically:
```bash
nvim
```

Then install the LSP servers inside Neovim:
```
:MasonInstall pyright ts_ls ruby_lsp lua_ls
```

**3. Authenticate GitHub CLI**
```bash
gh auth login
```

**4. Authenticate GitHub Copilot**
```bash
copilot auth login
# or, if using the gh extension:
gh extension install github/gh-copilot
gh copilot auth
```

**5. Authenticate Claude Code**
```bash
claude
```
Claude Code walks you through authentication on first launch.

---

## Re-running safely

The playbook is idempotent — running it again skips anything already installed and only applies changes that are missing or out of date. If `init.lua` already exists, the old version is backed up before being overwritten.
