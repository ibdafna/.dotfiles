return {
	"jackMort/ChatGPT.nvim",
	config = function()
		local chat_gpt = require("chatgpt")
		chat_gpt.setup({
			api_key_cmd = "getopenaikey",
			openai_params = {
				model = "gpt-4",
			},
			openai_edit_params = {
				model = "gpt-4",
			},
			keymaps = {
				close = "<C-c>",
				yank_last = "<C-y>",
				yank_last_code = "<C-k>",
				scroll_up = "<C-u>",
				scroll_down = "<C-d>",
				new_session = "<C-n>",
				cycle_windows = "<Tab>",
				cycle_modes = "<C-f>",
				select_session = "<Space>",
				rename_session = "r",
				delete_session = "d",
				draft_message = "<C-d>",
				toggle_settings = "<C-o>",
				toggle_message_role = "<C-r>",
				toggle_system_role_open = "<C-s>",
				stop_generating = "<C-x>",
			},
		})
	end,
	dependencies = {
		"MunifTanjim/nui.nvim",
		"nvim-lua/plenary.nvim",
		"nvim-telescope/telescope.nvim",
	},
}
