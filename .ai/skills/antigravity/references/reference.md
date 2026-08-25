# Antigravity CLI (`agy`) Full Reference

Complete flag and subcommand reference for the Antigravity CLI, verified against `agy --help` at version `1.1.20`. Load this file when fine-grained CLI control is needed. Every pattern here is non-interactive; see `SKILL.md` for why that is the only mode an agent may use.

## Top-level flags

| Flag | Description |
|---|---|
| `-p`, `--print`, `--prompt` | Run a single prompt non-interactively and print the response. |
| `--model <id>` | Model for the session. `agy models` lists the ids. |
| `--effort low\|medium\|high` | Reasoning effort for the session. |
| `--output-format text\|json\|stream-json` | Output format in print mode. Default `text`. |
| `--input-format text\|stream-json` | Input format in print mode. `stream-json` reads one NDJSON message per line from stdin and runs a turn for each; requires `--output-format stream-json`. |
| `--json-schema <schema or path>` | Enforce structured output (for `stream-json`, applies to the final result only). |
| `--dangerously-skip-permissions` | Auto-approve all tool permission requests without prompting. |
| `--disable-slash-commands` | Disable slash command and skill expansion in print mode. |
| `--print-timeout <duration>` | Timeout for print mode wait. Default `5m0s`. Go-style durations (`30s`, `10m`, `1h`). |
| `--add-dir <path>` | Add a directory to the workspace. Repeatable. |
| `--sandbox` | Run in a sandbox with terminal restrictions enabled. |
| `--mode accept-edits\|plan` | Agent execution mode for the session. |
| `--agent <name>` | Agent for the session (`agy agents` lists them). |
| `--project <id or name>` | Project for the session. |
| `--new-project` | Create a new project for this session. |
| `-c`, `--continue` | Continue the most recent conversation. |
| `--conversation <id>` | Resume a previous conversation by ID. |
| `--log-file <path>` | Override the CLI log file path. |
| `-i`, `--prompt-interactive` | Run an initial prompt interactively and continue the session. Never from an agent. |

## Subcommands

| Subcommand | Description |
|---|---|
| `agy models` | List available models with ids and display names. |
| `agy agents` (alias `agent`) | List available agents. |
| `agy mcp <add\|remove\|list\|enable\|disable>` | Manage MCP servers. |
| `agy plugin <cmd>` (alias `plugins`) | Manage plugins. |
| `agy changelog` | Show changelog and release notes. |
| `agy update` | Update the CLI. May prompt; hand to the user. |
| `agy install` | Configure environment paths and shell settings. May prompt; hand to the user. |
| `agy mic-serve` | Serve this machine's microphone to a CLI on another host. Not for agents. |
| `agy help [subcommand]` | Help for the CLI or a subcommand. |

### `agy plugin` commands

| Command | Description |
|---|---|
| `agy plugin list` | List imported plugins. |
| `agy plugin import [source]` | Import plugins from `gemini` or `claude`. |
| `agy plugin install <target>` | Install a plugin. Supports `plugin@marketplace` syntax. |
| `agy plugin uninstall <name>` | Uninstall a plugin. |
| `agy plugin enable <name>` / `disable <name>` | Toggle a plugin. |
| `agy plugin validate [path]` | Validate a plugin. |
| `agy plugin link <mp> <target>` | Generate a link to a marketplace. |

## Models

`agy models` at 1.1.20 returned, in this order: `gemini-3.7-flash-high|medium|low`, `gemini-3.6-flash-high|medium|low`, `gemini-3.5-flash-high|medium|low`, `gemini-3.1-pro-high|low`, `claude-sonnet-4-6`, `claude-opus-4-6-thinking`, `gpt-oss-120b-medium`. The list changes between releases; rerun the command rather than trusting this snapshot. Defaults for this skill: `gemini-3.1-pro-high` for judgment, `gemini-3.7-flash-high` for speed, a Claude or GPT id for a cross-family second opinion.

## Common invocation patterns

The prefix used throughout:

```bash
AGY="agy --dangerously-skip-permissions --disable-slash-commands --model gemini-3.1-pro-high --effort high"
```

### Non-interactive prompt

```bash
$AGY -p "<prompt>" 2>&1
```

### Extended timeout

```bash
$AGY --print-timeout 20m -p "<prompt>" 2>&1
```

### Multi-root workspace

```bash
$AGY --add-dir /path/to/repo-a --add-dir /path/to/repo-b -p "<prompt>" 2>&1
```

### Continue a conversation

```bash
$AGY -c -p "<follow-up>" 2>&1
$AGY --conversation <conversation-id> -p "<follow-up>" 2>&1
```

### Background long-running job

```bash
$AGY --print-timeout 30m -p "<prompt>" > /tmp/agy-out.txt 2>&1 &
AGY_PID=$!
wait $AGY_PID
cat /tmp/agy-out.txt
```

Read the file only after the process exits. A partial file is a partial answer.

### Sandbox mode

```bash
$AGY --sandbox -p "<prompt>" 2>&1
```

Use for untrusted tasks or prompts that might trigger shell commands you don't want loose on the host.

## Output format

`text` (default) prints the response as plain text. `json` wraps the result in a JSON envelope for parsing. `--json-schema` constrains the model's answer to a shape:

```bash
$AGY --output-format json --json-schema /tmp/findings.schema.json -p \
  "<task>. Return findings as JSON: file, line, severity (HIGH|MED|LOW), note." 2>&1
```

Without a schema, still tell the model in the prompt exactly what shape to emit and to omit prose and fences.

## Duration format

`--print-timeout` accepts Go-style durations: `30s`, `5m` (default), `15m`, `1h`, `1h30m`.

## Prompt-quality checklist for delegation

A complete delegation prompt specifies:

1. **Goal.** One-line statement of what success looks like.
2. **Inputs.** File paths, data, context to read.
3. **Constraints.** Style, dependencies, what not to touch.
4. **Deliverable.** Exact output format (file edits applied, patch on stdout, JSON, etc.).
5. **Autonomy directive.** "Apply edits directly. Do not ask for confirmation."

Without these, `agy` may stall asking clarifying questions that `--dangerously-skip-permissions` does not suppress, and a stalled print-mode run ends as a timeout, not an answer.
