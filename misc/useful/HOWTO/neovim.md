# neovim (nvim) — Hyperextensible Vim

A modern Vim fork with Lua config, built-in LSP client, and a rich plugin
ecosystem. Set as `$EDITOR` by the playbook.

## Launch

```bash
nvim                        # open empty buffer
nvim file.py                # open a file
nvim file1 file2            # open multiple files
nvim .                      # open file explorer (netrw or your file tree plugin)
nvim -d file1 file2         # diff mode
```

## Modes

| Mode | How to enter |
|------|-------------|
| Normal | `Esc` (default) |
| Insert | `i` (before cursor), `a` (after), `o` (new line below) |
| Visual | `v` (char), `V` (line), `Ctrl+v` (block) |
| Command | `:` |
| Search | `/` (forward), `?` (backward) |

## Essential normal mode commands

### Navigation
```
h j k l         ← ↓ ↑ →
w / b           next / prev word
e               end of word
0 / ^           start of line (hard / soft)
$               end of line
gg / G          first / last line
{N}G            go to line N
Ctrl+d / Ctrl+u  scroll half page down / up
```

### Editing
```
dd              delete line
yy              yank (copy) line
p / P           paste after / before
u               undo
Ctrl+r          redo
.               repeat last change
ciw             change inner word
di"             delete inside quotes
```

### Search and replace
```
/pattern        search forward
n / N           next / previous match
:%s/old/new/g   replace all in file
:%s/old/new/gc  replace all with confirmation
```

## Common commands

```vim
:w              save
:q              quit
:wq             save and quit
:q!             quit without saving
:e filename     open a file
:vs filename    vertical split
:sp filename    horizontal split
:term           open terminal in split
:Mason          open LSP/tool installer (if mason.nvim installed)
:Lazy           open plugin manager (if lazy.nvim installed)
```

## LSP features (configured via Mason)

```vim
gd              go to definition
gr              show references
K               hover documentation
<leader>rn      rename symbol
<leader>ca      code action
[d / ]d         previous / next diagnostic
:lua vim.diagnostic.open_float()   show diagnostic detail
```

## Config location

```bash
~/.config/nvim/init.lua      # main config (copied from repo by playbook)
~/.config/nvim/lua/          # modular Lua config files (if split)
```

## Post-install steps (from playbook)

```bash
# 1. Open nvim — lazy.nvim installs plugins automatically
nvim

# 2. Install LSP servers
:MasonInstall pyright ts_ls ruby_lsp lua_ls
```

## Tips

- `Ctrl+\` + `Ctrl+n` — exit terminal mode back to normal mode
- `:checkhealth` — diagnose plugin and LSP issues
- `:Telescope find_files` — fuzzy file finder (if Telescope installed)
- `:Telescope live_grep` — search across files with ripgrep
