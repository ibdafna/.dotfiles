-- Leader key
vim.g.mapleader = " "

-- Open the file browser
vim.keymap.set("n", "<leader>pv", vim.cmd.Ex)

-- Move selected line / block of text in visual mode
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

-- Keeps the cursor in place while joining lines
vim.keymap.set("n", "J", "mzJ`z")

-- Keeps the cursor in the middle when jumping up or down
vim.keymap.set("n", "<C-d>", "<C-d>zz")
vim.keymap.set("n", "<C-u>", "<C-u>zz")

-- Keeps the cursor in place when jumping between words during search
vim.keymap.set("n", "n", "nzzzv")
vim.keymap.set("n", "N", "Nzzzv")

-- Paste selected word over current word but keep the pasted word in buffer
vim.keymap.set("x", "<leader>p", [["_dP]])

-- Cut selected word without adding it to the buffer
vim.keymap.set("n", "<leader>x", [["_x]])

-- Copy to system clipboard
vim.keymap.set({"n", "v"}, "<leader>y", [["+y]])
vim.keymap.set("n", "<leader>Y", [["+Y]])

-- Managing windows
vim.keymap.set("n", "<leader>sv", ":vsplit<CR>")
vim.keymap.set("n", "<leader>sh", ":split<CR>")
vim.keymap.set("n", "<leader>se", ":wincmd =<CR>")
vim.keymap.set("n", "<leader>sx", ":close<CR>")

-- Moving between splits
function my_custom_function()
    -- Get a single character of input from the user
    local char = vim.fn.getchar()

    -- Convert the ASCII value to a character
    local char = vim.fn.nr2char(char)

    -- Perform an action based on the input
    if char == 'h' then
        vim.cmd('wincmd h')
    elseif char == 'j' then
      vim.cmd('wincmd j')
    elseif char == 'k' then
      vim.cmd('wincmd k')
    elseif char == 'l' then
      vim.cmd('wincmd l')
    end
end

vim.api.nvim_set_keymap('n', '<leader>m', ':lua my_custom_function()<CR>', {noremap = true, silent = true})

-- Deleting to the void register in normal and visual mode
vim.keymap.set({"n", "v"}, "<leader>d", [["_d]])

-- Noop for Q
vim.keymap.set("n", "Q", "<nop>")

-- Format code
vim.keymap.set("n", "<leader>f", vim.lsp.buf.format)

-- Exit insert mode
vim.keymap.set("i", "jk", "<ESC>")

-- Shortcut for searching and replacing
vim.keymap.set("n", "<leader>s", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]])

-- Switch between projects via tmux
vim.keymap.set("n", "<C-f>", "<cmd>silent !tmux neww tmux-sessionizer<CR>")

-- Source the current file
vim.keymap.set("n", "<leader><leader>", function()
    vim.cmd("so")
end)

-- Save the current file
vim.keymap.set("n", "<leader>w", function()
    vim.cmd("w")
end)

-- Save and quit
vim.keymap.set("n", "<leader>q", function()
    vim.cmd("wq")
end)

-- Quit without saving
vim.keymap.set("n", "<leader>Q", function()
    vim.cmd("q!")
end)


-- Extension mappings
-- Toggle tree
vim.keymap.set("n", "<leader>tt", ":NvimTreeToggle<CR>")
-- ChatGPT
vim.keymap.set("n", "<leader>cg", ":ChatGPT<CR>")
-- Vim Fugitive
vim.keymap.set("n", "<leader>gs", vim.cmd.Git)
