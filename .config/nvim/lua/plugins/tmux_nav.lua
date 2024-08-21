return {
  {
    "alexghergh/nvim-tmux-navigation",
    priority = 1000,
    config = function()
      local nvim_tmux_nav = require("nvim-tmux-navigation")
      nvim_tmux_nav.setup({
        disable_when_zoomed = true, -- defaults to false
      })
      -- keymaps are defined in the keymaps.lua file.
    end,
  },
}
