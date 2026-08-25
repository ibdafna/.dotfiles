# Env config files

This repo contains my tmux and nvim configuration. A lot of the content here
is inspired by the configs from [ThePrimeagen](https://github.com/ThePrimeagen/.dotfiles) and [josean-dev](https://github.com/josean-dev/dev-environment-files) (thank you!)

## How to use these files

Clone the repo anywhere, then run:

```bash
./install
```

The installer now:

- Symlinks each top-level config directory from `.config/` into `~/.config/`
- Symlinks `bin/tmux-sessionizer` into both `~/.local/bin` and `~/bin`
- Installs shell-specific files based on your login shell in `$SHELL`
- Backs up conflicting files and directories before replacing them

You can also force a specific shell:

```bash
./install bash
./install zsh
./install all
```

To install core macOS dependencies and bootstrap plugin managers:

```bash
./install --install-deps --bootstrap-plugins zsh
```

This currently installs core packages with Homebrew:

- `git`
- `neovim`
- `tmux`
- `fzf`
- `ripgrep`
- `fd`
- `starship`

The repo can also manage portable AI CLI config under `.ai/`:

- `.ai/claude/settings.json` -> `~/.claude/settings.json`
- `.ai/claude/CLAUDE.md` -> `~/.claude/CLAUDE.md`
- `.ai/claude/agents/*` -> `~/.claude/agents/*`
- `.ai/skills/*` -> `~/.claude/skills/*`, `~/.codex/skills/*`, `~/.agents/skills/*`, `~/.cursor/skills/*` (one folder of plain SKILL.md directories shared by every agent)
- `.ai/gemini/settings.json` -> `~/.gemini/settings.json`
- `.ai/gemini/GEMINI.md` -> `~/.gemini/GEMINI.md`
- `.ai/gemini/commands/*` -> `~/.gemini/commands/*`
- `.ai/gemini/extensions/*` -> `~/.gemini/extensions/*`
- `.ai/codex/config.toml` -> `~/.codex/config.toml`
- `.ai/codex/skills/*` -> `~/.codex/skills/*`

Only portable config should live there. Do not commit auth, session history, caches, or other tool-managed state.

If you see anything bad in here, do me a solid and open a PR 😄

## Misc notes

Some of the extensions assume patched fonts which allow for icons to be rendered as glyphs - are installed. These can be downloaded from [Nerd Fonts](https://www.nerdfonts.com/font-downloads)

`tmux-sessionizer` expects `tmux` and `fzf` to be installed, and it searches for projects under `~/dev` and `~/dfx`.

The Neovim config also assumes:

- `git` so the plugin manager can clone plugins
- `ripgrep` for Telescope live grep
- `make` so `telescope-fzf-native.nvim` can build

Some integrations are still optional and are not bootstrapped automatically, including `getopenaikey` for ChatGPT-style plugins and any extra local tools you may layer on top of these dotfiles.
