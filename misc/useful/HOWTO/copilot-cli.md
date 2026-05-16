# copilot-cli — GitHub Copilot in the Terminal

AI-powered shell command suggestions from GitHub Copilot. Explains commands,
suggests shell one-liners, and helps with git operations — all from the CLI.

## Setup

```bash
# Authenticate (one-time)
gh auth login
gh extension install github/gh-copilot

# Or if installed standalone:
copilot auth login
```

## Main commands

```bash
gh copilot suggest "..."        # suggest a shell command
gh copilot explain "..."        # explain a command
```

## Suggest

```bash
# Describe what you want in plain English
gh copilot suggest "find all files modified in the last 7 days"
gh copilot suggest "compress a directory excluding node_modules"
gh copilot suggest "kill the process running on port 3000"
gh copilot suggest "list all docker containers using more than 500MB"
gh copilot suggest "undo last git commit but keep changes staged"
```

The CLI asks you to pick a command type:
- **generic shell** — any bash/zsh command
- **git** — git-specific operations
- **gh** — GitHub CLI operations

Then it suggests a command and asks if you want to run it, copy it, or revise.

## Explain

```bash
# Understand what a command does before running it
gh copilot explain "awk '{print $2}' file | sort | uniq -c | sort -rn"
gh copilot explain "git rebase -i HEAD~3"
gh copilot explain "find . -name '*.log' -mtime +7 -delete"
gh copilot explain "lsof -i :8080"
```

## Shell aliases (optional, add to ~/.zshrc)

```bash
alias '??'='gh copilot suggest -t shell'
alias 'git?'='gh copilot suggest -t git'
alias 'gh?'='gh copilot suggest -t gh'
```

Then:
```bash
?? "recursively find large files over 100MB"
git? "combine my last 3 commits into one"
```

## Use-cases

- Forgetting the exact syntax for `find`, `awk`, `sed`, `tar` etc.
- Generating git commands for complex operations (rebase, cherry-pick, bisect)
- Explaining unfamiliar commands from docs or Stack Overflow before running
- Quickly generating one-liners without switching to a browser
