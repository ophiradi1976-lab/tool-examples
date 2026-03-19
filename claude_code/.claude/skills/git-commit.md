---
description: "Use this skill when the user asks to commit changes, stage files, or create a git commit."
---

# Skill: git-commit

A safe, repeatable workflow for staging and committing code changes.

## Steps

1. **Assess** — run `git status` to see what has changed
2. **Review** — run `git diff` to read the actual diffs before staging anything
3. **Stage** — add only the relevant files (`git add <files>`, never `git add .` blindly)
4. **Write message** — follow Conventional Commits format: `type(scope): short description`
   - Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
   - Example: `feat(api): add /health endpoint`
5. **Commit** — run `git commit -m "<message>"`
6. **Confirm** — run `git log --oneline -3` to verify the commit landed

## Rules
- Never use `git push --force`
- Never commit `.env` files or secrets
- If you see unrelated changes, commit them separately
