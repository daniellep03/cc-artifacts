# Subagent Demonstration

## Setup

The following subagent dispatch was run against a sample repository with a branch `feature/add-tax-and-logging`. The branch added a new `apply_tax` function to `app.py`, introduced a `requirements.txt`, but left in debug artifacts, a TODO, commented-out code, and used non-descriptive commit messages. No test file was updated.

**Dispatch call (from parent Claude instance):**

```python
Agent({
  subagent_type: "pr-readiness-checker",
  description: "Pre-flight check on feature/add-tax-and-logging",
  prompt: "Check branch feature/add-tax-and-logging against main and produce a readiness report."
})
```

---

## Subagent Output

# PR Readiness Report — feature/add-tax-and-logging

## Verdict: BLOCKED

**Summary:** The branch contains an active debugger call and a TODO in production code, non-descriptive commit messages, untested new logic, and a dependency manifest change that warrants review.

---

## Blockers (must fix before merge)

- **`app.py:11` — Active debugger:** `pdb.set_trace()` is present in `apply_tax`. This will halt execution in any environment that runs the function.
- **`app.py:10` — TODO left in code:** `# TODO: handle tax-exempt items` indicates the function is not complete. Merging incomplete logic can silently break downstream consumers.

---

## Warnings (should fix, not blocking)

- **`app.py:13–18` — Commented-out code block:** Five consecutive commented lines (`old_tax` implementation) were added in this diff. Dead code in a PR obscures intent; remove or move to a separate branch.
- **Untested change:** `apply_tax` was added to `app.py` but `test_app.py` was not modified. The only test file in the repo does not cover the new function.
- **Commit `df02fe0` — Weak message:** Message is `"wip"` (3 characters). Commit messages must describe the change for future `git blame` and changelog generation.
- **`requirements.txt` modified:** A new dependency (`requests==2.31.0`) was introduced. Confirm this is intentional — `requests` is not referenced in any changed source file in this diff.

---

## Informational

- No merge conflict markers detected.
- No CI/CD config files changed.
- Largest file changed: `app.py` (+13 lines) — within normal size limits.

---

## Stats

| Metric | Value |
|---|---|
| Files changed | 2 |
| Lines added | +14 |
| Lines removed | -0 |
| Test files touched | 0 |
| Commits on branch | 1 |

---

## Interpretation

The parent Claude instance received this report as a single message return from the subagent's isolated execution context. Because the verdict is **BLOCKED**, the parent did not proceed to `gh pr create`. Instead it surfaced the two blockers to the developer and waited for confirmation before taking further action.
