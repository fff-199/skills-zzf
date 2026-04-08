# Chinese Word Report Checklist

## 1. Structure

- Start with conclusion and decision context, then move to assumptions, quantitative basis, route comparison, cases, and next steps.
- Group content by user decision path, not by collection source.
- Merge “route comparison” and “2D/layout explanation” when they explain the same decision.
- Put supporting cases after the route they support, not in isolated appendices unless the user wants a data-heavy backup section.

## 2. Tone

- Write as a formal upward-reporting document.
- Prefer phrases like `本报告认为`, `当前认识`, `下一步工作`, `供决策参考`.
- Avoid overly conversational or self-referential phrasing.
- Avoid “东一个西一个”的跳跃叙述; each section should answer one clear question.

## 3. Evidence Handling

- Separate:
  - direct material/process evidence
  - engineering route analogy
  - supplier capability reference
- For enclosed belt / pipe conveyor discussions, say explicitly whether the case proves:
  - exact powder handling
  - enclosed route feasibility
  - long-distance / complex terrain implementation

## 4. Images

- Use images to support a point, not to prove that a webpage exists.
- Prefer:
  - original case image
  - cropped useful image
  - one-image-one-paragraph explanation
- If a supplier's page has high learning value, keep one separate learning board page instead of spreading many messy screenshots everywhere.
- Do not let tiny unreadable screenshots occupy a full page.

## 5. Pagination

- Remove manual page breaks unless they are intentional chapter boundaries.
- Delete redundant blank paragraphs.
- Reduce heading `space_before` / `space_after`.
- Avoid these defects:
  - a heading alone at page bottom
  - one sentence alone on a page
  - a large blank lower half before the next section starts
  - a figure label separated from the figure
  - a cut-off card or split image block

## 6. Tables

- Keep tables compact and decision-oriented.
- Merge low-value tables into surrounding text if they do not add decision value.
- If a figure already summarizes the point, do not repeat a weak table below it.
- Tables should answer a concrete question such as:
  - which route uses less land
  - which evidence is direct vs analogy
  - which supplier is worth prioritizing

## 7. Final QA

- Render full PDF and inspect page by page.
- Check at minimum:
  - cover
  - first summary section
  - transitions between major chapters
  - dense case pages
  - pages with large images or tables
- If the user has edited the file manually, preserve their useful changes and only tighten layout around them.
