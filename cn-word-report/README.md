# cn-word-report

Design, tighten, and polish Chinese report-style Word documents (.docx) for leadership, client, or internal review. Use when Codex needs to create or revise Chinese汇报稿/方案汇总/调研报告 with strong structure, integrated narrative, image-table-caption coherence, and tight pagination; especially when sections feel fragmented, cases are scattered, images are unclear, or large blank spaces appear between major sections.

## Portable Entry Point

- Start here if you are using this repository from a non-Codex agent.
- The original Codex-oriented source remains in `SKILL.md` for reference.
- Run bundled scripts relative to this folder, for example `./cn-word-report/scripts/...` from the repo root.

## Adapted Instructions

# Chinese Word Report

Use this skill for Chinese report-style `.docx` work where reading flow and page layout matter as much as the text.

## Workflow

1. Read the user's current `.docx` first.
   - Treat the user's latest edited file as the source of truth.
   - Preserve the user's wording choices unless they clearly damage clarity or consistency.
2. Render early.
   - Convert `docx -> pdf` with `soffice`.
   - Render key pages to images and inspect actual pagination before editing again.
3. Fix structure before wording.
   - Reorder sections by decision logic, not by source type.
   - Group “how to store”, “how to convey”, “case evidence”, and “current judgment” into a readable sequence.
4. Fix page rhythm before adding more content.
   - Remove unnecessary manual page breaks.
   - Tighten heading spacing and delete empty spacer paragraphs.
   - Avoid leaving a heading or one sentence stranded on a page.
5. Then refine evidence presentation.
   - Distinguish direct evidence from route analogy.
   - Prefer one useful image plus one short explanation over full-page raw web screenshots.
   - If dense reference material is valuable, keep a dedicated learning board page in addition to the single-image explanations.
6. Re-render and inspect again.
   - Check first for large blank areas, clipped images, split captions, and awkward section starts.
   - Only then polish wording.

## Layout Rules

- Keep cover pages separate, but do not force new pages between major sections unless the page is already full or the next section starts a new chapter cleanly.
- Tighten一级标题、二级标题、正文段距. Default to small, consistent spacing; do not use blank paragraphs as visual padding.
- Let major sections connect naturally. If page bottom still has usable space, continue with the next heading instead of forcing a new page.
- Treat charts, tables, and captions as one block. Do not leave the caption on one page and the figure on the next.
- Use A4 portrait consistently unless a special landscape page is truly necessary.
- Prefer compact tables with readable fonts over oversized tables that force awkward whitespace.

## Content Rules

- Write for upward reporting: direct, calm, and decision-oriented.
- Avoid scattered source-driven narration. Integrate cases into the argument they support.
- State evidence class explicitly when needed:
  - `direct evidence`: directly tied to the target material/process.
  - `route analogy`: proves engineering feasibility or route maturity, but not exact material equivalence.
- When discussing route options, bind each route to:
  - occupied area
  - building form
  - main equipment
  - evidence/case support
  - project implication

## Image Rules

- Do not rely on raw whole-page web screenshots when the useful content is only one section.
- Crop to the informative area or use original case images when available.
- For representative vendors or references such as SRON or 华电科工, use both:
  - single-image case cards for explanation
  - a dense “学习图版” page when the web page structure itself is worth learning

## Render Loop

- Prefer `python-docx` for edits.
- Use `soffice --headless --convert-to pdf` for layout review.
- Render pages to images and inspect visually before final delivery.
- If large blank space remains, first look for:
  - manual page breaks
  - blank paragraphs
  - oversized image widths
  - keep-with-next / keep-lines effects

## References

- Read [references/report-checklist.md](references/report-checklist.md) when you need the full checklist for structure, pagination, evidence integration, and final QA.

## Resource Map

### References
- `references/report-checklist.md`

## Source

- Original skill definition: `SKILL.md`
