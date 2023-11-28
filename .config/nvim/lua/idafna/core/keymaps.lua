-- set leader key to space
vim.g.mapleader = " "

-- General keymaps
vim.keymap.set("i", "jk", "<ESC>", { desc = "Exit insert mode with jk" })

-- Delete single character without copying it into the register
vim.keymap.set("n", "x", '"_x', { desc = "Delete single character without copying it into the register" })

-- Increment and decrement numbers
vim.keymap.set("n", "<C-a>", "<C-a>", { desc = "Increment number under cursor" })
vim.keymap.set("n", "<C-x>", "<C-x>", { desc = "Decrement number under cursor" })

-- Move selected line / block of text in visual mode
vim.keymap.set("x", "K", ":move '<-2<CR>gv-gv", { desc = "Move selected line / block of text in visual mode" })
vim.keymap.set("x", "J", ":move '>+1<CR>gv-gv", { desc = "Move selected line / block of text in visual mode" })

-- Move current line / block with Alt-j/k ala vscode.
vim.keymap.set("n", "<A-j>", ":m .+1<CR>==", { desc = "Move current line / block with Alt-j/k ala vscode." })
vim.keymap.set("n", "<A-k>", ":m .-2<CR>==", { desc = "Move current line / block with Alt-j/k ala vscode." })

-- Better indenting
vim.keymap.set("v", "<", "<gv", { desc = "Better indenting" })
vim.keymap.set("v", ">", ">gv", { desc = "Better indenting" })

-- Window management
vim.keymap.set("n", "<C-h>", "<C-w>h", { desc = "Move to window left" })
vim.keymap.set("n", "<leader>sv", ":vsplit<CR>", { desc = "Split window vertically" })
vim.keymap.set("n", "<leader>sh", ":split<CR>", { desc = "Split window horizontally" })
vim.keymap.set("n", "<leader>se", ":wincmd =<CR>", { desc = "Equalize window sizes" })
vim.keymap.set("n", "<leader>sx", ":close<CR>", { desc = "Close window" })
vim.keymap.set("n", "<leader>so", ":only<CR>", { desc = "Close all windows except current one" })
vim.keymap.set("n", "<leader>to", ":tabnew<CR>", { desc = "Open new tab" })
vim.keymap.set("n", "<leader>tx", ":tabclose<CR>", { desc = "Close tab" })
vim.keymap.set("n", "<leader>tn", ":tabnext<CR>", { desc = "Next tab" })
vim.keymap.set("n", "<leader>tp", ":tabprevious<CR>", { desc = "Previous tab" })
vim.keymap.set("n", "<leader>tf", "<cmd>tabnew %<CR>", { desc = "Open file in new tab" })

-- Copy to system clipboard
vim.keymap.set({ "n", "v" }, "<leader>y", [["+y]])
vim.keymap.set("n", "<leader>Y", [["+Y]])

-- Format code
vim.keymap.set("n", "<leader>f", vim.lsp.buf.format)

-- Shortcut for searching and replacing
vim.keymap.set("n", "<leader>s", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]])

-- Switch between projects via tmux
vim.keymap.set("n", "<C-f>", "<cmd>silent !tmux neww tmux-sessionizer<CR>")

-- Save the current file
vim.keymap.set("n", "<leader>w", function()
	vim.cmd("w")
end)
