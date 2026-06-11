# Feature descriptions

Use this reference to write one TiDB release note feature description from PM or engineering input, such as a short feature brief, GitHub issue links, PR links, feature specification, benchmark results, and documentation links.

The goal is not to summarize implementation work. The goal is to produce a user-facing entry that matches the `## Feature details` or `## Features` style in current TiDB release notes: clear title, concrete user problem, new capability in this version, user value, and a documentation link.

The cross-cutting rules in [SKILL.md](../SKILL.md) also apply, especially user perspective, inline-code formatting, issue and contributor links, and component names.

## Quick workflow

1. Read the supplied issue, PR, feature brief, and related documentation.
2. Extract only user-facing facts:
    - What problem, limitation, or scenario does this feature address?
    - What can users do starting from this version?
    - How do users enable, configure, or use it?
    - What benefit does it bring, such as performance, scalability, stability, compatibility, security, operability, or observability?
    - What maturity state applies: GA, experimental, or no maturity tag?
    - What caveats, unsupported cases, or benchmark conditions must be stated?
3. Decide whether the change belongs in a feature entry. If it is a small behavior improvement, bug fix, or internal refactor with no new user-facing capability, use the Improvements or Bug fixes reference instead.
4. Draft the entry using the standard structure: title line, context paragraph, new behavior paragraph, optional details, and documentation link.
5. Check every technical claim against the source input. Do not invent defaults, limits, metrics, maturity state, or documentation links.

## Section placement in the release note file

```markdown
## Features
```

Use level-3 category headings when the release groups features by area. Common categories are:

- `### Scalability`
- `### Performance`
- `### Reliability`
- `### Availability`
- `### SQL`
- `### DB Operations and Observability`
- `### DB operations`
- `### Observability`
- `### Security`
- `### Data Migration`

For Chinese heading mappings, see [SKILL.md](../SKILL.md).

When writing the description for a feature, consider which category the feature belongs to and use the appropriate heading.

## Entry shape

Prefer this shape for a complete feature description:

```markdown
* <Feature title> <maturity tag if needed> [#NNNNN](https://github.com/org/repo/issues/NNNNN) @[contributor](https://github.com/contributor)

    Before vX.Y.Z, <describe the user-facing limitation, pain point, or scenario>.

    Starting from vX.Y.Z, <describe the new capability, how users use or configure it, and the user benefit>.

    <Optional details: caveats, limitations, examples, configuration notes, benchmark table, or sub-feature list.>

    For more information, see [documentation](/path-to-doc.md).
```

Minimum viable entry:

- Title line
- One paragraph that states the new behavior and user value
- Documentation link

Add a before paragraph when the feature solves a known limitation, changes an existing workflow, or needs motivation to be understandable.

## Title line

The title line should name the capability and, when useful, include the main benefit. It is usually a verb phrase.

Common title patterns:

```markdown
* Support <capability> [#NNNNN](...) @[contributor](...)
* Support <capability> to improve <benefit> [#NNNNN](...) @[contributor](...)
* Introduce <feature or mechanism> for <benefit> [#NNNNN](...) @[contributor](...)
* Add <field, variable, parameter, statement, or identifier> [#NNNNN](...) @[contributor](...)
* Improve <workflow or capability>, with <sourced metric or concrete benefit> [#NNNNN](...) @[contributor](...)
* <Feature name> becomes generally available (GA) [#NNNNN](...) @[contributor](...)
```

Title rules:

- Use the same bullet marker as the surrounding release file. Existing feature entries commonly use `*`; some patch release files use `-`.
- Do not end the title line with `.` or `。`.
- Include all relevant issue links and contributor links.
- Use `(experimental)` for experimental features.
- Use `(GA)` when a feature becomes generally available.
- Keep the title concise. Move explanation, conditions, and caveats into the body.

## Body paragraphs

### Context paragraph

Use the context paragraph to explain why the feature matters. It usually describes the previous limitation or user scenario.

Common English openings:

- `Before vX.Y.Z, ...`
- `In TiDB versions earlier than vX.Y.Z, ...`
- `In earlier versions, ...`
- `<Scenario or limitation sentence without a version prefix>.`

Common Chinese openings:

- `在 vX.Y.Z 之前，……`
- `在 vX.Y.Z 之前的版本中，……`
- `在此前版本中，……`

### New behavior paragraph

Use the new behavior paragraph to explain what changes in this version and what users gain.

Common English openings:

- `Starting from vX.Y.Z, ...`
- `In vX.Y.Z, ...`
- `TiDB vX.Y.Z introduces ...`
- `TiDB vX.Y.Z optimizes ...`

Common Chinese openings:

- `从 vX.Y.Z 开始，……`
- `在 vX.Y.Z 中，……`
- `TiDB vX.Y.Z 引入……`
- `TiDB vX.Y.Z 优化了……`

The paragraph should answer:

- What is the capability?
- How do users enable, configure, or use it, if applicable?
- What concrete benefit does it provide?

## Optional details

Add extra details only when they help users evaluate or use the feature.

