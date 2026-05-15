-- ─────────────────────────────────────────────────────────────────────────────
-- LEADER KEY
-- The "leader" is a prefix key for custom shortcuts. By default it's "\".
-- Setting it to space makes shortcuts more comfortable to type.
-- This MUST be set before lazy.nvim loads, otherwise keymaps won't work.
-- ─────────────────────────────────────────────────────────────────────────────
vim.g.mapleader = " "

-- ─────────────────────────────────────────────────────────────────────────────
-- EDITOR SETTINGS
-- Basic visual improvements — line numbers and current line highlight.
-- ─────────────────────────────────────────────────────────────────────────────
vim.opt.number         = true   -- show absolute line numbers
vim.opt.cursorline     = true   -- highlight the line the cursor is on
vim.opt.shiftwidth     = 2      -- indent size when using >> or 
vim.opt.tabstop        = 2      -- how wide a tab character appears
vim.opt.expandtab      = true   -- insert spaces instead of tab characters
vim.opt.splitright     = true   -- open vertical splits to the right

-- Force a visible cursorline — the default Neovim theme makes it nearly invisible
vim.api.nvim_set_hl(0, "CursorLine", { bg = "#3c3836", ctermbg = 236 })

-- ─────────────────────────────────────────────────────────────────────────────
-- RUBY PATH FIX
-- Tell Neovim to use rbenv's Ruby instead of the old macOS system Ruby (2.6).
-- This must be set early so Mason sees the correct Ruby when installing servers.
-- ─────────────────────────────────────────────────────────────────────────────
vim.env.PATH = vim.fn.expand("~/.rbenv/shims:") .. vim.env.PATH

-- ─────────────────────────────────────────────────────────────────────────────
-- LAZY.NVIM BOOTSTRAP
-- lazy.nvim is a plugin manager — it downloads and manages Neovim plugins.
-- This block checks if lazy.nvim is already installed. If not, it clones it
-- from GitHub into Neovim's data directory (~/.local/share/nvim/lazy/).
-- This only runs once on first launch.
-- ─────────────────────────────────────────────────────────────────────────────
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath,
  })
end
-- Prepend lazy.nvim to the runtime path so Neovim can find it
vim.opt.rtp:prepend(lazypath)

