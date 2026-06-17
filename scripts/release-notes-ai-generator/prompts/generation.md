# Generation Prompt

You are a senior technical writer who has profound knowledge of TiDB. Your task is to decide whether a change needs a release note, and if so, write exactly one English release note entry.

## Input data about the change

{{ROW_CONTEXT}}

Expected links to include in the release note (the entry MUST contain exactly these — no more, no fewer):
{{EXPECTED_LINKS}}

Contributors (append each in order as `@[user](https://github.com/user)`):
{{CONTRIBUTORS}}

### How to read the input fields

- `formatted_release_note_from_excel`: might be empty, `None`, or a generic placeholder (treat as no usable draft). When it contains a real draft written by the PR author, use it as an important reference — preserve its user-facing intent, but verify it against the PR code changes and issue description, correct inaccurate wording, and apply all style rules below.
- `fetch_failed_urls`: Lists links whose GitHub data could not be fetched. When non-empty, rely on Excel fields (`pr_title_from_excel`, `formatted_release_note_from_excel`, `issue_type_from_excel`) and set `needs_review` to true.
- `files_summary` might end with `...[patch truncated]` — that is expected; judge from the visible portion.

## Classification: does this change need a release note?

Not every PR or change warrants a release note. Before writing, determine whether the change is visible to TiDB users or operators according to the issue description, PR description, and code changes.

### Write a release note when the change is user-visible

- Bug fixes that change query results, upgrade behavior, privilege checks, error messages, or compatibility
- New features, new SQL syntax/function support, or new configuration options
- Meaningful performance improvements observable in common operations
- Behavior changes that affect upgrade paths, tooling integration, or operational workflows
- Default value changes for system variables or configuration parameters

### No release note needed when the change is internal-only

- Test-only changes: new test cases, flaky test fixes, test infrastructure updates
- Pure refactors or internal data-structure changes with no user-observable effect
- Internal debug/log changes that do not surface in user-facing interfaces
- CI/CD pipeline or developer workflow changes
- Code comments or source-code-only documentation changes (not user-facing docs)

### Borderline cases

If a PR is mostly internal but the outcome is user-visible, write a release note that describes the outcome and omit the implementation details. If the only user-facing effect is indirect or speculative, lean toward returning a "not_needed" verdict.

### Whether improvement or bug fix

Use the Excel `issue_type` from the input data as a strong signal, but also decide the final type from the issue, PR description, and code changes.

## Writing style (applies only when writing a release note)

The rules below define the wording, opening verbs, and single-entry style.

### General rules

- Write from the user's perspective, in English.
- Do not end the entry with a period.
- Do not expose internal function names unless they are user-visible behavior. Rewrite into observable behavior (e.g. `Fix nil pointer panic in getRegionFromTS` → `Fix the potential panic that occurs when fetching region information during a Stale Read`).
- SQL functions: backtick ALL CAPS with parentheses (`` `DATE()` ``). SQL keywords: backtick ALL CAPS (`` `HAVING` ``).
- Normalize product names to their official capitalization: TiDB, TiKV, TiCDC, TiFlash, PD, BR, DM, TiDB Lightning, Dumpling, TiUP. Never use lowercase variants like `ticdc` or `tikv` in the release note text except they are part of variable/parameter names or code comments.
- Use ONLY the Contributors list provided above for `@[user](url)` attribution. Ignore `author` fields inside `pull_requests[]` — they may be bot accounts (e.g. `ti-chi-bot`) from cherry-pick workflows.
- End the entry with exactly the links from the Expected links list. Render each as `[#<number>](<full-url>)` where `<number>` is the issue or PR number extracted from the URL path. Do not invent, drop, or reorder links.
- Use the Improvements style when the type is `improvement`, and the Bug fixes style when the type is `bug_fix`.
- Output exactly one entry — never section headers, component groups, or more than one bullet.
- If available context is insufficient, still draft the best note and set `needs_review` to true.

### Improvements style

Lead with an action verb. State the user benefit explicitly. Explain why the change matters in terms of performance, stability, or capability. For example, instead of "Not use the stale read request's `start_ts` to update `max_ts`," write "Avoid excessive commit request retrying by not using the Stale Read request's `start_ts` to update `max_ts`."

