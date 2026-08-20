# Release-note Task

## Release-note task

Decide whether the change needs a release note, and if so, write exactly one English release note entry.

## How to read the input

- `formatted_release_note_from_excel` might be empty, `None`, or a generic placeholder. Treat those values as no usable draft. When it contains a real draft written by the PR author, preserve its user-facing intent, but verify it against the PR code changes and issue description, correct inaccurate wording, and apply all style rules below.
- `fetch_failed_urls` lists links whose GitHub data could not be fetched. When non-empty, rely on the available Excel fields and GitHub context, and set `needs_review` to `true`.
- `files_summary` might end with `...[patch truncated]`. That is expected; judge from the visible portion.

## Classification

Write a release note when the change is visible to TiDB users or operators, including:

- Bug fixes that change query results, upgrade behavior, privilege checks, error messages, or compatibility.
- New features, new SQL syntax or function support, or new configuration options.
- Meaningful performance improvements observable in common operations.
- Behavior changes that affect upgrade paths, tooling integration, or operational workflows.
- Default value changes for system variables or configuration parameters.

Return a no-release-note verdict for internal-only changes, including:

- Test-only changes, flaky test fixes, or test infrastructure updates.
- Pure refactors or internal data-structure changes with no user-observable effect.
- Internal debug or log changes that do not surface in user-facing interfaces.
- CI/CD pipeline or developer workflow changes.
- Code comments or source-code-only documentation changes.

If a PR is mostly internal but the outcome is user-visible, describe the outcome and omit implementation details. If the only user-facing effect is indirect or speculative, lean toward `not_needed`.

First, use all available context to decide whether the change needs a release note. If it does, classify it as follows:

- When `issue_type_from_excel` is non-empty, use it as the primary basis for choosing between `bug_fix` and `improvement`. Map values containing `bug` or `fix` to `bug_fix`, and values containing `improvement` or `enhancement` to `improvement`, case-insensitively. Use the issue, PR, changed-file summary, and Excel draft only as supporting context for understanding the user impact and writing an accurate entry. Do not override a type that maps clearly from `issue_type_from_excel` merely because the other context could support another classification.
- When `issue_type_from_excel` is empty, determine the type from all available context. Use `bug_fix` for a correction to broken, incorrect, or unexpected existing behavior. Use `improvement` for a new capability or an optimization, enhancement, or other beneficial change that does not correct a defect.
- When a non-empty `issue_type_from_excel` does not map clearly to either type, interpret that value first and use the other context only to resolve the ambiguity. Set `needs_review` to `true` if the type remains uncertain.

## Writing style

- Write from the user's perspective, clearly and concisely, in English.
- Do not end the entry with a period.
- Do not expose internal function names unless they are user-visible behavior. Rewrite implementation details into observable behavior.
- Put SQL functions in backticks in ALL CAPS with parentheses, such as `` `DATE()` ``. Put SQL keywords in backticks in ALL CAPS, such as `` `HAVING` ``.
- Normalize product names to their official capitalization: TiDB, TiKV, TiCDC, TiFlash, PD, BR, DM, TiDB Lightning, Dumpling, and TiUP.
- Use only the provided Contributors list for attribution. Ignore `author` fields inside `pull_requests[]`, which might contain bot accounts from cherry-pick workflows.
- End the entry with exactly the provided Expected links, rendered as `[#<number>](<full-url>)`, followed by the provided contributors rendered as `@[user](https://github.com/user)`. Do not invent, drop, or reorder links or contributors.
- Output exactly one entry. Do not output section headings, component groups, or multiple bullets.
- If the available context is insufficient, draft the best note and set `needs_review` to `true`.

### Improvements style

Lead with an action verb and state the user benefit in terms of performance, stability, or capability. Common opening verbs include `Support`, `Add`, `Optimize`, `Improve`, `Avoid`, `Enhance`, `Mitigate`, `Accelerate`, `Remove`, and `Increase`.

Examples:

```text
- Improve the MySQL compatibility of expression default values displayed in the output of `SHOW CREATE TABLE` [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
- Support adding multiple indexes concurrently in the ingest mode [#52596](https://github.com/pingcap/tidb/issues/52596) @[lance6716](https://github.com/lance6716)
```

### Bug fixes style

Focus bug-fix entries on user-visible symptoms or error messages, trigger conditions, and impact, and avoid including internal implementation details unless they are necessary to explain the user-visible behavior.

Lead with a fix verb phrase. Accepted patterns include:

- `Fix the issue that [subject] [verb phrase]`.
- `Fix the issue of [noun phrase] that occurs when/during [condition]`.
- `Fix the [incorrect/inaccurate] [noun]`.
- `Fix a [rare/potential] issue that [description]`.
- `Fix the potential/occasional [panic/crash] that occurs when [condition]`.
- `Fix the panic issue caused by [X]`.

Include the trigger condition and observed impact when available. For non-deterministic failures, use `might` as a modal verb or `potential` as an adjective. Do not use `may` or `could`. Use `that`, not `where`, after `Fix the issue`.

Examples:

```text
- Fix the issue that executing SQL statements containing tables with multi-valued indexes might return the `Can't find a proper physical plan for this query` error [#49438](https://github.com/pingcap/tidb/issues/49438) @[qw4990](https://github.com/qw4990)
- Fix the issue that TiDB might crash when `tidb_mem_quota_analyze` is enabled and the memory used by updating statistics exceeds the limit [#52601](https://github.com/pingcap/tidb/issues/52601) @[hawkingrei](https://github.com/hawkingrei)
```

## Required output fields

- `type`: `"improvement"`, `"bug_fix"`, or `"not_needed"`.
- `release_note`: the formatted entry.
- `needs_review`: `true` or `false`.
- `reason`: a short English reason for the type and wording.

For `improvement` or `bug_fix`, `release_note` must be one Markdown bullet:

```text
- <description> <expected links> <contributors>
```

For `not_needed`, `release_note` must start with:

```text
Release note is not needed: <short reason>
```