-- ─────────────────────────────────────────────────────────────────────────────
-- PLUGINS
-- This is where you declare all the plugins you want lazy.nvim to install.
-- On first launch (or after :Lazy sync), lazy.nvim downloads them all.
-- Each entry is a GitHub repo in the format "author/repo-name".
-- ─────────────────────────────────────────────────────────────────────────────
require("lazy").setup({

  -- Telescope: fuzzy finder for files, text search, buffers, and more.
  -- Think of it as a powerful search UI that sits on top of your project.
  -- Required: `brew install ripgrep`
  {
    "nvim-telescope/telescope.nvim",
    tag = "0.1.8",
    dependencies = {
      "nvim-lua/plenary.nvim",                       -- utility library required by telescope
      "nvim-tree/nvim-web-devicons",                 -- adds file-type icons in the picker UI
      {
        "nvim-telescope/telescope-fzf-native.nvim",  -- C extension for faster fuzzy sorting
        build = "make",                              -- compiled on install with `make`
      },
    },
  },

  -- nvim-lspconfig: connects Neovim to Language Server Protocol (LSP) servers.
  -- LSP servers provide IDE features: go-to-definition, hover docs, rename, etc.
  -- mason.nvim makes it easy to install LSP servers without leaving Neovim.
  -- mason-lspconfig bridges mason and lspconfig so servers auto-configure.
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "williamboman/mason.nvim",           -- LSP server installer UI (open with :Mason)
      "williamboman/mason-lspconfig.nvim", -- auto-configures servers installed via mason
    },
  },

  -- nvim-cmp: autocompletion engine.
  -- Shows a popup of suggestions as you type, pulling from multiple sources:
  -- your LSP server, snippets, words in the current buffer, and file paths.
  {
    "hrsh7th/nvim-cmp",
    dependencies = {
      "hrsh7th/cmp-nvim-lsp",     -- suggestions from your LSP server
      "hrsh7th/cmp-buffer",       -- suggestions from words in the current buffer
      "hrsh7th/cmp-path",         -- suggestions for file system paths
      "L3MON4D3/LuaSnip",         -- snippet engine (required by cmp)
      "saadparwaiz1/cmp_luasnip", -- connects LuaSnip snippets into cmp
    },
  },

  -- harpoon: bookmark up to 4 files and switch between them instantly.
  -- Great when you're jumping between a controller, model, and test file.
  -- Space+h → open harpoon menu, Space+a → add current file to harpoon
  {
    "ThePrimeagen/harpoon",
    branch = "harpoon2",
    dependencies = { "nvim-lua/plenary.nvim" },
  },

  -- flash.nvim: jump anywhere on screen in 2-3 keystrokes.
  -- Press `s` in Normal mode, type a character, then pick the label shown.
  { "folke/flash.nvim" },

  -- nvim-autopairs: automatically closes (, [, {, " as you type.
  -- Zero configuration needed — just install and it works.
  {
    "windwp/nvim-autopairs",
    event = "InsertEnter",  -- only loads when you enter Insert mode (faster startup)
  },

  -- lualine.nvim: a polished status bar at the bottom of the screen.
  -- Shows current mode, filename, git branch, LSP errors, and more.
  {
    "nvim-lualine/lualine.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
  },

  -- gitsigns.nvim: shows git diff indicators in the gutter (the left margin).
  -- Lines added show as │, changed as ~, deleted as _
  -- Also lets you stage/unstage individual hunks without leaving Neovim.
  { "lewis6991/gitsigns.nvim" },
})

-- ─────────────────────────────────────────────────────────────────────────────
-- TELESCOPE CONFIGURATION
-- Set up Telescope's behavior and load optional extensions.
-- ─────────────────────────────────────────────────────────────────────────────
local telescope = require("telescope")
local builtin   = require("telescope.builtin")  -- built-in pickers (find_files, grep, etc.)

telescope.setup({
  defaults = {
    -- These folders will never appear in Telescope search results
    file_ignore_patterns = { "node_modules", ".git/" },
  },
})

-- Load the fzf extension for faster sorting (pcall means: try it, don't crash if missing)
pcall(telescope.load_extension, "fzf")

-- ─────────────────────────────────────────────────────────────────────────────
-- TELESCOPE KEYMAPS
-- All keymaps are set to "n" (Normal) mode — press Esc first if you're typing.
-- Usage: press Space, then the two-letter shortcut. E.g. Space → f → f
-- ─────────────────────────────────────────────────────────────────────────────
vim.keymap.set("n", "<leader>ff", builtin.find_files, { desc = "Find files" })   -- search files by name
vim.keymap.set("n", "<leader>fg", builtin.live_grep,  { desc = "Live grep" })    -- search text inside files
vim.keymap.set("n", "<leader>fb", builtin.buffers,    { desc = "Find buffers" }) -- switch between open files
vim.keymap.set("n", "<leader>fr", builtin.oldfiles,   { desc = "Recent files" }) -- recently opened files
vim.keymap.set("n", "<leader>fh", builtin.help_tags,  { desc = "Help tags" })    -- search Neovim's help docs

-- ─────────────────────────────────────────────────────────────────────────────
-- MASON SETUP
-- Initializes mason.nvim, the LSP server installer.
-- After this runs you can open :Mason to browse and install language servers.
-- ─────────────────────────────────────────────────────────────────────────────
require("mason").setup()

-- ─────────────────────────────────────────────────────────────────────────────
-- MASON-LSPCONFIG SETUP
-- Tells mason which LSP servers to install automatically, and wires them up
-- to Neovim's built-in LSP client via the handlers function.
--
-- To add a new language:
--   1. Add its server name to ensure_installed
--   2. Restart Neovim — Mason will install it automatically
--   3. No other changes needed; the default handler covers all servers
--
-- Find server names at: https://github.com/williamboman/mason-lspconfig.nvim
-- ─────────────────────────────────────────────────────────────────────────────
require("mason-lspconfig").setup({
  ensure_installed = {
    "lua_ls",    -- Lua  (for editing init.lua itself)
    "pyright",   -- Python
    "ts_ls",     -- TypeScript and JavaScript
    "ruby_lsp",  -- Ruby  (also run: gem install ruby-lsp)
  },
  automatic_installation = true, -- auto-install if a server is missing

  handlers = {
    -- Default handler: runs for every server in ensure_installed.
    -- vim.lsp.config() configures the server, vim.lsp.enable() activates it.
    function(server_name)
      vim.lsp.config(server_name, {})
      vim.lsp.enable(server_name)
    end,
  },
})

-- ─────────────────────────────────────────────────────────────────────────────
-- LSP KEYMAPS
-- These keymaps are only active inside a buffer where an LSP server is running.
-- The LspAttach autocmd fires automatically whenever an LSP connects.
--
-- Useful shortcuts once LSP is active:
--   gd        → jump to where a function/variable is defined
--   K         → show documentation for what's under the cursor
--   gi        → jump to the implementation
--   gr        → show all references to the symbol under the cursor
--   Space+rn  → rename a symbol across the whole project
--   Space+ca  → show code actions (fixes, imports, refactors)
-- ─────────────────────────────────────────────────────────────────────────────
vim.api.nvim_create_autocmd("LspAttach", {
  callback = function(args)
    local opts = { buffer = args.buf }  -- keymaps only apply to this buffer
    vim.keymap.set("n", "gd",         vim.lsp.buf.definition,     opts)
    vim.keymap.set("n", "K",          vim.lsp.buf.hover,          opts)
    vim.keymap.set("n", "gi",         vim.lsp.buf.implementation, opts)
    vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename,         opts)
    vim.keymap.set("n", "<leader>ca", vim.lsp.buf.code_action,    opts)
    vim.keymap.set("n", "gr",         vim.lsp.buf.references,     opts)
  end,
})

-- ─────────────────────────────────────────────────────────────────────────────
-- AUTOCOMPLETION (nvim-cmp)
-- Shows a popup menu of suggestions as you type.
-- Sources are checked in priority order: LSP → snippets → buffer words → paths.
--
-- How to use:
--   (just type)   → popup appears automatically
--   Tab           → cycle forward through suggestions
--   Shift-Tab     → cycle backward through suggestions
--   Enter         → confirm and insert the selected suggestion
--   Ctrl-Space    → manually trigger the popup if it didn't appear
--   Ctrl-e        → dismiss the popup without inserting anything
-- ─────────────────────────────────────────────────────────────────────────────
local cmp     = require("cmp")
local luasnip = require("luasnip")

cmp.setup({
  snippet = {
    -- LuaSnip is used to expand snippets when you confirm a snippet suggestion
    expand = function(args)
      luasnip.lsp_expand(args.body)
    end,
  },

  mapping = cmp.mapping.preset.insert({
    ["<C-Space>"] = cmp.mapping.complete(),        -- manually trigger completion popup
    ["<C-e>"]     = cmp.mapping.abort(),           -- close the popup without inserting
    ["<CR>"]      = cmp.mapping.confirm({          -- Enter confirms the selected suggestion
                      select = true,               -- auto-selects first item if none highlighted
                    }),

    -- Tab: move to next suggestion, or jump to next snippet placeholder
    ["<Tab>"]     = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_next_item()
      elseif luasnip.expand_or_jumpable() then
        luasnip.expand_or_jump()
      else
        fallback()                                 -- behave like a normal Tab if popup is closed
      end
    end, { "i", "s" }),                            -- active in insert mode and select mode

    -- Shift-Tab: move to previous suggestion, or jump back in snippet
    ["<S-Tab>"]   = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_prev_item()
      elseif luasnip.jumpable(-1) then
        luasnip.jump(-1)
      else
        fallback()
      end
    end, { "i", "s" }),
  }),

  -- Where suggestions come from, in priority order.
  -- The first group (LSP + snippets) is preferred over the second (buffer + paths).
  sources = cmp.config.sources({
    { name = "nvim_lsp" },  -- function signatures, types, methods from your LSP server
    { name = "luasnip" },   -- snippet completions
  }, {
    { name = "buffer" },    -- words already present in the current file (fallback)
    { name = "path" },      -- file system path completions (e.g. "./src/...")
  }),
})

