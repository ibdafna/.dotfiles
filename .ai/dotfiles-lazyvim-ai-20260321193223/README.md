# AI CLI Config

This directory stores portable AI CLI configuration that can be safely tracked in dotfiles.

Safe to commit:

- user settings files
- instruction files like `CLAUDE.md` and `GEMINI.md`
- reusable Codex skills, Claude skills, Gemini commands, and Gemini extensions

Do not commit:

- auth tokens
- session history
- caches or logs
- tool-managed state databases

The installer links these files into the native config locations for Claude Code, Gemini CLI, and Codex.
