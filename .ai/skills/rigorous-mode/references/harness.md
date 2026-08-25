# Harness reference

pstack runs on Cursor (IDE and CLI), Claude Code, and Codex CLI. The skills describe work in capability terms ("spawn a background worker", "ask the user", "open a todo list") and this file maps each capability to the concrete tool in the harness you are running in. Detect the harness from your tool list, then use the matching column. When a capability is missing in your harness, use the fallback in the last column instead of skipping the step.

## Capability map

| Capability | Cursor | Claude Code | Codex CLI | Fallback when absent |
|---|---|---|---|---|
| Spawn a subagent | `Task` tool | `Agent` tool | `spawn_agent` tool | Do the work inline, in sequence, and say so in the reply. |
| Named pstack agent | `subagent_type: "<name>"` | `subagent_type: "<name>"` (`"pstack:<name>"` when installed as a plugin) | An `[agents.<name>]` role in `~/.codex/config.toml` (written by `/setup-pstack`); otherwise inline the body of `~/.codex/agents/<name>.md` into the spawn prompt | Paste the agent file body into the prompt. |
| Generic worker | `subagent_type: generalPurpose` | `subagent_type: general-purpose` | `spawn_agent` with no role | Same. |
| Background spawn | `run_in_background: true` | `run_in_background: true` | Spawns are asynchronous by default; collect with `wait_agent` | Spawn one at a time. |
| Per-spawn model | `model: <slug>` | `model: <alias>` (`sonnet`, `opus`, `haiku`, `fable`) | Not per spawn. `default_subagent_model` in config.toml, or a role's config file | Omit the model and vary the prompt lens instead (see `models.md`). |
| Read-only worker | `readonly: true` | `subagent_type: Explore`, or an agent whose `tools` list excludes Edit and Write | A role whose config sets `sandbox_mode = "read-only"` | Tell the worker in its prompt that it must not write. |
| MCP access in a worker | Stripped by `readonly: true`; use agent mode when a worker needs MCP tools | Kept; MCP tools load on demand via `ToolSearch` | Kept | Run the MCP queries from the parent. |
| Isolated worker environment | `environment: "cloud"` (plus `cloud_base_branch`) | `isolation: "worktree"` | Give each worker its own `git worktree` in the prompt | One git worktree per worker, concurrency capped by local CPU count. |
| Todo list | Built-in todo list | `TodoWrite` | `update_plan` | A numbered checklist at the top of the reply, updated each turn. |
| Ask the user a structured question | `AskQuestion` | `AskUserQuestion` | `request_user_input` | A plain question in the reply. |
| Recurring wake or heartbeat | `/loop` | `/loop` | None. Run the watcher (`scripts/watch-pr/watch-pr`) or a `sleep` loop in a blocking shell call | Blocking watcher command with a timeout. |
| Skill authoring skill | `create-skill` (built-in) | `skill-creator` (Anthropic's skill, install it when absent) | `$skill-creator` (bundled) | Follow `playbooks/authoring-a-skill.md` and validate by hand. |
| Slash invocation | `/name` | `/name` or `/pstack:name` | `$name` | Say "use the `<name>` skill". |
| Review bots on PRs | Bugbot | Claude code review | Codex review | Any automated reviewer; the triage rules in `references/bugbot-triage.md` apply to all of them. |

## Paths

| Thing | Cursor | Claude Code | Codex CLI |
|---|---|---|---|
| Project skills directory | `.cursor/skills/` | `.claude/skills/` | `.agents/skills/` |
| Personal skills directory | `~/.cursor/skills/` | `~/.claude/skills/` | `~/.codex/skills/` (also `~/.agents/skills/`) |
| Installed plugins | `~/.cursor/plugins/` | `~/.claude/plugins/` | `~/.codex/plugins/` |
| Session transcripts | `~/.cursor/projects/<slug>/agent-transcripts/` (`<slug>` is the workspace path with the leading slash dropped and each `/` turned into `-`; layouts: `<id>.jsonl`, `<id>/<id>.jsonl`, `<parent>/subagents/<child>.jsonl`) | `~/.claude/projects/<slug>/*.jsonl` (`<slug>` is the workspace path with each `/` turned into `-`, leading dash kept) | `~/.codex/sessions/<YYYY>/<MM>/<DD>/*.jsonl` (all workspaces; filter by the `cwd` field) |
| pstack model config | `~/.agents/pstack/models.md` (see `models.md`) | same | same |
| pstack agent definitions (`rigorous-agent.md`, `comment-sicko.md`) | `~/.cursor/agents/` | `~/.claude/agents/` | `~/.codex/agents/` |

Antigravity also reads these skills: the CLI (`agy`) from `~/.gemini/config/skills/`, the IDE from `~/.gemini/antigravity/skills/`, both from `<workspace>/.agents/skills/` (project); its agents are `~/.gemini/config/agents/<name>/agent.md`. Treat it like Codex in the capability map: no per-spawn model parameter, `--model` on the CLI instead.

Transcript rules hold on every harness. Read only the active workspace's transcripts. Never glob across other projects' directories; that reads private chats from unrelated work. Order candidates by modification time (`ls -t`), never by id.

## Generated project skills

When a pstack skill writes a project-local skill (for example `verify-<app>` from `create-verification-skill`, or a personal `-mode` skill from `automate-me`), write it under the current harness's project skills directory from the table above. If the repository already has one of the three directories, use that one. To make the skill visible to the other harnesses too, symlink the same directory from their project skills directories; the SKILL.md format is shared.

## Optional Cursor extras

The `cursor-team-kit` plugin ships `deslop`, `control-cli`, and `control-ui`. pstack does not depend on them. Pre-commit cleanup lives in the **no-comments** skill, and live verification goes through the project's `verify-<app>` skill generated by **create-verification-skill**. When `cursor-team-kit` is installed you may use its skills as a supplement.
