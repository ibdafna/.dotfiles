# Codex CLI Full Reference

Complete flag and subcommand reference for the OpenAI Codex CLI, verified against `codex --help`, `codex exec --help`, and `codex review --help` at version `0.147.0`. Load this file when fine-grained CLI control is needed. Every pattern here is non-interactive; see `SKILL.md` for why that is the only mode an agent may use.

## `codex exec` flags

| Flag | Description |
|---|---|
| `[PROMPT]` | Initial instructions. Omitted or `-` reads the prompt from stdin. If stdin is piped and a prompt is also given, stdin is appended as a `<stdin>` block, so end argument-prompt runs with `</dev/null`. |
| `-m`, `--model <id>` | Model the agent should use. |
| `-c`, `--config <key=value>` | Override any `~/.codex/config.toml` value. Dotted paths for nested keys. The value is parsed as TOML; if that fails the raw string is used, so `-c approval_policy=never` and `-c approval_policy='"never"'` are equivalent. |
| `-s`, `--sandbox <mode>` | `read-only`, `workspace-write`, or `danger-full-access`. |
| `-C`, `--cd <dir>` | Working root for the agent. |
| `--add-dir <dir>` | Additional writable directory alongside the workspace. Repeatable. |
| `--skip-git-repo-check` | Allow running outside a git repository. |
| `--ephemeral` | Run without persisting session files; the session cannot be resumed. |
| `-o`, `--output-last-message <file>` | Write the agent's last message to a file. |
| `--output-schema <file>` | JSON Schema file describing the final response shape. |
| `--json` | Print events to stdout as JSONL instead of the final message. |
| `--color always\|never\|auto` | Color settings (default `auto`). |
| `-p`, `--profile <name>` | Layer `codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only_HOME/<name>.config.toml` on top of the base config. |
| `--enable <feature>` / `--disable <feature>` | Feature flag toggles (`codex features` lists them). |
| `--strict-config` | Error out on unrecognized `config.toml` fields. |
| `--ignore-user-config` | Do not load `$CODEX_HOME/config.toml` (auth still uses `CODEX_HOME`). |
| `--ignore-rules` | Do not load user or project execpolicy `.rules` files. |
| `-i`, `--image <file>` | Attach image(s) to the prompt. Repeatable. |
| `--oss`, `--local-provider lmstudio\|ollama` | Use a local open-source provider. |
| `--approve-for-me` | Route approval requests through automatic review with the workspace-write sandbox. |
| `--dangerously-bypass-approvals-and-sandbox` | Skip all prompts and run without sandboxing. Only inside an environment that is already sandboxed. |
| `--dangerously-bypass-hook-trust` | Run enabled hooks without persisted hook trust. |

### `codex exec resume`

```
codex exec resume [OPTIONS] [SESSION_ID] [PROMPT]
```

`SESSION_ID` is the UUID printed as `session id:` on stderr by the original run (or a thread name). `--last` picks the newest session recorded for the current directory; `--all` disables that cwd filter. `PROMPT` as `-` reads stdin. Takes the same `-c`, `-i`, `--enable/--disable`, `--strict-config` options; add `--skip-git-repo-check` outside a repository. Not available for `--ephemeral` sessions.

## `codex review` flags

```
codex review [OPTIONS] [PROMPT]
```

| Flag | Description |
|---|---|
| `[PROMPT]` | Custom review instructions (`-` reads stdin). Cannot be combined with a scope flag. |
| `--uncommitted` | Review staged, unstaged, and untracked changes. |
| `--base <branch>` | Review changes against the given base branch. |
| `--commit <sha>` | Review the changes introduced by a commit. |
| `--title <title>` | Commit title to display in the review summary. |
| `-c`, `--config <key=value>` | Config override. This is how to pick a model (`-c model=gpt-5.4-mini`), effort (`-c model_reasoning_effort=low`), and sandbox (`-c sandbox_mode=read-only`); there is no `-m` or `-s`. |
| `--enable` / `--disable` / `--strict-config` | As for `exec`. |

Output: a one-paragraph summary followed by `Review comment:` items, each `[P1]`/`[P2]`/`[P3]` with `path:line-line` and an explanation, on stdout. `codex exec review` is the same command under the `exec` namespace.

## Other subcommands

| Subcommand | Safe from a script? | Description |
|---|---|---|
| `codex doctor` | yes | Diagnose installation, config, auth, and runtime health. |
| `codex features` | yes | Inspect feature flags. |
| `codex completion <shell>` | yes | Shell completion script. |
| `codex apply` | yes | Apply the latest diff produced by the agent as a `git apply`. |
| `codex sandbox <cmd>` | yes | Run a command inside Codex's sandbox. |
| `codex mcp ...`, `codex plugin ...` | list/read only | Manage MCP servers and plugins; install/add variants may prompt. |
| `codex` (bare), `codex resume`, `codex fork` | no | Interactive TUI / session pickers. |
| `codex login`, `codex logout`, `codex update`, `codex app`, `codex cloud` | no | Browser or prompt driven; hand to the user. |
| `codex mcp-server`, `codex app-server`, `codex exec-server`, `codex remote-control` | no | Long-running servers. |

