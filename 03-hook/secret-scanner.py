#!/usr/bin/env python3
"""
PreToolUse hook — Secret Scanner

Reads the pending tool call from stdin (JSON), scans Bash commands and
file-write content for common secret patterns, and exits with code 2 to
block the tool if anything suspicious is found.
"""

import json
import re
import sys

# (label, compiled pattern)
SECRET_PATTERNS = [
    ("Anthropic API key",    re.compile(r"sk-ant-api\d{2}-[A-Za-z0-9_\-]{93}")),
    ("OpenAI API key",       re.compile(r"sk-[A-Za-z0-9]{48}")),
    ("AWS Access Key ID",    re.compile(r"AKIA[A-Z0-9]{16}")),
    ("GitHub token",         re.compile(r"gh[ps]_[A-Za-z0-9]{36}")),
    ("Slack token",          re.compile(r"xox[baprs]-[0-9A-Za-z\-]+")),
    ("Private key block",    re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("Hardcoded credential", re.compile(
        r'(?i)(?:password|passwd|secret|api[_\-]?key|token)\s*[:=]\s*["\']?[A-Za-z0-9+/]{24,}["\']?'
    )),
]


def scan(text: str) -> list[tuple[str, str]]:
    hits = []
    for label, pattern in SECRET_PATTERNS:
        m = pattern.search(text)
        if m:
            snippet = m.group(0)
            preview = snippet[:24] + "..." if len(snippet) > 24 else snippet
            hits.append((label, preview))
    return hits


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # malformed input — let the tool proceed

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name == "Bash":
        text = tool_input.get("command", "")
    elif tool_name == "Write":
        text = tool_input.get("content", "")
    elif tool_name == "Edit":
        text = tool_input.get("new_string", "")
    else:
        sys.exit(0)  # unrecognized tool — allow

    hits = scan(text)
    if not hits:
        sys.exit(0)

    print("SECRET SCANNER — tool call blocked", file=sys.stderr)
    print(f"Tool: {tool_name}", file=sys.stderr)
    print("Detected:", file=sys.stderr)
    for label, preview in hits:
        print(f"  • {label}: {preview}", file=sys.stderr)
    print(
        "\nRemove or rotate the secret before proceeding. "
        "Use environment variables or a secrets manager instead.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
