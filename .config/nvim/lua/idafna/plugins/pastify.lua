return {
	"TobinPalmer/pastify.nvim",
	cmd = { "Pastify" },
	event = "VeryLazy",
	config = function()
		require("pastify").setup({})
	end,
}
