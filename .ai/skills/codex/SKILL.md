---
name: codex
description: Wield the OpenAI Codex CLI (`codex exec` / `codex review`) as an auxiliary AI agent for adversarial review, plan critique, subagent delegation, diff review, second opinions from the GPT model family, and general consult. Use when a task benefits from an independent AI perspective, when delegating a self-contained chunk of work, when stress-testing a plan or diff, or when the user explicitly asks for Codex ("codex review", "ask codex", "second opinion").
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
---

# Codex CLI Integration Skill

This skill lets the current agent (Claude Code, Codex, Cursor, or Antigravity) orchestrate the OpenAI Codex CLI as an auxiliary agent for adversarial review, plan critique, subagent delegation, code review, codebase research, and general consult.

Codex is the GPT-family counterpart of the `antigravity` skill (Gemini family). If you are already running inside Codex, an "outside opinion" should come from `antigravity` instead; this skill still works for delegation.

## Non-interactive only. This is the rule that matters most.

`codex` is a CLI built for humans first: bare `codex` opens a TUI. Every command you run must be one that finishes on its own and puts its whole answer on stdout or in a file you then read in full. You never see a terminal; anything that waits for a keypress, opens a picker, or streams a partial answer hangs your turn or hands you a truncated result. The `cli-for-agents` skill is the general guide to running CLIs this way; read it once, then apply these `codex` specifics:

- **Only two entry points: `codex exec` and `codex review`.** Never run bare `codex`, `codex resume`, `codex fork` (both open a session picker), `codex cloud`, `codex app`, `codex login`, or `codex update`. Follow-ups go through `codex exec resume <session-id> "<prompt>"`, which is non-interactive; re-pass `-c approval_policy=never -c sandbox_mode=read-only` on it, because a resume takes its policy from the base config, not from the original run.
- **Always `</dev/null`** (or feed the prompt on stdin, see below). When stdin is not a terminal, `codex exec` reads it and appends it to the prompt; an open pipe stalls the run.
- **Never rely on approvals.** Pass `-c approval_policy=never` and an explicit sandbox: `-s read-only` for review, consult, and research; `-s workspace-write` when you want edits applied. There is nobody to answer an approval prompt.
- **Capture the whole answer, then read it whole.** stdout carries only the agent's final message; the header, transcript, and token count go to stderr. Use `-o <file>` to write the final message to a file as well, redirect stderr to a log, wait for the process to exit, then read the file. Do not `tail` a running job and act on a partial answer.
- **Ask for machine-readable output when you will parse it:** `--output-schema <json-schema-file>` constrains the final message to a shape; `--json` prints events as JSONL.
- **Outside a git repository add `--skip-git-repo-check`**, or the run refuses to start. Same for `codex exec resume`.
- **No built-in timeout flag.** For long jobs, run in the background, `wait`, then read the file.
- **Write prompts that leave no room for a clarifying question.** A non-interactive run that wants to ask something ends with the question as its final message, not with work done. Give the goal, inputs, constraints, and exact deliverable; say "do not ask for confirmation".

## Model selection

There is no `codex models` command. Omit `-m` to use the account's configured default (`model` in `~/.codex/config.toml`), or pick explicitly. Reasoning effort is a separate config key, not part of the model id: `-c model_reasoning_effort=<minimal|low|medium|high|xhigh>` (some models also accept `ultra`).

| Need | Flags |
|---|---|
| Default: judgment, review, design critique, anything you will act on | omit `-m` (configured default), or `-m gpt-5.6 -c model_reasoning_effort=high` |
| Hardest problems, worth the wait | `-m gpt-5.6-pro -c model_reasoning_effort=xhigh` |
| Fast or bulk: mechanical edits, summaries, many parallel calls | `-m gpt-5.4-mini -c model_reasoning_effort=low` |

Model ids present in CLI 0.147.0 include `gpt-5.6`, `gpt-5.6-pro`, `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.3-codex`. If an id is rejected, fall back to the configured default (drop `-m`); the available set depends on the account and changes between releases.

## Core Invocation Pattern

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never \
  -c approval_policy=never -s read-only \
  -o $OUT/out.md "<prompt>" </dev/null 2>$OUT/log.txt
cat $OUT/out.md
```

Long prompts (a diff, a plan) go on stdin with `-` as the prompt argument instead of `</dev/null`:

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only \
  -o $OUT/out.md - < $OUT/prompt.md 2>$OUT/log.txt
```

