# resume-fit

**Type:** Claude Code skill
**Invoke with:** `/resume-fit`

---

## What it does

`resume-fit` is a skill that runs a complete job-application preparation pass
in a single invocation. It takes a job description and your resume as inputs,
then produces three sequential outputs without requiring you to manually
re-prompt between steps:

1. **ATS red-flag audit** — catches formatting issues that cause Applicant
   Tracking Systems to misparse resumes (tables, non-standard headings, icons
   used as data, etc.)
2. **Keyword gap analysis** — extracts the top keywords from the JD, checks
   which ones appear in your resume, scores coverage as a percentage, and
   suggests specific bullets to add for the highest-priority gaps.
3. **Cover letter outline** — produces a role-specific, bulleted outline
   structured around your strongest match, a keyword bridge for missing terms,
   and a company-fit signal pulled from the JD itself.

All three phases are delivered in one pass, ending with a 5-item action
checklist.

---

## When to invoke it

Invoke `/resume-fit` every time you start an application for a new role —
before you finalize your resume or write a single word of your cover letter.
The value compounds: each application teaches you which keywords your resume
habitually lacks, so you can make durable edits rather than one-off patches.

Do **not** invoke it to generate a finished cover letter. The skill
deliberately produces an outline, not prose, to keep your voice in the final
document.

---

## Why a skill and not a plain prompt

Claude Code **skills** are reusable instruction sets that Claude loads into the
agentic loop as structured context. Unlike typing a long prompt each time, a
skill:

- **Context injection** — when you invoke `/resume-fit`, Claude Code loads the
  skill's full instruction set into the context window automatically. This is
  context injection: the harness injects structured instructions so you never
  have to type or paste them yourself.
- **Persists across sessions** — the injected context is identical every time,
  so the analysis is reproducible regardless of what else is in the
  conversation.
- **Enforces a consistent workflow** — the skill's markdown body defines the
  exact sequence of analysis phases, so Claude does not skip or reorder steps
  depending on how the user words their request.
- **Supports progressive disclosure** — the skill collects missing inputs
  (JD text, resume file path) before beginning analysis rather than failing
  mid-run, keeping the agentic loop from stalling on an ambiguous state.
- **Composes with other tools** — because the skill declares `Read` in its
  `tools` list, Claude can read a resume file from disk directly when the user
  provides a path, without the user needing to copy-paste the content.

This is the difference between a skill and a hook: a **hook** is a shell
command that fires automatically in response to a Claude Code event (e.g.,
after every file save). A skill is a user-invoked instruction set that shapes
how Claude reasons through a task. `resume-fit` is a skill because it requires
user input and judgment at invocation time — it is not a side-effect of
another action.

---

## Inputs

| Input | How to provide |
|---|---|
| Job description | Paste the full text when prompted, or include it in your invocation message |
| Resume | Paste text directly, or give a file path (e.g. `~/Documents/resume.docx`) |

---

## Example invocation

```
/resume-fit

Here is the JD: [paste]
My resume is at ~/Documents/danielle_resume.pdf
```

Claude will read the file, run the ATS audit, produce the keyword gap table,
and deliver a tailored cover letter outline — no additional prompts needed.

---

## Demonstration

See [`demo.md`](demo.md) for a transcript of the skill running against a real
job description and resume excerpt.
