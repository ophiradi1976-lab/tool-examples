# rbenv — Ruby Version Manager

Manages multiple Ruby versions per project or globally. Configured in `~/.zshrc`
by the playbook.

## Basic usage

```bash
rbenv versions              # list installed Ruby versions
rbenv version               # show current active version
rbenv install --list        # list available versions to install
rbenv install 3.3.0         # install a specific version
rbenv global 3.3.0          # set global default
rbenv local 3.2.2           # set version for current directory (creates .ruby-version)
rbenv shell 3.1.0           # set version for current shell session only
```

## How version selection works (priority order)

1. `RBENV_VERSION` env var (shell override)
2. `.ruby-version` file in current dir (or any parent dir)
3. Global version (`~/.rbenv/version`)

## Per-project Ruby version

```bash
cd my-project
rbenv local 3.2.2           # creates .ruby-version file
cat .ruby-version            # → 3.2.2
```

Commit `.ruby-version` to the repo so teammates use the same version.

## After installing a new Ruby version

```bash
rbenv install 3.3.5
rbenv global 3.3.5
rbenv rehash                # update shims after installing gems with executables
gem install bundler          # install bundler for the new version
```

## Useful commands

```bash
rbenv which ruby             # show path to active ruby binary
rbenv which gem              # show path to active gem binary
rbenv rehash                 # rebuild shims (run after gem install)
rbenv root                   # show rbenv root directory
```

## Troubleshooting

```bash
# Is rbenv on your PATH?
which rbenv

# Is the shims directory on PATH?
echo $PATH | tr ':' '\n' | grep rbenv

# Check init is in .zshrc
grep rbenv ~/.zshrc

# Full diagnostic
rbenv doctor     # (if rbenv-doctor plugin installed)
```

## .zshrc setup (added by playbook)

```bash
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init - zsh)"
```
