# Model roles

pstack assigns work to roles, not to fixed models. Each skill names the role it needs (`how explorer`, `interrogate reviewers`, `swarm workers`, and so on). The role resolves to a model in three steps.

1. A line for the role in your harness's section of `~/.agents/pstack/models.md`, written by `/setup-pstack` (format below). Read the file with your file tool when it exists.
2. Otherwise the default for your harness in the table below.
3. A value of `inherit-parent` or `auto` means run the role on the parent chat's model and omit any per-spawn model parameter.

Panel roles (`how critics`, `arena runners`, `arena cross-judge pool`, `architect runners`, `interrogate reviewers`) are lists. One subagent runs per entry, alias entries included, so the list length sets the fan-out.

## Config file format

`~/.agents/pstack/models.md`, one line per role, `role: value` or `role: value, value, ...`. Delete a line to fall back to the default. Comments start with `#`.

Model identifiers differ per harness (Cursor slugs, Claude Code aliases, nothing on Codex), so the file is split into `## cursor`, `## claude-code`, and `## codex` sections. Read only your harness's section; lines outside any section are ignored.

```
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model.

## cursor
feature, refactoring: <model>
bug-fix: <model>
perf-issue: <model>
hillclimb: <model>
judgment and prose: <model>
hardest tasks: <model>
how explorer: <model>
how explainer: <model>
how critics: <model>, <model>, <model>, <model>
why investigators: <model>
why synthesizer: <model>
reflect tooling: <model>
reflect judgment, divergent, synthesizer: <model>
arena runners: <model>, <model>, <model>, <model>
arena cross-judge pool: <model>, <model>, <model>, <model>
swarm workers: <model>
architect runners: <model>, <model>, <model>, <model>
interrogate reviewers: <model>, <model>, <model>, <model>

## claude-code
feature, refactoring: <alias>

## codex
# nothing to set: every role is inherit-parent
```

## Defaults per harness

Values are whatever identifier the harness's spawn tool accepts. Cursor takes full slugs. Claude Code takes the aliases `sonnet`, `opus`, `haiku`, and `fable`. Codex has no per-spawn model, so every role is `inherit-parent` and fan-out comes from prompt lenses.

| Role | Cursor | Claude Code | Codex CLI |
|---|---|---|---|
| feature, refactoring | `grok-4.6-fast-xhigh` | `sonnet` | `inherit-parent` |
| bug-fix | `gpt-5.6-sol-max` | `opus` | `inherit-parent` |
| perf-issue | `gpt-5.6-sol-max` | `opus` | `inherit-parent` |
| hillclimb | `gpt-5.6-sol-max` | `opus` | `inherit-parent` |
| judgment and prose | `claude-fable-5-thinking-max` | `fable` (`opus` where unavailable) | `inherit-parent` |
| hardest tasks | `claude-fable-5-thinking-max` | `fable` (`opus` where unavailable) | `inherit-parent` |
| how explorer | `grok-4.6-fast-xhigh` | `sonnet` | `inherit-parent` |
| how explainer | `claude-fable-5-thinking-max` | `opus` | `inherit-parent` |
| how critics | `claude-fable-5-thinking-max`, `gpt-5.6-sol-max`, `grok-4.6-fast-xhigh`, `claude-opus-5-thinking-xhigh` | `opus`, `sonnet`, `opus`, `sonnet` | `inherit-parent` x4 |
| why investigators | `grok-4.6-fast-xhigh` | `sonnet` | `inherit-parent` |
| why synthesizer | `claude-fable-5-thinking-max` | `opus` | `inherit-parent` |
| reflect tooling | `gpt-5.6-sol-max` | `sonnet` | `inherit-parent` |
| reflect judgment, divergent, synthesizer | `claude-fable-5-thinking-max` | `opus` | `inherit-parent` |
| arena runners | `claude-fable-5-thinking-max`, `gpt-5.6-sol-max`, `grok-4.6-fast-xhigh`, `claude-opus-5-thinking-xhigh` | `opus`, `sonnet`, `opus`, `sonnet` | `inherit-parent` x4 |
| arena cross-judge pool | same four | `opus`, `sonnet` | `inherit-parent` |
| swarm workers | `grok-4.6-fast-xhigh` | `sonnet` | `inherit-parent` |
| architect runners | same four | `opus`, `sonnet`, `opus`, `sonnet` | `inherit-parent` x4 |
| interrogate reviewers | same four | `opus`, `sonnet`, `opus`, `sonnet` | `inherit-parent` x4 |

## Tiering code delegates

Code delegates tier by difficulty. The hardest changes (cross-cutting design, gnarly concurrency, subtle algorithms) go to `hardest tasks` when the work needs judgment or the intent is vague, and to `bug-fix` (the strongest instruction-following model) when the work is a precisely specified sequence of steps. Trivial mechanical edits go to `feature, refactoring`.

## When only one model family is available

Several skills get their signal from model diversity: reviewers with different blind spots, a judge from a different family than the parent. Inside Claude Code or Codex every subagent is the same family. Keep the fan-out and replace family diversity with lens diversity.

- Give each panel member a distinct lens in its prompt: correctness, security and data safety, maintainability and code quality, performance and resource use. Name the lens in the reviewer's label.
- Where the harness supports a reasoning-effort setting, vary it across the panel.
- For a cross-family judge, spawn the judge with a different model size than the parent when possible, and state in the reply that the judge shared the parent's model family.
- A "second opinion from another family" can still be had by shelling out to another installed CLI (`codex exec`, `claude -p`, `cursor-agent`) with the same prompt. Offer it; do not require it.

Agreement across a same-family panel is weaker evidence than across families. Say so in the verdict.

## Unresolvable model

If the harness rejects a model identifier when you spawn, read the valid identifiers from the error, pick the closest equivalent (prefer the highest-reasoning tier of the same family), spawn with it, and open a separate PR to update the config or this table. Do not block the task on the identifier. Never treat `inherit-parent` or `auto` as broken identifiers.
