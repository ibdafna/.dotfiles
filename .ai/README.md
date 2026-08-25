# AI CLI Config

This directory stores portable AI CLI configuration that can be safely tracked in dotfiles.

Safe to commit:

- user settings files
- instruction files like `CLAUDE.md` and `GEMINI.md`
- reusable agent skills under `skills/` (plain `SKILL.md` directories, shared by Claude Code, Codex, Cursor, and Gemini), Claude agents, Gemini commands, and Gemini extensions

Do not commit:

- auth tokens
- session history
- caches or logs
- tool-managed state databases

The installer links these files into the native config locations for Claude Code, Gemini CLI, and Codex.

## Skills

`skills/` holds plain copies. Nothing is fetched at install time; add or update a skill by editing the files here and committing. Sources worth knowing about when refreshing:

- `rigorous-mode`, `how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, the `principle-*` set, and the rest of pstack: a harness-agnostic fork of the `pstack` plugin from cursor/plugins (entry point renamed from `poteto-mode`). Its two agents live in `agents/`, linked into every harness's agents directory.
- `grill-me`, `grilling`, `which-skill`, `setup-engineering-skills`, `to-tickets`, `implement`, `tdd-loop`, `teach-me`, and the rest of the engineering/productivity set: mattpocock/skills, with `ask-matt` and `setup-matt-pocock-skills` renamed, and `tdd`/`teach` renamed to `tdd-loop`/`teach-me` so they do not clash with pstack's.
- `agent-browser`, `skill-creator`, `antigravity` (the `agy` CLI wrapper, replaces the old gemini-cli skill), `cli-for-agents` (from cursor/plugins), the marketing pack, and the ui.sh design skills: as installed from their upstreams.
