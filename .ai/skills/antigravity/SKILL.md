---
name: antigravity
description: Wield the Antigravity CLI (`agy`) as a powerful auxiliary AI agent for adversarial review, plan critique, subagent delegation, code review, second opinions, and general consult. Use when a task benefits from an independent AI perspective, when delegating a self-contained chunk of work, when stress-testing a plan or diff, or when the user explicitly requests Antigravity / `agy`.
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
---

# Antigravity CLI Integration Skill

This skill enables Claude Code to orchestrate the Antigravity CLI (`agy`) as an auxiliary AI agent — for adversarial review, plan critique, subagent delegation, code review, web/codebase research, and general consult.

Antigravity replaces the previous Gemini integration. Default to `agy` whenever an "outside opinion" or "delegated subagent" pattern would help.

## When to Use This Skill

### Ideal use cases

1. **Adversarial review (challenge mode)**
   - Try to break a proposed plan or diff
   - Find edge cases, race conditions, broken assumptions
   - Stress-test a design before implementation

2. **Plan / architecture review (second opinion)**
   - Independent critique of a plan written in this session
   - Sanity-check before committing to a direction
   - Get architectural feedback from a non-conversation-attached agent

3. **Subagent delegation**
   - Offload a self-contained task (code generation, refactor, doc pass) and use the result
   - Run long tasks in the background while continuing main work
   - Parallelize independent chunks

4. **Code review on diffs / files**
   - Independent review focusing on bugs, security, style
   - Pre-PR sweep before `/ship` or `/review`

5. **General consult / Q&A**
   - Ask `agy` anything where a second perspective is useful
   - Continue a previous `agy` conversation for back-and-forth

6. **Codebase research**
   - Hand `agy` a workspace dir and let it investigate
   - Useful when the answer requires reading many files

### When NOT to use

- Trivial tasks (overhead not worth it)
- Anything requiring tight loop / immediate streaming response
- When context is already fully loaded in this session and the answer is obvious
- Interactive multi-turn refinement that needs to stay inside this conversation

## Core Invocation Pattern

Antigravity is invoked as `agy`. The non-interactive workflow is:

```bash
agy --dangerously-skip-permissions -p "<prompt>" 2>&1
```

**Flag order matters.** Put boolean flags (`--dangerously-skip-permissions`, `--sandbox`) BEFORE `-p`, or put the prompt immediately after `-p` and other flags last:

```bash
# OK
agy --dangerously-skip-permissions -p "<prompt>"
agy -p "<prompt>" --dangerously-skip-permissions

# BROKEN — `-p` consumes the next arg as its prompt, so `-p --sandbox "<prompt>"`
# treats `--sandbox` as the prompt string and errors on `"<prompt>"` as a stray arg.
agy -p --sandbox "<prompt>"
```

Key flags (verified against `agy --help`):

| Flag | Purpose |
|---|---|
| `-p`, `--print`, `--prompt` | Run a single prompt non-interactively and print the response |
| `-i`, `--prompt-interactive` | Run an initial prompt, then continue interactively (avoid in scripted use) |
| `-c`, `--continue` | Continue the most recent conversation |
| `--conversation <id>` | Resume a specific previous conversation by ID |
| `--dangerously-skip-permissions` | Auto-approve all tool permission prompts (YOLO equivalent) |
| `--add-dir <path>` | Add a directory to `agy`'s workspace (repeatable) |
| `--sandbox` | Run in a sandbox with terminal restrictions |
| `--print-timeout <duration>` | Timeout for print mode wait (default `5m`) |
| `--log-file <path>` | Override CLI log file path |

Subcommands: `changelog`, `help`, `install`, `plugin` (alias `plugins`), `update`.

## Verifying Installation

Before first use in a session:

```bash
command -v agy && agy --version
```

If missing, surface that to the user — do not silently fall back.

## Critical Behavioral Notes

