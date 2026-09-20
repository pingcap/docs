# Writing Style

Use this guidance for authoring, editing, or reviewing Markdown in `pingcap/docs`.

## Overall principles

- Write for TiDB users, not for internal teams.
- Use a conversational and friendly tone, but do not sound playful or promotional.
- Prefer clear, direct, and practical language.
- When in doubt, favor clarity over cleverness.
- Rewrite content that might confuse a new user.
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
- Prefer present tense unless you are describing historical behavior.
- Correct English grammar, spelling, and punctuation errors.
- Put conditions before instructions, not after.
- Use standard American English spelling and punctuation.
- Use serial commas.
- Prefer concise and precise wording over decorative phrasing.
- Preserve technical meaning. Do not rewrite in ways that change product behavior or scope.

## Terminology and version notation

- Use terminology consistently. Do not use "database" and "instance" interchangeably. Choose the term that matches the actual product concept.
- Use "replicate" instead of "synchronize" when referring to replicating data from one TiDB cluster to another.
- Write MySQL versions as `MySQL 8.0`, `MySQL 8.4`, or `MySQL 8.x`. Do not add a `v` prefix. The `v` prefix is reserved for TiDB and TiDB tool versions, such as `TiDB v8.5` and `DM v2.0`.
- Follow the established terminology in `glossary.md` and `resources/terms.md`.

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

## Final checklist

Before finalizing authored, edited, or reviewed content, verify that:

- [ ] The content addresses a clear user need and is appropriate for its intended audience.
- [ ] Technical facts are accurate, and edits preserve the intended product behavior and scope.
- [ ] The structure matches the document type, and headings follow the required hierarchy and capitalization.
- [ ] Procedures present prerequisites and conditions before clear, actionable steps.
- [ ] Terminology, product names, and version notation are accurate and consistent.
- [ ] Commands, code, configuration names, API fields, UI strings, and literal values remain correct.
- [ ] Links, formatting, lists, notes, warnings, images, and alt text follow repository conventions.
- [ ] The language is clear, concise, grammatically correct, and easy for a global audience to understand.
- [ ] Related documents, TOC entries, aliases, or cross-references have been considered when applicable.
