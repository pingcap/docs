# Variable or Configuration Documentation-impact Task

## Variable or configuration documentation-impact task

Decide whether the PR code changes add, modify, deprecate, delete, or rename a user-facing system variable or configuration parameter that documentation maintainers need to check. This is a triage signal; it does not claim that the corresponding documentation is currently missing.

Return `detected` even if the same PR also updates documentation. Classify the product change, not whether the documentation work has already been completed.

## Set `status` to `detected`

Use `detected` when:

- A user-facing system variable or configuration parameter is newly added, modified, deprecated, deleted, or renamed.
- A user-facing command-line flag that serves as a configuration option changes in one of those ways.
- Its default value, allowed range, units, validation rules, scope, mutability, persistence, compatibility, or documented behavior changes.
- A bug fix changes behavior that users configure through the variable or parameter and the documented semantics might need revision.

For each detected change:

- `kind` must be `system_variable` or `configuration_parameter`.
- `name` must be the exact user-facing variable or parameter name. Do not return an internal Go, Rust, C++, or test symbol.
- `change_type` must be `newly_added`, `modified`, `deprecated`, `deleted`, or `renamed`.
- `description` must concisely state what changed and what documentation maintainers should verify.
- `source_pr` must be the exact corresponding PR URL from `pr_urls` and `pull_requests[]`. When the row has PR links, do not use an issue URL or invent a URL. Use an empty string only when the input has no PR URL.

## Set `status` to `not_detected`

Do not report:

- Internal constants, struct fields, function arguments, test-only variables, test fixtures, failpoints, or CI settings.
- Refactors that move or rename internal code without changing the public variable or parameter.
- Changes to a variable or parameter implementation that preserve its documented user-facing semantics.
- A sample or test configuration edit unless the underlying supported parameter also changes.

Set `changes` to an empty array.

## Set `status` to `uncertain`

Use `uncertain` instead of guessing when relevant GitHub data could not be fetched, changed-file information is truncated or omits the relevant definition, or visible evidence suggests a configuration change but does not establish whether it is user-facing.

If any PR URL appears in `fetch_failed_urls`, use `uncertain` because the code changes could not be inspected. If only an issue URL failed but the PR and changed-file evidence are sufficient, judge from the available PR evidence.

Set `changes` to an empty array and `needs_review` to `true`. Do not choose `uncertain` merely because documentation maintainers still need to verify the affected document when the product change itself is clear.

## Required output field

Return `variable_or_config_doc_impact`, an object with exactly these fields:

- `status`: `"detected"`, `"not_detected"`, or `"uncertain"`.
- `changes`: an array of detected change objects; use an empty array for `not_detected` and `uncertain`.
- `needs_review`: `true` or `false`; it must be `true` for `uncertain`.
- `reason`: a short English reason for the decision.

Each object in `changes` has exactly these fields:

- `kind`: `"system_variable"` or `"configuration_parameter"`.
- `name`: the exact user-facing name.
- `change_type`: `"newly_added"`, `"modified"`, `"deprecated"`, `"deleted"`, or `"renamed"`.
- `description`: a concise description of the documentation impact.
- `source_pr`: an exact PR URL from the input, or an empty string only if no PR URL exists.