- **`--dangerously-skip-permissions` skips tool-permission prompts but does not suppress `agy`'s own clarifying questions.** When delegating, write prompts that leave no room for clarification — give the goal, the constraints, the inputs, and the desired output format explicitly.
- **Default timeout is 5 minutes.** For long jobs (refactors, large reviews), pass `--print-timeout 15m` (or longer) or run in the background.
- **`--print` returns plain text on stdout.** There is no built-in JSON output mode; if structured output is needed, instruct `agy` to emit JSON in the prompt itself.
- **Workspace scoping matters.** By default `agy` runs in the current working directory. To give it access to additional roots, use repeated `--add-dir` flags.
- **Conversation continuity:** use `-c` to continue the last conversation, or `--conversation <id>` for a specific one. Useful for multi-turn consult where the first reply needs follow-up.

## Mode Playbooks

### Adversarial review (challenge)

Frame the prompt as an attack: tell `agy` its job is to find flaws.

```bash
agy --dangerously-skip-permissions -p \
  "You are an adversarial reviewer. Your job is to break the following plan / diff. \
   Find edge cases, race conditions, security holes, broken assumptions, and missing tests. \
   Be ruthless. Output a numbered list of concrete problems, severity (HIGH/MED/LOW), \
   and the smallest reproducible scenario for each.

   <plan or diff here>" 2>&1
```

### Plan / second-opinion review

```bash
agy --dangerously-skip-permissions -p \
  "Review the plan below as a senior engineer. \
   Output: (1) what's strong, (2) what's risky, (3) concrete suggested changes, \
   (4) verdict: SHIP / REVISE / RETHINK.

   <plan>" 2>&1
```

### Subagent delegation (self-contained task)

```bash
agy --dangerously-skip-permissions -p --print-timeout 15m \
  "Task: <one-line goal>.
   Inputs: <files/paths/data>.
   Constraints: <style, deps, must-not-touch>.
   Deliverable: <exact output format — file contents, patch, JSON, etc.>.
   Apply edits directly. Do not ask for confirmation." 2>&1
```

Run long jobs in the background:

```bash
agy --dangerously-skip-permissions -p --print-timeout 30m "<prompt>" > /tmp/agy-out.txt 2>&1 &
```

Then monitor with `BashOutput` or `tail -f /tmp/agy-out.txt`.

### Code review on a diff

```bash
git diff <base>...HEAD > /tmp/diff.patch
agy --dangerously-skip-permissions -p \
  "Review this diff for: (1) correctness bugs, (2) security issues, \
   (3) style / consistency, (4) missing tests. \
   For each finding: file:line, severity, why, suggested fix.

   $(cat /tmp/diff.patch)" 2>&1
```

### General consult / Q&A with follow-up

```bash
# First turn
agy --dangerously-skip-permissions -p "<question>" 2>&1

# Follow-up on the most recent conversation
agy -c -p --dangerously-skip-permissions "<follow-up>" 2>&1
```

### Codebase research

```bash
agy --dangerously-skip-permissions -p --add-dir /path/to/repo --print-timeout 15m \
  "Investigate the codebase at the workspace root. \
   Answer: <specific question>. \
   Cite file paths and line numbers in the answer." 2>&1
```

## Standard Integration Workflow

The Generate → Review → Fix loop:

```bash
# 1. Generate (Claude writes the code)
# 2. Independent review by agy
agy --dangerously-skip-permissions -p \
  "Review <file> for bugs, security issues, and style. Be thorough." 2>&1

# 3. If agy flags real issues, Claude applies the fix — or delegates the fix back:
agy --dangerously-skip-permissions -p \
  "Fix these issues in <file>: <list>. Apply edits directly." 2>&1
```

Always validate `agy` output before trusting it: read the changed files, run tests / type-check / lint, and verify the change matches the original intent.

## Error Handling

- **Timeout** — raise with `--print-timeout 15m` (or longer) or background the job.
- **Auth / config issues** — run `agy --version` to confirm the CLI loads; surface failures to the user, do not silently retry.
- **Tool-permission prompts** — pass `--dangerously-skip-permissions` for non-interactive runs.
- **`agy` refuses or asks for clarification** — the prompt was underspecified. Rewrite with explicit goal, inputs, constraints, output format.

## Plugins and Updates

- List / install plugins: `agy plugin list`, `agy plugin install <target>`.
- Import from existing setups: `agy plugin import gemini` or `agy plugin import claude`.
- Update CLI: `agy update`.
- View changelog: `agy changelog`.

## See Also

- `references/reference.md` — full flag and subcommand reference, with examples.
