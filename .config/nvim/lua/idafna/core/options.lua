-- Line numbers
vim.opt.relativenumber = true
vim.opt.number = true

-- Tabs and indentation
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true
vim.opt.smartindent = true

-- Line wrapping
vim.opt.wrap = false

-- Search
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.incsearch = true
vim.opt.hlsearch = false

-- Cursor line
vim.opt.cursorline = true

-- Appearance
vim.opt.termguicolors = true
vim.opt.background = "dark"
vim.opt.signcolumn = "yes"

-- Backspace
vim.opt.backspace = "indent,eol,start"

-- Clipboard
vim.opt.clipboard = "unnamedplus"

-- Split windows
vim.opt.splitbelow = true
vim.opt.splitright = true

-- Swap files
vim.opt.swapfile = false

-- Scroll offset
vim.opt.scrolloff = 8

-- Skip backward compatibility check
vim.g.skip_ts_context_commentstring_module = true