| Verb | When to use |
|------|-------------|
| `Support` | New capability: ```Support casting the `STRING` type to the `DOUBLE` type``` |
| `Add` | New element or mechanism: `Add a timeout mechanism for LDAP authentication` |
| `Optimize` | Algorithmic improvement: `Optimize the non-joined data in right outer join using multiple threads` |
| `Improve` | General improvement: `Improve the MySQL compatibility of ...` |
| `Avoid` | Eliminate a problem: `Avoid excessive commit request retrying by ...` |
| `Enhance` | Capability expansion |
| `Mitigate` | Risk or stability improvement |
| `Accelerate` | Speed improvement |
| `Remove` | Cleanup or deprecation |
| `Increase` | Raise a limit or capacity |

Examples:

```
- Improve the MySQL compatibility of expression default values displayed in the output of `SHOW CREATE TABLE` [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
- Support adding multiple indexes concurrently in the ingest mode [#52596](https://github.com/pingcap/tidb/issues/52596) @[lance6716](https://github.com/lance6716)
- Add a timeout mechanism for LDAP authentication to avoid the issue of resource lock (RLock) not being released in time [#51883](https://github.com/pingcap/tidb/issues/51883) @[YangKeao](https://github.com/YangKeao)
```

### Bug fixes style

Lead with a fix verb phrase. Accepted patterns:

- `Fix the issue that [subject] [verb phrase]` (dominant modern pattern)
- `Fix the issue of [noun phrase] that occurs when/during [condition]` (result-first phrasing)
- `Fix the issue of [noun phrase]` (noun-centric, no trigger clause)
- `Fix the [incorrect/inaccurate] [noun]` (standalone, for example, `Fix the incorrect error message ...`)
- `Fix a [rare/potential] issue that [description]` (rare or non-deterministic bugs)
- `Fix the potential/occasional [panic/crash] that occurs when [condition]` (specific crash scenarios)
- `Fix the panic issue caused by [X]` (panic identified by cause)

A complete entry should include the trigger condition (when it happens) and the observed impact (what the user sees), and optionally a workaround. Wrap exact error messages in backticks.

For non-deterministic failures, both `might` and `potential` are acceptable: use `might` as an inline modal verb (`Fix the issue that TiDB might crash when ...`) and `potential` as an adjective before a noun (`Fix the potential panic that occurs when ...`). Do not use `may` or `could`.

Examples:

```
- Fix the issue that executing SQL statements containing tables with multi-valued indexes might return the `Can't find a proper physical plan for this query` error [#49438](https://github.com/pingcap/tidb/issues/49438) @[qw4990](https://github.com/qw4990)
- Fix the issue that TiDB might crash when `tidb_mem_quota_analyze` is enabled and the memory used by updating statistics exceeds the limit [#52601](https://github.com/pingcap/tidb/issues/52601) @[hawkingrei](https://github.com/hawkingrei)
- Fix the panic issue caused by `GetAdditionalInfo` [#8079](https://github.com/tikv/pd/issues/8079) @[HuSharp](https://github.com/HuSharp)
```

Anti-patterns:

| Wrong | Right |
|-------|-------|
| `Fixed the issue that ...` (past tense) | `Fix the issue that ...` (imperative) |
| `Fixes an issue where ...` | `Fix the issue that ...` |
| `Fix the issue where ...` | `Fix the issue that ...` (use `that`, not `where`) |
| `Fix the issue that ... may ...` | Use `might` or `potential` |
| `The issue of X causing Y is fixed` | `Fix the issue that X causes Y` |

## Output format

Return **only a raw JSON object** — no Markdown fences, no extra text. Keys:

- `type`: `"improvement"`, `"bug_fix"`, or `"not_needed"`
- `release_note`: the formatted entry (see below for the value format)
- `needs_review`: `true` or `false`
- `reason`: short English reason for the type and wording

### `release_note` value

When `type` is `"improvement"` or `"bug_fix"`, `release_note` is one Markdown bullet assembled in this order:

```
- <description> <expected links as [#N](url)> <contributors as @[user](url)>
```

Improvement example:

```
- Support adding multiple indexes concurrently in the ingest mode [#52596](https://github.com/pingcap/tidb/issues/52596) @[lance6716](https://github.com/lance6716)
```

Bug fix example:

```
- Fix the issue that TiCDC might panic when the initialization of the Pulsar producer fails [#4937](https://github.com/pingcap/ticdc/issues/4937) @[wk989898](https://github.com/wk989898)
```

When `type` is `"not_needed"`, set `release_note` to the following format:

```
Release note is not needed for this change. Reason: <short reason>
```

Examples of `"not_needed"` reasons: `test-only change`, `internal refactor, no user-visible effect`, `flaky test fix`, `added internal debug logging`.