Key flags (verified against `codex exec --help`, CLI 0.147.0):

| Flag | Purpose |
|---|---|
| `[PROMPT]` or `-` | Prompt as an argument, or read from stdin |
| `-m, --model <id>` | Model (see Model selection); `codex review` takes `-c model=<id>` instead |
| `-c key=value` | Any config override; used here for `approval_policy`, `model_reasoning_effort`, `sandbox_mode` |
| `-s, --sandbox read-only\|workspace-write\|danger-full-access` | What the agent's shell commands may touch |
| `-C, --cd <dir>` | Working root for the agent |
| `--add-dir <dir>` | Extra writable directory (repeatable) |
| `--skip-git-repo-check` | Allow running outside a git repository |
| `-o, --output-last-message <file>` | Write the final message to a file |
| `--output-schema <file>` | JSON Schema the final message must satisfy |
| `--json` | Print events to stdout as JSONL |
| `--ephemeral` | Do not persist the session (disables later `resume`) |
| `--color never` | Plain output |
| `-p, --profile <name>` | Layer `$CODEX_HOME/<name>.config.toml` on top of the base config |
| `--dangerously-bypass-approvals-and-sandbox` | No sandbox at all. Only inside an environment that is already sandboxed. |

Subcommands: `exec`, `exec resume`, `review`, `doctor`, `features`, `help` (safe); `resume`, `fork`, `cloud`, `app`, `login`, `update`, and bare `codex` (interactive; not from a script).

## Verifying Installation

Before first use in a session:

```bash
command -v codex && codex --version
```

If missing, surface that to the user; do not silently fall back to another tool.

## Critical Behavioral Notes

- **stdout is the answer, stderr is the log.** A `codex exec` run prints its header (model, sandbox, `session id: <uuid>`), the transcript, and `tokens used` on stderr. Keep the log; the session id in it is what `exec resume` needs.
- **`codex review` reviews a scope, or follows a prompt, not both.** `--uncommitted`, `--base <branch>`, `--commit <sha>` cannot be combined with a custom prompt. To review a diff with your own instructions, use `codex exec` and feed the diff on stdin. `review` has no `-m`/`-s`; pass `-c model=<id>` and `-c sandbox_mode=read-only`.
- **Sandbox `read-only` still lets the agent read the whole workspace** and run read-only commands. `workspace-write` lets it edit files under the working root and `--add-dir` paths.
- **Conversation continuity.** `codex exec resume <session-id> "<follow-up>"` continues a persisted (non-`--ephemeral`) session. Prefer the id from the log over `--last`, which picks the newest session for the cwd and can grab the wrong one.
- **You own the result.** Read what Codex changed, run tests / type-check / lint, and check the change against the original intent before trusting it.

## Mode Playbooks

Every example uses the read-only sandbox; delegation swaps in `-s workspace-write`. Commands are written out in full because shell variables do not word-split in zsh and shell state does not persist between an agent's tool calls.

### Adversarial review (challenge)

Frame the prompt as an attack: Codex's job is to find flaws.

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only -o $OUT/out.md \
  "You are an adversarial reviewer. Your job is to break the following plan / diff. \
   Find edge cases, race conditions, security holes, broken assumptions, and missing tests. \
   Be ruthless. Output a numbered list of concrete problems, severity (HIGH/MED/LOW), \
   and the smallest reproducible scenario for each.

   <plan or diff here>" </dev/null 2>$OUT/log.txt
cat $OUT/out.md
```

### Plan / second-opinion review

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only -o $OUT/out.md \
  "Review the plan below as a senior engineer. \
   Output: (1) what's strong, (2) what's risky, (3) concrete suggested changes, \
   (4) verdict: SHIP / REVISE / RETHINK.

   <plan>" </dev/null 2>$OUT/log.txt
cat $OUT/out.md
```

### Subagent delegation (self-contained task)

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s workspace-write \
  -C /path/to/repo -o $OUT/out.md \
  "Task: <one-line goal>.
   Inputs: <files/paths/data>.
   Constraints: <style, deps, must-not-touch>.
   Deliverable: <exact output format: files edited in place, patch on stdout, JSON, etc.>.
   Apply edits directly. Do not ask for confirmation." </dev/null 2>$OUT/log.txt