-- ─────────────────────────────────────────────────────────────────────────────
-- HARPOON
-- Bookmark files you're actively working on and jump to them instantly.
-- Think of it as a persistent, manual "recent files" list of 1-4 files.
--
-- Keymaps:
--   Space+a      → add current file to harpoon list
--   Space+h      → open the harpoon menu (edit the list)
--   Space+1..4   → jump directly to harpoon file 1, 2, 3, or 4
-- ─────────────────────────────────────────────────────────────────────────────
local harpoon = require("harpoon")
harpoon:setup()

vim.keymap.set("n", "<leader>a", function() harpoon:list():add() end,          { desc = "Harpoon: add file" })
vim.keymap.set("n", "<leader>h", function() harpoon.ui:toggle_quick_menu(harpoon:list()) end, { desc = "Harpoon: menu" })
vim.keymap.set("n", "<leader>1", function() harpoon:list():select(1) end,      { desc = "Harpoon: file 1" })
vim.keymap.set("n", "<leader>2", function() harpoon:list():select(2) end,      { desc = "Harpoon: file 2" })
vim.keymap.set("n", "<leader>3", function() harpoon:list():select(3) end,      { desc = "Harpoon: file 3" })
vim.keymap.set("n", "<leader>4", function() harpoon:list():select(4) end,      { desc = "Harpoon: file 4" })

