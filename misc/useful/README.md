# macOS CLI Tools Setup with Ansible

This setup installs useful command-line tools on a local Mac using Homebrew and Ansible.

Tools installed:

- `fzf`
- `bat`
- `eza`
- `tree`
- `lazygit`
- `tig`
- `git-delta`
- `jq`
- `just`
- `direnv`
- `entr`
- `watchexec`
- `hyperfine`
- `tldr`
- `asciinema`
- `pv`
- `lazydocker`

## Prerequisites

### 1. Install Homebrew

If Homebrew is not already installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installing Homebrew, follow any instructions it prints for adding `brew` to your shell path.

### 2. Install Ansible

```bash
brew install ansible
```

Verify:

```bash
ansible --version
```

## Files

```text
README.md
install-cli-tools.yml
```

## Run the Ansible playbook

From the directory containing `install-cli-tools.yml`:

```bash
ansible-playbook install-cli-tools.yml
```

Because the playbook runs only on your local Mac, no inventory file is required.

## What the playbook does

The playbook:

1. Installs the CLI tools with Homebrew.
2. Runs the `fzf` install script for shell integration.
3. Adds useful aliases to `~/.zshrc`.
4. Enables `direnv` integration for zsh.
5. Configures Git to use `delta` for better diffs.
6. Updates the `tldr` cache.

## Post-install setup details

### fzf

The playbook runs:

```bash
$(brew --prefix)/opt/fzf/install --all --no-bash --no-fish
```

This enables zsh key bindings and fuzzy completion.

Common shortcuts:

```text
Ctrl-R  fuzzy search shell history
Ctrl-T  fuzzy find files
```

### bat

The playbook adds:

```bash
alias cat="bat"
```

Usage:

```bash
bat README.md
```

### eza

The playbook adds:

```bash
alias ls="eza"
alias ll="eza -lah --git"
alias lt="eza --tree"
```

Usage:

```bash
ll
lt
```

### direnv

The playbook adds:

```bash
eval "$(direnv hook zsh)"
```

Example usage:

```bash
echo 'export FOO=bar' > .envrc
direnv allow
```

### delta

The playbook configures Git with:

```bash
git config --global core.pager delta
git config --global interactive.diffFilter "delta --color-only"
git config --global delta.navigate true
git config --global merge.conflictstyle zdiff3
```

Now Git diffs should be easier to read:

```bash
git diff
```

### tldr

The playbook runs:

```bash
tldr --update
```

Usage:

```bash
tldr tar
tldr jq
tldr git
```

### lazygit

Run:

```bash
lazygit
```

### lazydocker

Run:

```bash
lazydocker
```

### pv

`pv` shows progress through pipes.

Example:

```bash
cat large-file.sql | pv | mysql my_database
```

### hyperfine

Benchmark shell commands:

```bash
hyperfine 'grep foo large-file.txt' 'rg foo large-file.txt'
```

### watchexec

Run a command whenever files change:

```bash
watchexec -e rb 'ruby test.rb'
```

### entr

Another lightweight file watcher:

```bash
ls *.rb | entr ruby test.rb
```

## Reload your shell

After running the playbook:

```bash
source ~/.zshrc
```

Or close and reopen your terminal.

## Verify installation

```bash
fzf --version
bat --version
eza --version
tree --version
lazygit --version
tig --version
delta --version
jq --version
just --version
direnv --version
entr -v
watchexec --version
hyperfine --version
tldr --version
asciinema --version
pv --version
lazydocker --version
```
