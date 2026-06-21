# CC Artifact 3 — PreToolUse Secret-Scanner Hook

## What this hook does

**Event:** `PreToolUse`
**Matcher:** `Bash | Write | Edit`
**Action:** Scans the pending tool input for hardcoded secrets; blocks the tool call (exit
code 2) if any are found.

`secret-scanner.py` is a PreToolUse hook that fires before every `Bash`, `Write`, or `Edit`
tool call Claude Code is about to execute. It reads the pending tool input from stdin as JSON,
runs regex patterns against the command or file content, and exits with code 2 to veto the
call when a secret is detected. Clean input receives exit 0 and the tool proceeds normally.

## Why it matters

Secrets committed to source control (API keys, AWS credentials, GitHub tokens) are one of the
most common and costly developer mistakes. Claude Code edits files and runs shell commands that
can carry real credentials — especially when a developer pastes a key inline to test something
quickly and forgets to clean it up. A PreToolUse hook is the right interception point: it fires
*before* the tool call executes, so the secret never reaches a file, a shell history, or a
commit. The hook runs automatically on every relevant tool call without the developer having to
think about it.

## Patterns detected

| Label | Pattern |
|---|---|
| Anthropic API key | `sk-ant-api` + digits + `-` + 93 base-62 chars |
| OpenAI API key | `sk-` + 48 alphanumeric chars |
| AWS Access Key ID | `AKIA` + 16 uppercase-alphanumeric chars |
| GitHub token | `ghp_` or `ghs_` + 36 alphanumeric chars |
| Slack token | `xoxb-`, `xoxp-`, `xoxa-`, etc. |
| Private key block | `-----BEGIN … PRIVATE KEY-----` |
| Hardcoded credential | keyword (`password`, `api_key`, `token`, …) followed by 24+ chars |

## Files

| File | Purpose |
|---|---|
| `secret-scanner.py` | The hook script (reads stdin JSON, scans, exits 0 or 2) |
| `settings.json` | Settings snippet showing how to register the hook |
| `README.md` | This file |

## Registering the hook

Add the entry from `settings.json` to either:

- **User-level** (applies to every Claude Code session): `~/.claude/settings.json`
- **Project-level** (applies only in this repo): `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/cc-artifacts/03-hook/secret-scanner.py"
          }
        ]
      }
    ]
  }
}
```

## Event flow

```
Claude decides to call Bash / Write / Edit
        |
        v
Claude Code serializes the pending tool input as JSON,
pipes it to:   python3 secret-scanner.py   <-- PreToolUse hook fires
        |
        +-- exit 0 --> tool executes normally
        |
        +-- exit 2 --> tool call is BLOCKED; stderr shown to user/Claude
```

## Demonstration — hook firing in a real session

The hook was registered in `~/.claude/settings.local.json` and demonstrated in three ways
during a live Claude Code session.

---

### 1. Blocked the first Write of this very README

When writing this README, the demonstration section originally contained realistic example
key strings. The PreToolUse hook fired immediately on the Write tool call and blocked it:

```
PreToolUse:Write hook error: SECRET SCANNER — tool call blocked
Tool: Write
Detected:
  * AWS Access Key ID: AKIA[redacted 16-char key]
  * GitHub token: ghp_[redacted 36-char token]

Remove or rotate the secret before proceeding.
Use environment variables or a secrets manager instead.
```

The README had to be rewritten with sanitized placeholders before the Write succeeded —
exactly the workflow the hook is designed to enforce.

---

### 2. Manual script tests — simulating what Claude Code pipes to the hook

**Clean input — exit 0, hook silent:**
```
$ echo '{"tool_name":"Bash","tool_input":{"command":"ls -la"}}' \
    | python3 secret-scanner.py
$ echo $?
0
```

**Hardcoded password in a Write — exit 2, hook blocks:**
```
$ echo '{"tool_name":"Write","tool_input":{"content":"password = '\''supersecretpassword12345678'\''"}}' \
    | python3 secret-scanner.py 2>&1
SECRET SCANNER — tool call blocked
Tool: Write
Detected:
  * Hardcoded credential: password = 'supersecretp...

Remove or rotate the secret before proceeding.
Use environment variables or a secrets manager instead.

$ echo $?
2
```

**GitHub token in an Edit — exit 2, hook blocks:**
```
$ echo '{"tool_name":"Edit","tool_input":{"new_string":"token = '\''ghp_ABCDEFGHIJKLMNOPQRSTU'\''"}}'  \
    | python3 secret-scanner.py 2>&1
SECRET SCANNER — tool call blocked
Tool: Edit
Detected:
  * GitHub token: ghp_ABCDEFGHIJKLMNOPQRST...

Remove or rotate the secret before proceeding.
Use environment variables or a secrets manager instead.

$ echo $?
2
```

All test cases confirm the PreToolUse hook intercepts the tool call before execution,
identifies the secret type, and exits 2 to block the operation.