- Configuration or usage: mention system variables, configuration items, SQL statements, command-line flags, and literal values in backticks.
- Caveats and limitations: state unsupported cases, disabled-by-default behavior, compatibility notes, or known constraints.
- Performance metrics: include the metric, magnitude, and test conditions when available. Do not use unsourced claims such as "significant" or "large" unless the input supports them.
- Sub-feature lists: use indented `-` items for supported operations, optimization strategies, or new fields.
- Benchmark tables: include only sourced results and enough environment details to make the numbers meaningful.

## Documentation link

End every complete feature description with a documentation link.

English:

```markdown
    For more information, see [documentation](/path-to-doc.md).
```

Chinese:

```markdown
    更多信息，请参考[用户文档](/path-to-doc.md)。
```

If no documentation page exists yet, do not invent one. Ask for the intended documentation link or leave a clear placeholder for human follow-up.

## Maturity and version history

For experimental features:

- Add `(experimental)` to the title line.
- State whether the feature is disabled by default, and explain how to enable it if the input provides that information.

For features that become generally available (GA) from an experimental version:

- Add `(GA)` to the title line when it reads naturally.
- Mention the previous experimental version if known.
- State whether the feature becomes enabled by default if that is part of the release behavior.

For features that are new and GA from the start:

- No need to add `(GA)` to the title line, which means that a feature is GA by default if `(experimental)` is not present.

Useful patterns:

```markdown
TiDB vX.Y.Z introduces <feature> as an experimental feature. In vA.B.C, this feature becomes generally available (GA).

Starting from vA.B.C, <feature> becomes generally available (GA) and is enabled by default.
```

Do not infer a maturity state from the PR alone. Use only information provided by the issue, PR, release plan, PM input, or existing documentation.

## Style rules

- Write for users, not implementers.
- Prefer `you can ...`, `TiDB supports ...`, and `Starting from vX.Y.Z, ...`.
- State the capability or benefit before implementation details.
- Use present tense for product behavior.
- Use active voice when natural.
- Keep paragraphs short. Split long explanations into multiple paragraphs or a list.
- Do not expose internal function names, package names, test names, or code-level refactors unless they are user-visible.
- Do not overstate certainty. Use `can improve` or `helps reduce` when the benefit depends on workload.
- Use normal sentence punctuation in body paragraphs. Only the title line omits the trailing period.

Chinese-specific rules:

- Use full-width punctuation in Chinese prose: `，`、`。`、`（`、`）`、`：`.
- Use Chinese verbs that match release-note style: `支持`, `引入`, `提供`, `新增`, `提升`, `优化`, `加速`.
- The Chinese documentation link sentence ends with `。`.
- The Chinese title line does not end with `。`.

## Examples

### Standard before-and-after feature

```markdown
* Support column-level privilege management [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf) @[fzzf678](https://github.com/fzzf678)

    Before v8.5.6, TiDB privilege control covers the database and table levels and does not support granting or revoking privileges on specific columns, unlike MySQL. As a result, you cannot restrict users to access only a subset of sensitive columns in a table.

    Starting from v8.5.6, TiDB supports column-level privilege management. You can use the `GRANT` and `REVOKE` statements to manage privileges on specific columns. TiDB performs privilege checks based on column-level privileges during query processing and execution plan construction, enabling finer-grained access control and better support for sensitive data isolation and the principle of least privilege.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/column-privilege-management).
```

### Experimental feature with enablement

```markdown
* Support table-level data affinity to improve query performance (experimental) [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024)

    Starting from v8.5.5, you can configure the `AFFINITY` table option as `table` or `partition` when creating or altering a table. When this option is enabled, PD groups Regions that belong to the same table or partition into a single affinity group and prioritizes placing their Leaders and Voter replicas on the same subset of TiKV nodes. This reduces latency caused by cross-node scattered queries and can improve query performance.

    Note that this feature is currently experimental and is disabled by default. To enable it, set the PD configuration item `schedule.affinity-schedule-limit` to a value greater than `0`.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/table-affinity).
```

### GA transition

```markdown
* Provide the Active PD Follower feature to enhance the scalability of PD's Region information query service (GA) [#7431](https://github.com/tikv/pd/issues/7431) @[okJiang](https://github.com/okJiang)

    In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances and a high concurrency of Region information requests, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.

    TiDB v7.6.0 introduces Active PD Follower as an experimental feature. In v8.5.0, this feature becomes generally available (GA). After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader.

    For more information, see [documentation](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service).
```

## Review checklist

- The entry describes user-facing capability and value, not only implementation work.
- The title line is concise, has issue and contributor links, and has no trailing period.
- Existing limitations are explained when needed.
- Enablement, configuration, caveats, and limitations are included when relevant.
- Performance claims include metrics and test conditions when available.
- Variables, config parameters, SQL statements, error messages, literal values, and links use the formatting rules in [SKILL.md](../SKILL.md).
- The entry ends with a valid documentation link or an explicit placeholder for follow-up.
- The wording follows nearby release note entries in the target file.
