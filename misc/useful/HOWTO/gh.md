# gh — GitHub CLI

The official GitHub CLI. Manage repos, PRs, issues, workflows, and more
without leaving the terminal.

## Setup

```bash
gh auth login           # authenticate (browser or token)
gh auth status          # check current auth
```

## Repos

```bash
gh repo view                            # view current repo in terminal
gh repo view --web                      # open in browser
gh repo clone owner/repo                # clone a repo
gh repo create my-project --public      # create a new repo
gh repo fork owner/repo                 # fork a repo
gh repo list                            # list your repos
```

## Pull Requests

```bash
gh pr list                              # list open PRs
gh pr view 42                           # view PR #42
gh pr view --web                        # open current branch's PR in browser
gh pr create                            # create PR (interactive)
gh pr create -t "Title" -b "Body"      # create PR non-interactively
gh pr checkout 42                       # checkout PR #42 locally
gh pr review 42 --approve               # approve a PR
gh pr review 42 --request-changes -b "needs work"
gh pr merge 42 --squash                 # merge with squash
gh pr diff 42                           # view diff in terminal (uses delta)
gh pr status                            # PRs relevant to you
```

## Issues

```bash
gh issue list                           # list open issues
gh issue view 10                        # view issue #10
gh issue create -t "Bug" -b "Details"  # create an issue
gh issue close 10                       # close an issue
gh issue comment 10 -b "Message"        # add a comment
gh issue status                         # issues relevant to you
```

## GitHub Actions / Workflows

```bash
gh run list                             # list recent workflow runs
gh run view 123456                      # view a specific run
gh run watch                            # watch a run in real time
gh workflow list                        # list workflows
gh workflow run deploy.yml              # trigger a workflow manually
```

## Releases

```bash
gh release list
gh release view v1.2.0
gh release create v1.3.0 --notes "Changelog..."
gh release upload v1.3.0 ./dist/*.zip  # attach artifacts
```

## Gists

```bash
gh gist create script.py               # create a gist
gh gist list                            # list your gists
```

## Use-cases

- Creating PRs from the terminal immediately after `git push`
- Reviewing PRs without switching to a browser
- Triggering CI runs manually: `gh workflow run`
- Checking CI status: `gh run list --branch main`
- Quickly opening a repo or PR in browser: `gh repo view --web`