## Models and reasoning effort

Model ids are set with `-m` (exec) or `-c model=<id>` (review). Effort is a config key, `model_reasoning_effort`, with values `minimal`, `low`, `medium`, `high`, `xhigh` (and `ultra` on some models). The account default for both lives in `~/.codex/config.toml`; omitting `-m` uses it. Ids present in the 0.147.0 binary: `gpt-5.6`, `gpt-5.6-pro`, `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.3-codex`, `gpt-5.2-codex`, `gpt-5.2`, `gpt-5`. Availability depends on the account; a rejected id is the signal to drop `-m`.

## Where the output goes

| Stream | Content |
|---|---|
| stdout | The agent's final message only (or JSONL events with `--json`). |
| stderr | `Reading additional input from stdin...` (when stdin is not a tty), the header block (version, workdir, model, provider, approval, sandbox, reasoning effort, `session id: <uuid>`), the transcript (`user`, `codex`, tool calls), and `tokens used`. |
| `-o <file>` | The final message, written when the run completes. |

A stale models-cache `ERROR codex_models_manager::manager: failed to load models cache` line on stderr after an upgrade is harmless; the run still completes.

## Common invocation patterns

Every example uses the full read-only command (no `$PREFIX` variable: zsh does not word-split it, and shell state does not persist between an agent's tool calls).

### Non-interactive prompt

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only -o $OUT/out.md "<prompt>" </dev/null 2>$OUT/log.txt
cat $OUT/out.md
```

### Prompt from a file (long prompts, diffs, plans)

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only -o $OUT/out.md - < $OUT/prompt.md 2>$OUT/log.txt
```

### Edits applied in a repository

```bash
OUT=$(mktemp -d)
codex exec --color never -c approval_policy=never -s workspace-write -C /path/to/repo \
  -o $OUT/out.md "<task>. Apply edits directly. Do not ask for confirmation." \
  </dev/null 2>$OUT/log.txt
git -C /path/to/repo status --short
```

### Extra writable roots

```bash
codex exec ... -s workspace-write -C /path/to/repo-a --add-dir /path/to/repo-b "<prompt>" </dev/null
```

### Structured output

```bash
OUT=$(mktemp -d)
cat > $OUT/findings.schema.json <<'JSON'
{"type":"object","properties":{"findings":{"type":"array","items":{"type":"object",
 "properties":{"file":{"type":"string"},"line":{"type":"integer"},
 "severity":{"type":"string","enum":["HIGH","MED","LOW"]},"note":{"type":"string"}},
 "required":["file","line","severity","note"],"additionalProperties":false}}},
 "required":["findings"],"additionalProperties":false}
JSON
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only --output-schema $OUT/findings.schema.json -o $OUT/out.json - < $OUT/prompt.md 2>$OUT/log.txt
jq . $OUT/out.json
```

### Event stream

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only --json "<prompt>" </dev/null 2>$OUT/log.txt > $OUT/events.jsonl
```

Read the file after exit; the last `agent_message` item is the answer.

### Continue a conversation

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only -o $OUT/out.md "<question>" </dev/null 2>$OUT/log.txt
SID=$(grep -o 'session id: .*' $OUT/log.txt | awk '{print $3}')
codex exec resume --skip-git-repo-check "$SID" "<follow-up>" </dev/null 2>$OUT/log2.txt
```

### Background long-running job

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only -o $OUT/out.md "<prompt>" </dev/null 2>$OUT/log.txt &
CODEX_PID=$!
wait "$CODEX_PID"
cat $OUT/out.md
```

Read the file only after the process exits. A partial file is a partial answer. There is no timeout flag; if a bounded wait is needed, use the shell's job control (`wait`, or `kill` after a deadline) rather than reading early.

### Built-in review

```bash
OUT=$(mktemp -d)
codex review --base main -c sandbox_mode=read-only </dev/null 2>$OUT/log.txt
codex review --uncommitted -c model=gpt-5.4-mini -c model_reasoning_effort=low -c sandbox_mode=read-only </dev/null 2>$OUT/log.txt
```

## Prompt-quality checklist for delegation

A complete delegation prompt specifies:

1. **Goal.** One-line statement of what success looks like.
2. **Inputs.** File paths, data, context to read.
3. **Constraints.** Style, dependencies, what not to touch.
4. **Deliverable.** Exact output format (file edits applied, patch on stdout, JSON, etc.).
5. **Autonomy directive.** "Apply edits directly. Do not ask for confirmation."

Without these, a non-interactive run ends with a clarifying question as its final message instead of finished work.
