#!/usr/bin/env bash
# Read-only worktree prune audit. Classifies every git worktree by size, merge
# state, uncommitted work, remote/PR state, and the most recent chat that
# operated in it. Emits a table sorted by size with a suggested bucket. Never
# deletes anything; deletion stays a human-gated step in the playbook.
#
# Usage: worktree-audit.sh [repo-path]   (defaults to the current repo)
set -u

repo="${1:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -z "$repo" ] && { echo "not in a git repo; pass a repo path" >&2; exit 1; }
cd "$repo" || exit 1

# Main worktree is the first entry; everything else is a candidate.
main_wt=$(git worktree list --porcelain | awk '/^worktree /{print $2; exit}')
candidates=$(git worktree list --porcelain | awk -v main="$main_wt" '/^worktree / && $2 != main {print $2}')

# origin/main drives the merge check. Best-effort; stale is fine for a first pass.
git fetch origin main --quiet 2>/dev/null || echo "warn: could not fetch origin/main; merged column may be stale" >&2

# PR state by branch, fetched once. Empty if gh is unavailable.
prs=$(mktemp)
gh pr list --author "@me" --state all --limit 1000 \
	--json number,state,headRefName 2>/dev/null > "$prs" || echo "[]" > "$prs"

# Transcript dirs, one per harness (see rigorous-mode/references/harness.md):
#   Cursor      ~/.cursor/projects/<path minus leading slash, / -> ->/agent-transcripts
#   Claude Code ~/.claude/projects/<path with / -> -, leading dash kept>
#   Codex       ~/.codex/sessions (all workspaces; the path match narrows it)
cursor_slug=$(printf '%s' "$main_wt" | sed 's#^/##; s#/#-#g')
claude_slug=$(printf '%s' "$main_wt" | sed 's#/#-#g')
transcripts=()
for d in "$HOME/.cursor/projects/$cursor_slug/agent-transcripts" \
	"$HOME/.claude/projects/$claude_slug" \
	"$HOME/.codex/sessions"; do
	[ -d "$d" ] && transcripts+=("$d")
done

# One pass over the transcripts for every candidate at once: newest mtime of a
# transcript that mentions each worktree path (followed by "/" or a quote so
# glint-482 does not match glint-482-r37). Output: "<epoch>\t<worktree>".
last_chat=$(mktemp)
if [ ${#transcripts[@]} -gt 0 ] && [ -n "$candidates" ]; then
	patterns=()
	while read -r wt; do patterns+=(-e "${wt}/" -e "${wt}\""); done <<< "$candidates"
	rg -l --no-messages "${patterns[@]}" "${transcripts[@]}" 2>/dev/null \
		| xargs stat -f '%m %N' 2>/dev/null \
		| while read -r mtime file; do
			while read -r wt; do
				grep -q -e "${wt}/" -e "${wt}\"" "$file" 2>/dev/null && printf '%s\t%s\n' "$mtime" "$wt"
			done <<< "$candidates"
		done | sort -rn | awk -F'\t' '!seen[$2]++' > "$last_chat"
fi

now=$(date +%s)

printf "SIZE\tAGE\tMERGED\tDIRTY\tREMOTE\tPR\tLAST_CHAT\tBUCKET\tWORKTREE\n"

while read -r wt; do
	[ -n "$wt" ] || continue
	size=$(du -sh "$wt" 2>/dev/null | awk '{print $1}')
	read -r head head_ts < <(git -C "$wt" log -1 --format='%H %ct' HEAD 2>/dev/null || echo "- 0")
	age=$([ "$head_ts" -gt 0 ] 2>/dev/null && echo "$(( (now - head_ts) / 86400 ))d" || echo "?")

	# Squash-merged branches are not ancestors of main, so PR state is the
	# real signal; merge-base only catches fast-forward/rebase merges.
	git merge-base --is-ancestor "$head" origin/main 2>/dev/null && merged=YES || merged=no

	# Distinguish real WIP (tracked edits) from disposable untracked scratch.
	read -r wip scratch < <(git -C "$wt" status --porcelain 2>/dev/null \
		| awk '/^\?\?/{s++; next} {w++} END{print w+0, s+0}')
	if [ "$wip" -gt 0 ]; then dirty="wip:$wip"
	elif [ "$scratch" -gt 0 ]; then dirty="scratch:$scratch"
	else dirty=clean; fi

	branch=$(git -C "$wt" symbolic-ref --quiet --short HEAD 2>/dev/null || echo "")
	if [ -z "$branch" ]; then remote=detached
	elif ahead=$(git -C "$wt" rev-list --count "origin/$branch..HEAD" 2>/dev/null); then
		[ "$ahead" = 0 ] && remote=pushed || remote="ahead$ahead"
	else remote=no-remote; fi

	pr=$([ -n "$branch" ] && jq -r --arg b "$branch" \
		'.[] | select(.headRefName==$b) | "#\(.number)/\(.state)"' "$prs" 2>/dev/null | head -1)
	[ -z "$pr" ] && pr="-"

	last_ts=$(awk -F'\t' -v wt="$wt" '$2==wt{print $1; exit}' "$last_chat")
	last=$([ -n "$last_ts" ] && date -r "$last_ts" '+%Y-%m-%d' 2>/dev/null || echo "-")

	if [[ $dirty == wip:* ]]; then bucket=hold-wip
	elif [[ $pr == *OPEN* ]]; then bucket=hold-open-pr
	elif [ -n "$last_ts" ] && [ $(( (now - last_ts) / 86400 )) -le 4 ]; then bucket=verify-recent-chat
	elif [ "$merged" = YES ] || [ "$pr" != "-" ]; then bucket=safe
	else bucket=review; fi

	printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
		"$size" "$age" "$merged" "$dirty" "$remote" "$pr" "$last" "$bucket" "$wt"
done <<< "$candidates" | sort -t$'\t' -k1,1 -rh

rm -f "$prs" "$last_chat"
