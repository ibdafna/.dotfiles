return {
	"mbbill/undotree",
	config = function()
		local undo_tree = require("undotree")
		vim.cmd.binding("n", "<leader>u", ":UndotreeToggle<CR>")
	end,
}
