---
name: antigravity
description: Wield the Antigravity CLI (`agy`) as an auxiliary AI agent for adversarial review, plan critique, subagent delegation, code review, second opinions from another model family, and general consult. Use when a task benefits from an independent AI perspective, when delegating a self-contained chunk of work, when stress-testing a plan or diff, or when the user explicitly requests Antigravity / `agy`. Supersedes the old gemini-cli skill.
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
---

# Antigravity CLI Integration Skill

This skill lets the current agent (Claude Code, Codex, or Cursor) orchestrate the Antigravity CLI (`agy`) as an auxiliary agent for adversarial review, plan critique, subagent delegation, code review, codebase research, and general consult.

Antigravity replaced the Gemini CLI integration. Default to `agy` whenever an "outside opinion" or "delegated subagent" pattern would help.

## Non-interactive only. This is the rule that matters most.

`agy` is a CLI built for humans first. Every command you run must be one that finishes on its own and puts its whole answer on stdout. You never see a terminal; anything that waits for a keypress, opens a TUI, or streams a partial answer hangs your turn or hands you a truncated result. The `cli-for-agents` skill is the general guide to running CLIs this way; read it once, then apply these `agy` specifics:

- **Always `-p` (`--print`).** Never run bare `agy` (opens the interactive TUI) and never use `-i` / `--prompt-interactive` (starts a session that waits for a human).
- **Always `--dangerously-skip-permissions`.** Without it `agy` stops to ask for tool approval, and nobody is there to answer.
- **Always `--disable-slash-commands`** in scripted use, so a `/word` in your prompt is not expanded as a slash command.
- **Capture full stdout, then read it whole.** End every call with `2>&1`. For anything longer than a quick question, redirect to a file, wait for the process to exit, then read the entire file. Do not `tail` a running job and act on a partial answer.
- **Set `--print-timeout`** above the job's expected length (default `5m`). A timeout produces an incomplete answer, not an error you can retry.
- **Ask for machine-readable output when you will parse it:** `--output-format json`, or `--json-schema <file-or-string>` to enforce a shape.
- **Avoid subcommands that may prompt** (`agy install`, `agy update`, `agy plugin install`). Tell the user to run those.
- **Write prompts that leave no room for a clarifying question.** `--dangerously-skip-permissions` skips tool approvals, not `agy`'s own questions. Give the goal, inputs, constraints, and exact deliverable; say "do not ask for confirmation".

## Model selection

`agy models` lists what your account can run. Pick with `--model`, and set `--effort high` unless speed matters more than depth.

| Need | Model |
|---|---|
| Default: judgment, review, design critique, anything you will act on | `gemini-3.1-pro-high` (the strongest Gemini available; `gemini-3.1-pro-low` for the same model at lower effort) |
| Fast or bulk: mechanical edits, summaries, many parallel calls | `gemini-3.7-flash-high` (`-medium` / `-low` to trade depth for speed) |
| A second opinion from a different model family than the one you are running on | `claude-opus-4-6-thinking`, `claude-sonnet-4-6`, or `gpt-oss-120b-medium` |

If a model id is rejected, run `agy models` and pick the closest current entry; model lists change between releases.

## Core Invocation Pattern

```bash
agy --dangerously-skip-permissions --disable-slash-commands \
  --model gemini-3.1-pro-high --effort high \
  -p "<prompt>" 2>&1
```

**Flag order matters.** `-p` consumes the next argument as the prompt, so put every other flag before `-p`, or put the prompt immediately after `-p`:

```bash
# OK
agy --dangerously-skip-permissions --model gemini-3.1-pro-high -p "<prompt>"
agy -p "<prompt>" --dangerously-skip-permissions --model gemini-3.1-pro-high

# BROKEN: `--sandbox` becomes the prompt and "<prompt>" is a stray argument
agy -p --sandbox "<prompt>"
```

Key flags (verified against `agy --help`, CLI 1.1.20):

| Flag | Purpose |
|---|---|
| `-p`, `--print`, `--prompt` | Run a single prompt non-interactively and print the response |
| `--model <id>` | Model for this session (see Model selection) |
| `--effort low\|medium\|high` | Reasoning effort |
| `--output-format text\|json\|stream-json` | Output format in print mode (default `text`) |
| `--json-schema <schema or path>` | Enforce structured output |
| `--dangerously-skip-permissions` | Auto-approve tool permission requests |
| `--disable-slash-commands` | Do not expand slash commands or skills in the prompt |
| `--print-timeout <duration>` | Timeout for print mode (default `5m`) |
| `--add-dir <path>` | Add a directory to the workspace (repeatable) |
| `--sandbox` | Run with terminal restrictions |
| `--mode accept-edits\|plan` | Agent execution mode |
| `-c`, `--continue` / `--conversation <id>` | Continue the last conversation or a specific one |
| `--agent <name>`, `--project <id>` | Pick a configured agent or project |
| `-i`, `--prompt-interactive` | Interactive session. Never use from an agent. |

