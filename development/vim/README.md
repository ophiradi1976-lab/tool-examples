# Neovim Installation

## 1. Install Neovim and ripgrep

```sh
brew install neovim
brew install ripgrep
```

## 2. Create the config file

```sh
mkdir -p ~/.config/nvim
touch ~/.config/nvim/init.lua
## Copy the init.lua in repo to ~/.config/nvim/init.lua
```

## 3. Install rbenv and Ruby

```sh
brew install rbenv ruby-build
```

Add rbenv to your shell:

```sh
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc
```

Install and set a modern Ruby version:

```sh
rbenv install 3.3.0
rbenv global 3.3.0
ruby --version   # should say 3.3.0
```

## 4. Install ruby-lsp

```sh
brew upgrade ruby
```

Add Ruby to your PATH in `~/.zshrc`:

```sh
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
source ~/.zshrc
gem install ruby-lsp
```
