# git-delta — Better Git Diffs

A syntax-highlighted, side-by-side capable diff pager for Git. Configured by
the playbook as the global Git pager.

## How it works

delta is a pager — you don't invoke it directly. It automatically enhances
output from `git diff`, `git log -p`, `git show`, and `git blame`.

```bash
git diff                # automatically uses delta
git show HEAD           # delta-rendered
git log -p              # delta-rendered
```

## Config set by playbook

```ini
[core]
    pager = delta

[interactive]
    diffFilter = delta --color-only

[delta]
    navigate = true       # n/N to jump between diff sections

[merge]
    conflictstyle = zdiff3  # shows base + both sides in conflicts
```

## Navigation (enabled)

When viewing diffs:
- `n` — next file / diff section
- `N` — previous file / diff section
- `q` — quit pager

## Useful delta flags (can be added to ~/.gitconfig)

```ini
[delta]
    navigate = true
    side-by-side = true      # two-column diff layout
    line-numbers = true
    syntax-theme = Dracula   # or: Nord, GitHub, OneHalfDark
    diff-so-fancy = false    # alternative: use diff-so-fancy style
```

Or temporarily on the command line:

```bash
git diff | delta --side-by-side
git diff | delta --syntax-theme=GitHub
```

## Conflict markers with zdiff3

With `merge.conflictstyle = zdiff3`, conflict blocks show three sections:

```
<<<<<<< HEAD
your version
||||||| base
the original
=======
their version
>>>>>>> feature-branch
```

The middle `|||||||` section (the common ancestor) makes it much easier to
understand what both sides changed.

## Use-cases

- Reviewing PRs locally with readable, colored diffs
- Understanding merge conflicts (zdiff3 shows the base)
- Side-by-side diffs for large refactors (`side-by-side = true`)
