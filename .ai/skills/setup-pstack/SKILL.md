---
name: setup-pstack
description: Configure which models pstack uses per role on this machine, for whichever harness you run (Cursor, Claude Code, Codex CLI). Detects your available models and writes a shared config file that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", or changing pstack's model choices.
---

# Setup pstack

Write `~/.agents/pstack/models.md`, a per-role model map that every pstack skill reads. The skills fall back to their harness defaults (`../rigorous-mode/references/models.md`) when a line is absent, so this is an override layer, not a requirement. The same file serves Cursor, Claude Code, and Codex; values are whatever identifiers the current harness accepts.

## Steps

### 1. Detect the harness and its models

Identify the harness from your tool list (`../rigorous-mode/references/harness.md`). Then enumerate the model identifiers you can pass when spawning a subagent in this session; that is the dependable source. If the harness exposes a models list (a CLI or API), prefer it for completeness. Codex has no per-spawn model, so its only valid values are `inherit-parent` and `auto`; say so and skip to step 5 with every role set to `inherit-parent` unless the user wants to set `default_subagent_model` in `~/.codex/config.toml` instead. If you cannot detect any models, ask the user to paste the identifiers they have access to. Never write a real identifier you have not confirmed is available. The aliases `inherit-parent` and `auto` are always valid.

### 2. Load current state

If `~/.agents/pstack/models.md` exists, read the current harness's section and treat its values as the current choices. If it does not but the legacy Cursor rule `~/.cursor/rules/pstack-models.mdc` does, read that instead and migrate its lines. Otherwise start from the harness defaults in `models.md`.

### 3. Map and confirm

Show every role with its current model, marking any real identifier not in the detected set as needing a choice. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` and `auto` (both mean: this role runs on the parent chat model, which is how "Auto" users stay on Auto) as the options. Use the structured-question tool over free text. For panel roles (how critics, arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose model family differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every real identifier written must be in the detected set; `inherit-parent` and `auto` always pass. If a chosen identifier is not available, stop and ask again. A config pointing at a model the user cannot use breaks every delegation that reads it.

### 5. Write the config

Write the current harness's section of `~/.agents/pstack/models.md` (`## cursor`, `## claude-code`, or `## codex`) in the shape shown under "Config file format" in `../rigorous-mode/references/models.md`, one line per role. Leave the other harnesses' sections untouched so the file keeps working on every machine that syncs it. Rewrite the whole section so re-runs stay idempotent.

### 6. Register the named agents (Codex only)

Codex addresses subagents by role, not by plugin agent file. A role is an `[agents.<name>]` entry in `~/.codex/config.toml` whose `config_file` is a TOML config overlay for that role. Write one overlay per pstack agent under `~/.codex/agents/`, carrying the agent file's body as `developer_instructions`, and register it. Leave existing entries untouched.

`~/.codex/agents/rigorous-agent.toml`:

```toml
developer_instructions = """
<body of <pstack install path>/agents/rigorous-agent.md, below its frontmatter>
"""
```

`~/.codex/agents/comment-sicko.toml`: the same shape with the body of `agents/comment-sicko.md`, plus `sandbox_mode = "read-only"` since that agent never writes.

`~/.codex/config.toml`:

```toml
[agents.rigorous-agent]
description = "pstack rigorous-mode delegate"
config_file = "~/.codex/agents/rigorous-agent.toml"

[agents.comment-sicko]
description = "pstack read-only comment reviewer"
config_file = "~/.codex/agents/comment-sicko.toml"
```

Confirm the role appears when you spawn a subagent. If your Codex version rejects the overlay keys, fall back to the harness reference's rule: paste the agent file's body into the spawn prompt instead.

On Cursor and Claude Code the plugin's `agents/` directory registers these automatically; skip this step.

### 7. Confirm

Tell the user the config was written, that it applies to new sessions, and that it is shared across harnesses. Re-running this skill updates it.

### 8. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill` (resolves wherever pstack is installed). On no, move on without pushing.
