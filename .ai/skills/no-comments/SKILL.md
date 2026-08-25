---
name: no-comments
description: "Strip AI slop from a diff before commit, then spawn Comment Sicko before review, fix accepted findings, and offer encodings for claimed constraints. Use for /no-comments, 'strip the comments', 'deslop this', or before any commit or review."
disable-model-invocation: true
---

# No comments

Two passes over the same scope. The slop pass runs before each commit. The comment audit runs before review. Run both when invoked without a qualifier.

Authoring agents defend comments. Defer to Comment Sicko's fresh perspective.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

## Slop pass (before commit)

Remove AI-generated slop the branch introduced, keeping behavior unchanged unless fixing a clear bug. Prefer minimal, focused edits over broad rewrites.

- Comments that narrate, restate the code, or are inconsistent with local style.
- Defensive checks or try/catch blocks that are abnormal for trusted code paths.
- Casts to `any` (or the language's equivalent) used only to bypass type issues.
- Deeply nested code that early returns would flatten.
- Other patterns inconsistent with the file and the surrounding codebase.

Summarize the pass in one to three sentences.

## Comment audit (before review)

1. Spawn the `comment-sicko` agent (identifier form per `../rigorous-mode/references/harness.md`; when your harness cannot address a named agent, paste `agents/comment-sicko.md` into the worker's prompt). Pass the scope. Do not restate its rules.
2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on our-code surprises stay actionable. Do not restore those comments. A keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions stay actionable `MUST KILL`s. Restore deletions only with exact exceptions and scoped proof. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, run `/how` or `/why` on their symbol. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it. Revert and rerun one rejected report with the failure named. Reject a second, report it open, and fail `/no-comments`.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, run `/architect` once for the accepted set and surrounding code. Stop at the sketch. Architect shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The **principle-fix-root-causes** and **principle-redesign-from-first-principles** skills guide intent only: fix real causes, redesign as if requirements always existed, never bolt on symptom guards. Neither authorizes widening the fence nor fixing instances outside it.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Wait for interactive approval. Unattended and eval require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. Report the deletion count, restored comments, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.
