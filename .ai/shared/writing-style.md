# Writing Style

Use this guidance for authoring, editing, or reviewing Markdown in `pingcap/docs`.

## Overall principles

- Write for TiDB users, not for internal teams.
- Use a conversational and friendly tone, but do not sound casual, playful, or promotional.
- Prefer clear, direct, and practical language.
- Do not pre-announce what the document will do. Start with useful information directly.
- Write for a global audience. Avoid culture-specific references, vague shorthand, and region-specific assumptions.
- Write accessibly. Prefer simple sentence structures and wording that is easy to scan and understand.

## File naming rules

- Use file names that briefly describe the document content, for example, `destroy-tidb-cluster.md`.
- Keep file names concise and general. Avoid overly specific wording that might require frequent renaming and cause unnecessary URL changes.
- Except for special files such as `TOC.md`, `CONTRIBUTING.md`, and `README.md`, use lowercase letters only in file names.
- If a file name contains multiple English words, separate them with hyphens (`-`).
- Do not use underscores (`_`) in file names.
- Use lowercase file extensions only.
- Markdown files must use the `.md` extension.

## Language and grammar

- Use second person, such as `you` and `your`, instead of `we`.
- Use active voice whenever possible. Make it clear who performs the action.
- Put conditions before instructions, not after.
- Use standard American English spelling and punctuation.
- Use serial commas.
- Prefer concise and precise wording over decorative phrasing.
- Preserve technical meaning. Do not rewrite in ways that change product behavior or scope.

## Structure and organization

- Keep the structure easy to scan with meaningful headings and short paragraphs.
- Keep exactly one top-level heading per file.
- Do not skip heading levels.
- When frontmatter is present, keep the `title` aligned with the H1.
- Write a concise `summary` that tells the reader what they will learn or do.
- In `summary`, do not start with a special character such as `>`, `*`, `#`, `-`, or `[`. If the summary must begin with a special character, wrap the summary content in quotation marks.

## Choose the right document pattern

Use the existing templates in `resources/doc-templates/` as the primary shape guide.

- Task-style documents explain how to complete a procedure step by step.
- Reference-style documents explain commands, parameters, options, system variables, configuration items, or APIs.
- Use concept, troubleshooting, or new-feature templates when they better match the user task.

Match the document structure to the document type. Do not force a task flow into a reference document or a reference layout into a task document.

## Heading capitalization

Use capitalization consistently based on the file type and heading level:

- In TOC-related Markdown files, use title case for headings and navigation titles.
- In regular Markdown files, use title case for the frontmatter `title`.
- In regular Markdown files, use title case for the H1 heading.
- In regular Markdown files, use sentence case for all headings below H1.

Keep the frontmatter `title` and the H1 aligned in wording and capitalization.

## Instructions and lists

- Use numbered lists for sequences of actions or ordered procedures.
- Use bulleted lists for most other lists.
- Use description lists for pairs of related items, such as a term and its definition.
- In procedural content, make each step a clear action.
- Put prerequisites, conditions, and important context before the steps they affect.
- Keep lists parallel in grammar and structure.

## Links

- Use descriptive link text.
- Do not use vague link text such as `here`, `click here`, or `this page`.
- Preserve repository-relative absolute paths such as `/foo/bar.md` when that is the repository convention.
- Prefer linking to the most relevant destination instead of adding multiple redundant links nearby.

## Formatting conventions

- Put code-related text in code font, including commands, file names, directory names, configuration items, parameter names, field names, environment variables, and literal values.
- Put UI elements in bold.
- Preserve code samples, commands, UI strings, API fields, JSON keys, and configuration names unless they are factually wrong or the task explicitly requires changing them.
- Keep blank lines around headings, lists, and fenced code blocks.
- Indent nested list content with 4 spaces in normal Markdown files.
- Use unambiguous date formats when dates are necessary.
- Keep punctuation and capitalization consistent within lists, headings, and tables.

## Notes, warnings, and emphasis

- Use notes and warnings only when they help the reader make a decision, avoid risk, or prevent confusion.
- Do not overuse callouts for ordinary information.
- Make warnings specific and actionable.
- Do not use emphasis for decoration. Use it only when it improves clarity.

## Images

- Provide alt text for images.
- Use images only when they add value that text alone cannot provide.
- Keep screenshots and diagrams aligned with the current product behavior and UI text.

## Review lens

When reviewing or rewriting content, check these in order:

1. Is the content factually correct?
2. Is the logic complete and easy to follow?
3. Are other related documents also affected and likely to need updates?
4. Does the structure match the document type?
5. Does the wording improve clarity without changing product meaning?

Make feedback specific, actionable, and tied to the changed content. Avoid praise-only edits.
