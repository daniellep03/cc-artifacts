# PR Readiness Checker — Subagent

## Role

This subagent inspects a feature branch and produces a structured go/no-go report before a pull request is opened. It checks for debug artifacts, incomplete work, untested changes, weak commit messages, risky file modifications, and merge conflict markers. The output is a Markdown report with a clear verdict — **READY**, **NEEDS WORK**, or **BLOCKED** — and a prioritized list of findings.

## When to dispatch this subagent

Dispatch this subagent when:

- A developer signals a branch is ready for review ("this is done, can you check it?").
- You are about to run `gh pr create` and want a pre-flight check.
- You are orchestrating multiple branch reviews in parallel — each branch gets its own subagent instance dispatched simultaneously so the agentic loop can collect all reports without serializing the work.
- A CI gate failed and you want a quick human-readable summary of what looks wrong before digging into logs.

Do **not** dispatch this subagent on branches that have already been merged or on detached HEAD states — it needs a named branch with an `origin/HEAD` or base ref to compute the diff.

## How it fits into an agentic loop

The parent Claude instance dispatches this subagent via the Agent tool, passing the branch name or letting the subagent detect it from `git branch --show-current`. The subagent runs in an isolated execution context: it reads git history and file contents but does not write, commit, or push anything. When the subagent finishes, it returns its Markdown report as a single message back to the parent, which can then act on the verdict — opening the PR, posting a comment, or surfacing blockers to the user.

Because each subagent execution is stateless and read-only, multiple instances can be dispatched in parallel across different branches without interference.

## Expected output

A Markdown report with this structure:

```
# PR Readiness Report — <branch name>

## Verdict: READY | NEEDS WORK | BLOCKED

**Summary:** one sentence.

## Blockers (must fix before merge)
## Warnings (should fix, not blocking)
## Informational
## Stats
```

**BLOCKED** means at least one finding must be resolved before the PR is safe to open (e.g., a leftover conflict marker or a debug `pdb.set_trace`).  
**NEEDS WORK** means the branch can technically be reviewed but has issues the author should address (e.g., a commit message that is just "fix").  
**READY** means the subagent found nothing actionable.

## Example dispatch

```
Agent({
  subagent_type: "pr-readiness-checker",
  description: "Pre-flight check on feature/payments-refactor",
  prompt: "Check branch feature/payments-refactor against main and produce a readiness report."
})
```

For parallel review of multiple branches, send multiple Agent tool calls in a single message — the agentic loop dispatches all subagents concurrently and waits for all results before proceeding.