cat $OUT/out.md
```

Long jobs run in the background and are read whole when done:

```bash
OUT=$(mktemp -d)
codex exec ... -o $OUT/out.md "<prompt>" </dev/null 2>$OUT/log.txt &
CODEX_PID=$!
# ... continue other work ...
wait "$CODEX_PID"; cat $OUT/out.md
```

Mechanical bulk work (renames, fixture generation, many small edits) is the case for `-m gpt-5.4-mini -c model_reasoning_effort=low`.

### Code review on a diff

Built-in review of a scope, with Codex's own review prompt (findings come back prioritized `[P1]`, `[P2]`, ... with `file:line` references on stdout):

```bash
OUT=$(mktemp -d)
codex review --base main -c sandbox_mode=read-only </dev/null 2>$OUT/log.txt
codex review --uncommitted -c sandbox_mode=read-only </dev/null 2>$OUT/log.txt
codex review --commit <sha> -c sandbox_mode=read-only </dev/null 2>$OUT/log.txt
```

Review with your own instructions (no scope flag allowed alongside a prompt, so feed the diff yourself):

```bash
OUT=$(mktemp -d)
{ printf '%s\n\n' "Review this diff for: (1) correctness bugs, (2) security issues, \
(3) style / consistency, (4) missing tests. For each finding: file:line, severity, why, suggested fix."
  git diff main...HEAD; } > $OUT/prompt.md
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only -o $OUT/out.md - < $OUT/prompt.md 2>$OUT/log.txt
cat $OUT/out.md
```

For findings you will parse, add `--output-schema $OUT/findings.schema.json`.

### General consult / Q&A with follow-up

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only -o $OUT/out.md "<question>" </dev/null 2>$OUT/log.txt
SID=$(grep -o 'session id: .*' $OUT/log.txt | awk '{print $3}')
codex exec resume --skip-git-repo-check -c approval_policy=never -c sandbox_mode=read-only "$SID" "<follow-up>" </dev/null 2>$OUT/log2.txt
```

Do not add `--ephemeral` to a run you may want to resume.

### Codebase research

```bash
OUT=$(mktemp -d)
codex exec --skip-git-repo-check --color never -c approval_policy=never -s read-only -C /path/to/repo -o $OUT/out.md \
  "Investigate the codebase at the working root. \
   Answer: <specific question>. \
   Cite file paths and line numbers in the answer." </dev/null 2>$OUT/log.txt
cat $OUT/out.md
```

## Standard Integration Workflow

The Generate → Review → Fix loop:

```bash
OUT=$(mktemp -d)
# 1. Generate (you write the code)
# 2. Independent review by Codex
codex review --uncommitted -c sandbox_mode=read-only </dev/null 2>$OUT/log.txt
# 3. Apply the fixes yourself, or delegate them back:
codex exec --skip-git-repo-check --color never -c approval_policy=never -s workspace-write \
  -o $OUT/out.md "Fix these issues in <file>: <list>. Apply edits directly. Do not ask for confirmation." \
  </dev/null 2>$OUT/log.txt
```

Always validate Codex output before trusting it: read the changed files, run tests / type-check / lint, and verify the change matches the original intent.

## Error Handling

- **"Not inside a trusted directory and --skip-git-repo-check was not specified."** Add the flag, or `-C` into a git repository.
- **"the argument '--uncommitted' cannot be used with '[PROMPT]'"** Drop the prompt (use Codex's built-in review) or drop the scope flag and feed the diff through `codex exec`.
- **"unexpected argument '-m' found"** from `codex review`: use `-c model=<id>`.
- **The final message is a question.** The prompt was underspecified. Rewrite with explicit goal, inputs, constraints, output format, and "do not ask for confirmation".
- **Auth / config issues.** `codex doctor` reports installation, config, auth, and runtime health without prompting; surface failures to the user, do not silently retry.
- **Unknown model.** Drop `-m` to use the configured default.

## Plugins and Updates

`codex plugin ...`, `codex login`, `codex update`, `codex mcp ...`. These may prompt or open a browser; hand them to the user rather than running them from a script.

## See Also

- `references/reference.md`: full flag and subcommand reference, with examples.
- The `cli-for-agents` skill: how to run any CLI non-interactively and read its complete output.
- The `antigravity` skill: the same playbooks against the Gemini model family.