Subcommands: `models`, `agents`, `mcp`, `plugin`, `changelog`, `update`, `install`, `help`.

## Verifying Installation

Before first use in a session:

```bash
command -v agy && agy --version
```

If missing, surface that to the user; do not silently fall back to another tool.

## Critical Behavioral Notes

- **Default timeout is 5 minutes.** For refactors and large reviews pass `--print-timeout 15m` or more, or background the job and read the file when it exits.
- **Workspace scoping.** `agy` runs in the current working directory; add other roots with repeated `--add-dir`.
- **Conversation continuity.** `-c` continues the last conversation, `--conversation <id>` a specific one, for multi-turn consult where the first reply needs follow-up.
- **You own the result.** Read what `agy` changed, run tests / type-check / lint, and check the change against the original intent before trusting it.

## Mode Playbooks

Every example below uses the default model; swap `--model` per the table above. `AGY` stands for the core invocation prefix:

```bash
AGY="agy --dangerously-skip-permissions --disable-slash-commands --model gemini-3.1-pro-high --effort high"
```

### Adversarial review (challenge)

Frame the prompt as an attack: `agy`'s job is to find flaws.

```bash
$AGY -p \
  "You are an adversarial reviewer. Your job is to break the following plan / diff. \
   Find edge cases, race conditions, security holes, broken assumptions, and missing tests. \
   Be ruthless. Output a numbered list of concrete problems, severity (HIGH/MED/LOW), \
   and the smallest reproducible scenario for each.

   <plan or diff here>" 2>&1
```

### Plan / second-opinion review

```bash
$AGY -p \
  "Review the plan below as a senior engineer. \
   Output: (1) what's strong, (2) what's risky, (3) concrete suggested changes, \
   (4) verdict: SHIP / REVISE / RETHINK.

   <plan>" 2>&1
```

For a second opinion from a different model family than your own, use `--model claude-opus-4-6-thinking` (or `gpt-oss-120b-medium`) here.

### Subagent delegation (self-contained task)

```bash
$AGY --print-timeout 15m -p \
  "Task: <one-line goal>.
   Inputs: <files/paths/data>.
   Constraints: <style, deps, must-not-touch>.
   Deliverable: <exact output format: file contents, patch, JSON, etc.>.
   Apply edits directly. Do not ask for confirmation." 2>&1
```

Long jobs run in the background and are read whole when done:

```bash
$AGY --print-timeout 30m -p "<prompt>" > /tmp/agy-out.txt 2>&1 &
AGY_PID=$!
# ... continue other work ...
wait $AGY_PID; cat /tmp/agy-out.txt
```

Mechanical bulk work (renames, fixture generation, many small edits) is the case for `--model gemini-3.7-flash-high`.

### Code review on a diff

```bash
git diff <base>...HEAD > /tmp/diff.patch
$AGY -p \
  "Review this diff for: (1) correctness bugs, (2) security issues, \
   (3) style / consistency, (4) missing tests. \
   For each finding: file:line, severity, why, suggested fix.

   $(cat /tmp/diff.patch)" 2>&1
```

For findings you will parse, add `--output-format json` and describe the JSON shape in the prompt, or pass `--json-schema`.

### General consult / Q&A with follow-up

```bash
$AGY -p "<question>" 2>&1
$AGY -c -p "<follow-up>" 2>&1
```

### Codebase research

```bash
$AGY --add-dir /path/to/repo --print-timeout 15m -p \
  "Investigate the codebase at the workspace root. \
   Answer: <specific question>. \
   Cite file paths and line numbers in the answer." 2>&1
```

## Standard Integration Workflow

The Generate → Review → Fix loop:

```bash
# 1. Generate (you write the code)
# 2. Independent review by agy
$AGY -p "Review <file> for bugs, security issues, and style. Be thorough." 2>&1
# 3. Apply the fixes yourself, or delegate them back:
$AGY -p "Fix these issues in <file>: <list>. Apply edits directly. Do not ask for confirmation." 2>&1
```

Always validate `agy` output before trusting it: read the changed files, run tests / type-check / lint, and verify the change matches the original intent.

## Error Handling

- **Timeout.** Raise `--print-timeout` or background the job; a timed-out answer is incomplete, never partially usable.
- **Auth / config issues.** `agy --version` confirms the CLI loads; surface failures to the user, do not silently retry.
- **It asked a question instead of working.** The prompt was underspecified. Rewrite with explicit goal, inputs, constraints, output format, and "do not ask for confirmation".
- **Unknown model.** Run `agy models` and pick a current id.

## Plugins and Updates

`agy plugin list`, `agy plugin install <target>`, `agy plugin import gemini|claude`, `agy update`, `agy changelog`. These may prompt; hand them to the user rather than running them from a script.

## See Also

- `references/reference.md`: full flag and subcommand reference, with examples.
- The `cli-for-agents` skill: how to run any CLI non-interactively and read its complete output.
