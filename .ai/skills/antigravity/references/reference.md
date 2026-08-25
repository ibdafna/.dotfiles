# Antigravity CLI (`agy`) — Full Reference

This is the complete flag and subcommand reference for the Antigravity CLI, as verified against `agy --help` at version `1.0.1`. Load this file when fine-grained CLI control is needed.

## Top-level flags

| Flag | Description |
|---|---|
| `--add-dir <path>` | Add a directory to the workspace. Repeatable. |
| `-c`, `--continue` | Continue the most recent conversation. |
| `--conversation <id>` | Resume a previous conversation by ID. |
| `--dangerously-skip-permissions` | Auto-approve all tool permission requests without prompting. |
| `-i`, `--prompt-interactive` | Run an initial prompt interactively and continue the session. |
| `--log-file <path>` | Override the CLI log file path. |
| `-p`, `--print`, `--prompt` | Run a single prompt non-interactively and print the response. |
| `--print-timeout <duration>` | Timeout for print mode wait. Default `5m0s`. Accepts Go-style durations (`30s`, `10m`, `1h`). |
| `--sandbox` | Run in a sandbox with terminal restrictions enabled. |

## Subcommands

| Subcommand | Description |
|---|---|
| `agy changelog` | Show changelog and release notes. |
| `agy help [subcommand]` | Show help for the top-level CLI or a specific subcommand. |
| `agy install` | Configure environment paths and shell settings. |
| `agy plugin <cmd>` | Manage plugins. Alias: `agy plugins`. |
| `agy update` | Update the CLI. |

### `agy plugin` commands

| Command | Description |
|---|---|
| `agy plugin list` | List imported plugins. |
| `agy plugin import [source]` | Import plugins from `gemini` or `claude`. |
| `agy plugin install <target>` | Install a plugin. Supports `plugin@marketplace` syntax. |
| `agy plugin uninstall <name>` | Uninstall a plugin. |
| `agy plugin enable <name>` | Enable a plugin. |
| `agy plugin disable <name>` | Disable a plugin. |
| `agy plugin validate [path]` | Validate a plugin. |
| `agy plugin link <mp> <target>` | Generate a link to a marketplace. |
| `agy plugin help` | Show plugin help. |

## Common invocation patterns

### Non-interactive prompt

```bash
agy --dangerously-skip-permissions -p "<prompt>" 2>&1
```

### Non-interactive with extended timeout

```bash
agy --dangerously-skip-permissions -p --print-timeout 20m "<prompt>" 2>&1
```

### Multi-root workspace

```bash
agy --dangerously-skip-permissions -p \
  --add-dir /path/to/repo-a \
  --add-dir /path/to/repo-b \
  "<prompt>" 2>&1
```

### Continue most recent conversation

```bash
agy -c -p --dangerously-skip-permissions "<follow-up>" 2>&1
```

### Resume specific conversation by ID

```bash
agy --conversation <conversation-id> -p --dangerously-skip-permissions "<follow-up>" 2>&1
```

### Background long-running job

```bash
agy --dangerously-skip-permissions -p --print-timeout 30m "<prompt>" \
  > /tmp/agy-out.txt 2>&1 &
```

Monitor via `BashOutput` (preferred in Claude Code) or `tail -f /tmp/agy-out.txt`.

### Sandbox mode

```bash
agy --dangerously-skip-permissions -p --sandbox "<prompt>" 2>&1
```

Use when running untrusted tasks or prompts that might trigger shell commands you don't want loose on the host.

## Output format

`agy --print` returns plain text on stdout. There is no built-in `-o json` flag.

If structured output is needed, instruct `agy` in the prompt itself:

```bash
agy --dangerously-skip-permissions -p \
  "<task>. Output ONLY valid JSON matching this schema: { \"findings\": [{\"file\": str, \"line\": int, \"severity\": \"HIGH|MED|LOW\", \"note\": str}] }. No prose, no markdown fences." 2>&1
```

## Duration format

`--print-timeout` accepts Go-style durations:

- `30s` — 30 seconds
- `5m` — 5 minutes (default)
- `15m` — 15 minutes
- `1h` — 1 hour
- `1h30m` — combined

## Prompt-quality checklist for delegation

When delegating work to `agy`, a complete prompt should specify:

1. **Goal** — one-line statement of what success looks like
2. **Inputs** — file paths, data, context to read
3. **Constraints** — style, dependencies, what not to touch
4. **Deliverable** — exact output format (file edits applied, patch on stdout, JSON, etc.)
5. **Autonomy directive** — "Apply edits directly. Do not ask for confirmation."

Without these, `agy` may stall asking clarifying questions that `--dangerously-skip-permissions` does not suppress.
