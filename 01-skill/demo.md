# Demo — `/resume-fit` transcript

The following is an edited transcript of the skill running against a real job
description (Data Analyst role at a mid-size SaaS company) and a resume
excerpt. Filler tokens and the resume text itself are abbreviated for
readability; the structure and outputs are authentic.

---

## Invocation

```
> /resume-fit

JD: [paste of 400-word job description for "Data Analyst, Growth" at Acme SaaS]
Resume: ~/Documents/danielle_resume.docx
```

---

## Claude's response

Reading resume from `~/Documents/danielle_resume.docx`…

---

### ATS Audit

- **Two-column layout in the Skills section** — ATS parsers often read
  multi-column blocks left-to-right across both columns, scrambling the text.
  Fix: flatten to a single-column bulleted list.
- **"About Me" section heading** — non-standard; parsers may skip it or
  misclassify it. Fix: rename to "Summary" or "Professional Summary."
- **Contact info in the document header** — Microsoft Word headers are
  frequently dropped by ATS imports. Fix: move name, email, phone, and
  LinkedIn URL into the body of page 1.
- **Skill ratings shown as filled/unfilled circles** — these are images; the
  underlying proficiency level is invisible to a parser. Fix: replace with
  text (e.g., "Python — 4 years professional experience").

No graphics or tables detected in body sections. Date formats are consistent
(Month YYYY). No certification logos found.

---

### Keyword Gap Analysis

Top keywords extracted from JD:

| JD Keyword | Found in Resume? |
|---|---|
| SQL | Yes |
| Python | Yes |
| Tableau | No |
| A/B testing | Partial ("experimentation") |
| Data pipeline | No |
| dbt | No |
| Looker | No |
| KPI dashboards | No |
| Cohort analysis | No |
| Stakeholder communication | Yes |
| Excel / Google Sheets | Yes |
| Growth metrics | Partial ("engagement metrics") |
| ETL | No |
| Statistical modeling | No |
| Product analytics | No |

**Coverage score: 5 of 15 keywords present (33%)**

**Top 5 missing keywords — suggested additions:**

1. **Tableau / Looker** — add to Skills section: "Data visualization: Tableau,
   Looker (self-directed learning, 2024)"
2. **dbt** — if you have any dbt exposure, add: "Built dbt models to transform
   raw event data for downstream reporting."
3. **Cohort analysis** — "Performed cohort retention analysis in Python
   (pandas) to identify 30-day drop-off patterns."
4. **ETL** — "Designed lightweight ETL scripts to ingest CSV exports into a
   PostgreSQL staging schema."
5. **A/B testing** — strengthen existing bullet: "Designed and analyzed A/B
   tests across email campaigns, reporting lift and statistical significance to
   product stakeholders."

---

### Cover Letter Outline

**Opening paragraph**
- Acme's stated focus on "data-informed growth loops" (JD language) mirrors
  the work I've done building retention dashboards for subscription products.
- Applying for Data Analyst, Growth — excited to bring SQL + Python depth to
  a team that ships decisions, not just reports.

**Body paragraph 1 — Strongest match**
- Led end-to-end analysis for a churn reduction initiative: queried 18 months
  of event data, built a cohort model, surfaced a 12% retention gap in the
  onboarding week, and co-owned the resulting product change.
- Result: 8-point improvement in 30-day retention over the following quarter.

**Body paragraph 2 — Keyword bridge**
- Actively building Tableau and dbt skills (reference personal project or
  coursework here) — can ramp quickly given existing Python/SQL foundation.
- Familiar with A/B testing frameworks from email optimization work; eager to
  apply rigorous experimentation discipline to product-level growth decisions.

**Body paragraph 3 — Culture/fit signal**
- The JD mentions "analysts who write product specs, not just decks" — that
  matches how I prefer to work: I include a recommended action and owner in
  every analysis deliverable.

**Closing paragraph**
- Would welcome the chance to discuss how my background in retention analytics
  translates to Acme's Growth team goals. Available for a call any time next
  week.

---

### Action Checklist

1. Fix the 4 ATS issues identified above before saving the final PDF.
2. Add the 5 keyword bullets to relevant experience and skills sections.
3. Expand the cover letter outline into full prose (keep it under 350 words).
4. Update the resume headline to match: "Data Analyst — Growth & Retention."
5. Export resume as an ATS-safe PDF (not a Canva or Figma export).

---

*Total elapsed time: ~35 seconds. No additional prompts were needed after the
initial invocation.*