-- ─────────────────────────────────────────────────────────────────────────────
-- FLASH.NVIM
-- Jump anywhere visible on screen in 2-3 keystrokes.
-- Press `s` in Normal mode, type 1-2 characters of your target,
-- then press the label letter that appears next to it.
--
-- Keymaps:
--   s        → start a flash jump (Normal mode)
--   S        → flash treesitter (select a syntax node)
-- ─────────────────────────────────────────────────────────────────────────────
require("flash").setup()

vim.keymap.set("n", "s", function() require("flash").jump() end,            { desc = "Flash: jump" })
vim.keymap.set("n", "S", function() require("flash").treesitter() end,      { desc = "Flash: treesitter" })

-- ─────────────────────────────────────────────────────────────────────────────
-- AUTOPAIRS
-- Automatically inserts closing brackets, quotes, etc. as you type.
-- Examples: typing ( inserts (), typing " inserts "", etc.
-- Works together with nvim-cmp so completions don't break the pairs.
-- ─────────────────────────────────────────────────────────────────────────────
local autopairs = require("nvim-autopairs")
autopairs.setup()

-- Make autopairs and cmp work together: when you confirm a completion,
-- autopairs automatically adds the closing bracket if needed.
local cmp_autopairs = require("nvim-autopairs.completion.cmp")
cmp.event:on("confirm_done", cmp_autopairs.on_confirm_done())

-- ─────────────────────────────────────────────────────────────────────────────
-- LUALINE
-- A polished status bar at the bottom of the screen showing:
-- current mode, filename, git branch, LSP diagnostics, file type, cursor position.
-- ─────────────────────────────────────────────────────────────────────────────
require("lualine").setup({
  options = {
    theme = "auto",               -- matches your current colorscheme automatically
    globalstatus = true,          -- single status bar across all splits
  },
  sections = {
    lualine_a = { "mode" },       -- current mode (NORMAL, INSERT, VISUAL, etc.)
    lualine_b = { "branch", "diff", "diagnostics" }, -- git branch + LSP errors
    lualine_c = { "filename" },   -- current filename
    lualine_x = { "filetype" },   -- file type (python, lua, ruby, etc.)
    lualine_y = { "progress" },   -- % through the file
    lualine_z = { "location" },   -- line:column
  },
})

-- ─────────────────────────────────────────────────────────────────────────────
-- GITSIGNS
-- Shows git diff indicators in the left gutter as you edit:
--   │  green  → new line added
--   ~  yellow → line changed
--   _  red    → line(s) deleted below
--
-- Keymaps:
--   ]c          → jump to next changed hunk
--   [c          → jump to previous changed hunk
--   Space+gs    → stage the hunk under the cursor
--   Space+gr    → reset (undo) the hunk under the cursor
--   Space+gp    → preview the hunk in a floating window
--   Space+gb    → show git blame for the current line
-- ─────────────────────────────────────────────────────────────────────────────
require("gitsigns").setup({
  on_attach = function(bufnr)
    local gs   = package.loaded.gitsigns
    local opts = { buffer = bufnr }

    vim.keymap.set("n", "]c",         gs.next_hunk,                    { buffer = bufnr, desc = "Next hunk" })
    vim.keymap.set("n", "[c",         gs.prev_hunk,                    { buffer = bufnr, desc = "Prev hunk" })
    vim.keymap.set("n", "<leader>gs", gs.stage_hunk,                   { buffer = bufnr, desc = "Stage hunk" })
    vim.keymap.set("n", "<leader>gr", gs.reset_hunk,                   { buffer = bufnr, desc = "Reset hunk" })
    vim.keymap.set("n", "<leader>gp", gs.preview_hunk,                 { buffer = bufnr, desc = "Preview hunk" })
    vim.keymap.set("n", "<leader>gb", function() gs.blame_line({ full = true }) end, { buffer = bufnr, desc = "Blame line" })
  end,
})

-- Mapping <space> as leader key to launching terminal in vertical split, to the right
vim.keymap.set("n", "<leader>t", ":vs | terminal<CR>")
--
-- Setting the default split to the right
vim.opt.splitright = true

-- Use option (meta key) on Mac h/l/j/k as navigation arrows to resize the new window 
vim.keymap.set("n", "<M-h>", ":vertical resize -3<CR>")
vim.keymap.set("n", "<M-l>", ":vertical resize +3<CR>")
vim.keymap.set("n", "<M-k>", ":resize +2<CR>")
vim.keymap.set("n", "<M-j>", ":resize -2<CR>")
vim.keymap.set("n", "<M-Right>", ":vertical resize +3<CR>")
vim.keymap.set("n", "<M-Up>", ":resize +2<CR>")
vim.keymap.set("n", "<M-Down>", ":resize -2<CR>")
