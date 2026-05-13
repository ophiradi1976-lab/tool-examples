# Neovim plugins guide

This document covers every plugin in your `init.lua` — what it does, how to use it, and all keymaps.

---

## Table of contents

1. [Telescope — fuzzy finder](#1-telescope--fuzzy-finder)
2. [LSP — language intelligence](#2-lsp--language-intelligence)
3. [nvim-cmp — autocompletion](#3-nvim-cmp--autocompletion)
4. [Harpoon — file bookmarks](#4-harpoon--file-bookmarks)
5. [Flash — screen navigation](#5-flash--screen-navigation)
6. [Autopairs — bracket completion](#6-autopairs--bracket-completion)
7. [Commenting — built-in](#7-commenting--built-in-neovim-010)
8. [Lualine — status bar](#8-lualine--status-bar)
9. [Gitsigns — git integration](#9-gitsigns--git-integration)

---

## General

Your leader key is `Space`. Keymaps written as `Space ff` mean: press Space, then `f`, then `f` — in sequence, not simultaneously.

You must be in **Normal mode** for most keymaps to work. Press `Esc` if you are unsure.

---

## 1. Telescope — fuzzy finder

Telescope is a search UI for your project. It lets you find files, search text, switch buffers, and more — all from a single popup window.

### Opening Telescope

| Keymap | Action |
|--------|--------|
| `Space ff` | Find files by name |
| `Space fg` | Search text inside files (requires `ripgrep`: `brew install ripgrep`) |
| `Space fb` | Switch between open buffers |
| `Space fr` | Recently opened files |
| `Space fh` | Search Neovim's built-in help docs |

### Inside the Telescope window

| Key | Action |
|-----|--------|
| Type anything | Filter results in real time |
| `↑` / `↓` or `Ctrl-k` / `Ctrl-j` | Move through results |
| `Enter` | Open the selected file |
| `Ctrl-v` | Open in a vertical split |
| `Ctrl-x` | Open in a horizontal split |
| `Ctrl-t` | Open in a new tab |
| `Esc` | Close Telescope |

### Tips

- `Space ff` is your primary way to open any file in a project — faster than a file tree.
- `Space fg` (live grep) is the equivalent of `grep` or VSCode's "find in files". It searches file contents, not file names.
- `Space fb` is useful when you have several files open and want to switch between them without using the mouse.

---

## 2. LSP — language intelligence

LSP (Language Server Protocol) gives Neovim IDE features: go-to-definition, hover documentation, rename across files, and more.

Supported languages in your config:

| Language | Server |
|----------|--------|
| Lua | `lua_ls` |
| Python | `pyright` |
| TypeScript / JavaScript | `ts_ls` |
| Ruby | `ruby_lsp` |

### LSP keymaps

These keymaps only activate inside a file where an LSP server is running.

| Keymap | Action |
|--------|--------|
| `gd` | Jump to the definition of the symbol under the cursor |
| `K` | Show documentation / hover info for the symbol under the cursor |
| `gi` | Jump to the implementation |
| `gr` | Show all references to the symbol (opens in Telescope) |
| `Space rn` | Rename the symbol everywhere in the project |
| `Space ca` | Show code actions (auto-imports, quick fixes, refactors) |
| `Ctrl-o` | Jump back to where you were (after `gd` or `gr`) |

### Useful commands

```
:LspInfo          → show which LSP server is attached to the current file
:Mason            → open the LSP server installer UI
:MasonInstall X   → install a specific server by name
```

### Tips

- Press `K` on any function or class to see its signature and docs without leaving the file.
- `gd` followed by `Ctrl-o` is the fastest way to peek at a definition and return.
- `Space ca` on an underlined error often offers a one-keypress fix.
- `]d` / `[d` jump to the next/previous diagnostic (error or warning) in the file.

---

## 3. nvim-cmp — autocompletion

nvim-cmp shows a popup of suggestions as you type. It pulls from your LSP server, snippets, words in the current file, and file paths.

### How it works

The popup appears automatically as you type. You do not need to trigger it manually.

| Key | Action |
|-----|--------|
| `Tab` | Select the next suggestion |
| `Shift-Tab` | Select the previous suggestion |
| `Enter` | Confirm and insert the selected suggestion |
| `Ctrl-Space` | Manually trigger the popup if it did not appear |
| `Ctrl-e` | Dismiss the popup without inserting anything |

### Suggestion sources (in priority order)

1. LSP server — function signatures, types, methods
2. LuaSnip — snippet expansions
3. Buffer — words already in the current file
4. Path — file system paths (e.g. `./src/...`)

### Tips

- If the popup is covering something you want to read, press `Ctrl-e` to dismiss it temporarily.
- LSP suggestions (source 1) are the most useful — they include type information and auto-imports.
- If a suggestion expands a snippet, `Tab` will jump between the snippet's placeholders.

---

## 4. Harpoon — file bookmarks

Harpoon lets you bookmark 2–4 files you are actively working on and jump between them instantly with a single keypress. It is faster than Telescope when you are switching repeatedly between the same small set of files.

### Keymaps

| Keymap | Action |
|--------|--------|
| `Space a` | Add the current file to the harpoon list |
| `Space h` | Open the harpoon menu |
| `Space 1` | Jump to harpoon file 1 |
| `Space 2` | Jump to harpoon file 2 |
| `Space 3` | Jump to harpoon file 3 |
| `Space 4` | Jump to harpoon file 4 |

### Removing a file from the list

1. Press `Space h` to open the harpoon menu
2. Navigate to the file you want to remove
3. Press `dd` to delete the line
4. Press `:w` to save the change (required — harpoon won't persist the deletion without this)
5. Press `q` or `Esc` to close the menu

### Typical workflow

Open your controller file → `Space a`, open your model → `Space a`, open your test file → `Space a`. Now press `Space 1`, `Space 2`, `Space 3` to bounce between all three instantly.

---

## 5. Flash — screen navigation

Flash lets you jump to any visible character on screen in 2–3 keystrokes. It is faster than scrolling or using `/` search for targets that are already visible.

### Keymaps

| Keymap | Action |
|--------|--------|
| `s` | Start a flash jump |
| `S` | Flash treesitter — highlight and select a whole syntax node |
| `Esc` | Cancel the jump |

### How to use

1. Press `s` in Normal mode
2. Type 1–2 characters from your target location
3. Flash highlights every match on screen with a label letter
4. Press the label letter to jump there instantly

### Example

You see a function called `process_order` on screen. Press `s` → type `pr` → a label appears next to the match → press the label. You are there.

---

## 6. Autopairs — bracket completion

Autopairs automatically closes brackets and quotes as you type. There are no keymaps to learn — it works silently in Insert mode.

### What it does automatically

| You type | Result |
|----------|--------|
| `(` | `()` — cursor placed inside |
| `[` | `[]` — cursor placed inside |
| `{` | `{}` — cursor placed inside |
| `"` | `""` — cursor placed inside |
| `'` | `''` — cursor placed inside |
| `` ` `` | ` `` ` `` — cursor placed inside |
| `)` | Skips over the auto-inserted `)` instead of adding a duplicate |

### Tips

- If autopairs inserts a closing bracket you do not want, press `Ctrl-w` to delete the pair, or `Del` to remove just the closing half.
- Autopairs is integrated with nvim-cmp: when you confirm a completion that ends with `(`, the closing `)` is added automatically.

---

## 7. Commenting — built-in (Neovim 0.10+)

Neovim 0.10 and later has built-in commenting. The comment style is detected automatically for every language (`#` for Python/Ruby, `//` for JS/TS, `--` for Lua).

### Keymaps

| Keymap | Mode | Action |
|--------|------|--------|
| `gcc` | Normal | Toggle comment on the current line |
| `gc` + motion | Normal | Toggle comment on a range. E.g. `gc5j` comments the next 5 lines |
| `gcip` | Normal | Toggle comment on the current paragraph |
| `gc` | Visual | Toggle comment on all selected lines |

### Tips

- Press `gcc` again on a commented line to uncomment it.
- In Visual mode, select lines with `V` (line visual) then press `gc`.

---

## 8. Lualine — status bar

Lualine is a status bar at the bottom of Neovim. It is passive — no keymaps needed. It shows:

| Section | Content |
|---------|---------|
| Left | Current mode (NORMAL, INSERT, VISUAL, etc.) |
| Left | Git branch name and number of changed lines |
| Left | LSP error and warning counts |
| Center | Current filename |
| Right | File type (python, lua, ruby, etc.) |
| Right | Scroll percentage and line:column position |

### Tips

- The mode section changes color when you switch modes — a quick visual indicator that you are where you think you are.
- LSP error counts (e.g. `E2 W1`) disappear as you fix issues in the file.
- You do not need to run `:set ft?` to check the file type — lualine always shows it.

---

## 9. Gitsigns — git integration

Gitsigns shows git diff indicators in the left gutter as you edit, and lets you stage or revert individual hunks without leaving Neovim.

### Gutter symbols

| Symbol | Color | Meaning |
|--------|-------|---------|
| `│` | Green | New line added |
| `~` | Yellow | Line changed |
| `_` | Red | Line(s) deleted below this point |

### Keymaps

| Keymap | Action |
|--------|--------|
| `]c` | Jump to the next changed hunk |
| `[c` | Jump to the previous changed hunk |
| `Space gp` | Preview the hunk in a floating diff window |
| `Space gs` | Stage the hunk under the cursor (like `git add -p`) |
| `Space gr` | Reset the hunk — discard changes and revert to what git has |
| `Space gb` | Show git blame for the current line |

### Tips

- Use `]c` / `[c` to move through all changes in a file before committing.
- `Space gp` is useful for a quick diff preview without opening a full diff tool.
- `Space gs` lets you stage individual hunks, so you can commit related changes separately even within the same file.
- `Space gb` shows the commit message and author for the current line — useful for understanding why code was written a certain way.

---

## Quick reference

| Keymap | Plugin | Action |
|--------|--------|--------|
| `Space ff` | Telescope | Find files |
| `Space fg` | Telescope | Live grep |
| `Space fb` | Telescope | Find buffers |
| `Space fr` | Telescope | Recent files |
| `Space fh` | Telescope | Help tags |
| `gd` | LSP | Go to definition |
| `K` | LSP | Hover docs |
| `gi` | LSP | Go to implementation |
| `gr` | LSP | References |
| `Space rn` | LSP | Rename symbol |
| `Space ca` | LSP | Code actions |
| `Tab` | nvim-cmp | Next suggestion |
| `Enter` | nvim-cmp | Confirm suggestion |
| `Ctrl-e` | nvim-cmp | Dismiss popup |
| `Space a` | Harpoon | Add file |
| `Space h` | Harpoon | Open menu |
| `Space 1-4` | Harpoon | Jump to file |
| `s` | Flash | Jump anywhere on screen |
| `gcc` | Built-in | Toggle line comment |
| `gc` | Built-in | Toggle comment (visual) |
| `]c` / `[c` | Gitsigns | Next/prev hunk |
| `Space gs` | Gitsigns | Stage hunk |
| `Space gr` | Gitsigns | Reset hunk |
| `Space gp` | Gitsigns | Preview hunk |
| `Space gb` | Gitsigns | Blame line |
