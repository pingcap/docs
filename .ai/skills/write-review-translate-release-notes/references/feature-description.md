# Feature descriptions

Use this reference to write one TiDB release note feature description from PM or engineering input, such as a short feature brief, GitHub issue links, PR links, feature specification, benchmark results, and documentation links.

A quality feature description must answer four core questions for the reader:

1. **What is this feature?** — Describe the feature in user-facing terms, focusing on what is newly available or modified (avoid internal implementation details).
2. **When do you use this feature?** — Describe the specific user scenario or condition where this feature applies or is triggered.
3. **What value does it provide?** — State the value in terms of what "you" (the user) can now do, such as "you can ...", "... lets you ...", "... enables you to ...". Ground the benefit in a concrete outcome (performance, stability, security, operability, compatibility, or a workflow that was previously impossible) rather than describing what the system does internally.
4. **Is there anything to pay attention to?** — Call out enablement steps, maturity state, limitations, caveats, or benchmark conditions when they exist.

Different features need different narratives. A GA transition reads differently from a brand-new experimental feature; a performance optimization with benchmark numbers reads differently from a small SQL compatibility fix. This reference helps you diagnose the feature first, then select the right narrative shape and depth.

The cross-cutting rules in [SKILL.md](../SKILL.md) also apply, especially user perspective, inline-code formatting, issue and PR author links, and component names.

## Quick workflow

1. Read the supplied issue, PR, feature brief, and related documentation.
2. Extract only user-facing facts:
    - What is the feature, and what can users do with it?
    - What problem, limitation, or scenario does this feature address?
    - How do users enable, configure, or use it?
    - What benefit does it bring, such as performance, scalability, stability, compatibility, security, operability, or observability?
    - What maturity state applies: GA, experimental, or no maturity tag?
    - What caveats, unsupported cases, or benchmark conditions must be stated?
3. Decide whether the change belongs in a feature entry. If it is a small behavior improvement, bug fix, or internal refactor with no new user-facing capability, use the Improvements or Bug fixes reference instead.
4. Diagnose the feature using the dimensions in [Diagnose the feature, then choose the narrative shape](#diagnose-the-feature-then-choose-the-narrative-shape). Select a narrative shape and draft the entry. Make sure the body answers the four core questions: what the feature is, when to use it, what value it provides, and what to pay attention to.
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

## Diagnose the feature, then choose the narrative shape

Before writing, diagnose the feature along these dimensions:

| Dimension | Questions to ask |
|-----------|-----------------|
| Complexity | Can a user understand this in one sentence, or does it need background context? |
| Novelty | Is this entirely new, or does it change or improve something users already know? |
| Maturity transition | Is this a new experimental feature, a new GA feature, or a GA promotion from experimental? |
| Quantifiable impact | Are there sourced benchmark numbers, metrics, or concrete magnitudes? |
| User action | Must users enable, configure, migrate, or opt in? Or is it automatic? |
| Scope | Is this one capability, or does it bundle multiple sub-capabilities or benefits? |

Use the diagnosis to select a narrative shape:

| Signal | Recommended shape | What it prioritizes |
|--------|-------------------|---------------------|
| Easy to understand, no historical baggage | **Direct capability** | Lead with the capability and user value. Skip the context paragraph. |
| Removes a known limitation or changes an established workflow | **Before-and-after** | Start with the previous limitation, then the new behavior. |
| Value is hard to see without the user's environment or pain point | **Scenario-first** | Open with the user scenario, then introduce the capability as the solution. |
| One feature bundles multiple operations, modes, or benefits | **Sub-feature list** | Short intro, then a bulleted list of what is included or what benefits it delivers. |
| Experimental → GA transition with version history | **GA transition** | Trace the version history briefly, state the GA behavior, mention default changes. |

These shapes can combine. For example, a GA transition that bundles multiple benefits can use a sub-feature list inside the GA transition narrative.

**Benchmark modifier**: When sourced benchmark metrics and test conditions are available, add a benchmark table to whichever shape you chose. Explain the optimization strategy, present the table with metrics and test environment, and state conditions that scope the numbers. Benchmark data supplements the narrative shape; it does not replace it.

### Minimum viable entry

Every entry needs at least:

- Title line with issue links and PR author links
- One or two paragraphs that state what the feature is and the user value
- Documentation link

Add more paragraphs before the documentation link when the feature demands it:

- **Context paragraph**: when the feature solves a known limitation, changes an established workflow, or is hard to understand without background.
- **Enablement or configuration details**: when users must opt in, set a variable, or change a config item.
- **Maturity state**: when the feature is experimental or transitions to GA.
- **Caveats and limitations**: when there are unsupported cases, disabled-by-default behavior, or compatibility notes.
- **Benchmark table**: when sourced metrics and test conditions are available.
- **Sub-feature list**: when one entry covers multiple operations or benefits.

Do not pad entries with optional sections just because they exist. A short, clear entry that answers the core questions is better than a long entry that adds context, caveats, and enablement details the feature does not need.

## Title line

The title line should name the capability and, when useful, include the main benefit. It is usually a verb phrase.

Common title patterns:

```markdown
* Support <capability> [#NNNNN](...) @[pr_author](...)
* Support <capability> to improve <benefit> [#NNNNN](...) @[pr_author](...)
* Introduce <feature or mechanism> for <benefit> [#NNNNN](...) @[pr_author](...)
* Add <field, variable, parameter, statement, or identifier> [#NNNNN](...) @[pr_author](...)
* Improve <workflow or capability>, with <sourced metric or concrete benefit> [#NNNNN](...) @[pr_author](...)
* <Feature name> becomes generally available (GA) [#NNNNN](...) @[pr_author](...)
```

Title rules:

- Use the same bullet marker as the surrounding release file. Existing feature entries commonly use `*`; some patch release files use `-`.
- Do not end the title line with `.` or `。`.
- Include all relevant issue links and PR author links. The `@` link is the author of the PR that resolves the issue, not the issue author.
- Use `(experimental)` for experimental features.
- Use `(GA)` when a feature becomes generally available.
- Keep the title concise. Move explanation, conditions, and caveats into the body.

## Body paragraphs

Opening patterns listed below are examples, not required templates. Vary the openings across entries in the same release file to avoid monotony. Choose based on the narrative shape and what the reader needs first. See the [Examples](#examples) section for how each shape uses the body in practice.

### Context paragraph

Add a context paragraph only when it helps users understand the value, risk, or reason for the feature. Skip it when the feature is self-explanatory.

Common English openings:

- `Before vX.Y.Z, ...`
- `In earlier versions, ...`
- `When <scenario>, ...` (scenario-first, no version prefix)
- `In a TiDB cluster with <condition>, ...` (scenario-first, environment-based)

Common Chinese openings:

- `在 vX.Y.Z 之前，……`
- `在此前版本中，……`
- `当 <场景> 时，……`

### New behavior paragraph

Use the new behavior paragraph to explain what changes in this version and what users gain. For direct capability features, this is the first and possibly only paragraph.

Common English openings:

- `Starting from vX.Y.Z, ...`
- `In vX.Y.Z, ...`
- `TiDB vX.Y.Z introduces ...`
- `The <feature> becomes generally available (GA) in vX.Y.Z.`
- `<Feature noun phrase> <verb> ...` (no version prefix, when the capability is the natural lead)

Common Chinese openings:

- `从 vX.Y.Z 开始，……`
- `在 vX.Y.Z 中，……`
- `TiDB vX.Y.Z 引入……`
- `<Feature 名词短语> <动词> ……`

The paragraph should answer:

- What is the capability?
- How do users enable, configure, or use it, if applicable?
- What concrete benefit does it provide?

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

Do not infer a maturity state from the PR alone. Use only information provided by the issue, PR, release plan, PM input, or existing documentation.

## Style rules

These rules supplement the cross-cutting rules in [SKILL.md](../SKILL.md).

- Express value in terms of what "you" can do: prefer `you can ...`, `... lets you ...`, `... enables you to ...` over describing what the system does internally. The reader should see what changes for them, not just what the code does.
- State the capability or benefit before implementation details.
- Keep paragraphs short. Split long explanations into multiple paragraphs or a list.
- Do not overstate certainty. Use `can improve` or `helps reduce` when the benefit depends on workload.
- When the primary audience is an orchestrator or platform tool (such as TiDB Operator) rather than a human operator, describe what the mechanism provides and how operators or tools interact with it. The "you" might be an orchestration layer.
- Use normal sentence punctuation in body paragraphs. Only the title line omits the trailing period.

Chinese-specific rules:

- Use full-width punctuation in Chinese prose: `，`、`。`、`（`、`）`、`：`.
- Use Chinese verbs that match release-note style: `支持`, `引入`, `提供`, `新增`, `提升`, `优化`, `加速`.
- The Chinese documentation link sentence ends with `。`.
- The Chinese title line does not end with `。`.

## Examples

Each example is annotated with its narrative shape so you can see why the shape was chosen and how it structures the entry differently.

### Before-and-after: feature removes a known limitation

Why this shape: users already know TiDB has privilege control at the database and table levels, so the previous limitation provides context that makes the new column-level capability meaningful.

```markdown
* Support column-level privilege management [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf) @[fzzf678](https://github.com/fzzf678)

    Before v8.5.6, TiDB privilege control covers the database and table levels and does not support granting or revoking privileges on specific columns, unlike MySQL. As a result, you cannot restrict users to access only a subset of sensitive columns in a table.

    Starting from v8.5.6, TiDB supports column-level privilege management. You can use the `GRANT` and `REVOKE` statements to manage privileges on specific columns. TiDB performs privilege checks based on column-level privileges during query processing and execution plan construction, enabling finer-grained access control and better support for sensitive data isolation and the principle of least privilege.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/column-privilege-management).
```

### Direct capability: feature is self-explanatory, no historical context needed

Why this shape: "foreign keys" is a well-known database concept. Users do not need a "before" paragraph to understand the value. The entry leads with the capability and goes straight to the benefit.

```markdown
* Support foreign keys (GA) [#36982](https://github.com/pingcap/tidb/issues/36982) @[YangKeao](https://github.com/YangKeao) @[crazycs520](https://github.com/crazycs520)

    The foreign key feature becomes generally available (GA) in v8.5.0. Foreign key constraints help ensure data consistency and integrity. You can establish foreign key relationships between tables, with support for cascading updates and deletions, simplifying data management for applications with complex data relationships.

    For more information, see [documentation](/foreign-key.md).
```

### Scenario-first: value emerges from the user's environment

Why this shape: the feature (storage engine identifiers in logs) only makes sense when the reader understands the diagnostic scenario. Opening with the scenario makes the new fields feel like a natural answer.

```markdown
* Add storage engine identifiers to statement summary tables and slow query logs [#61736](https://github.com/pingcap/tidb/issues/61736) @[henrybw](https://github.com/henrybw)

    When both TiKV and TiFlash are deployed in a cluster, you might need to filter SQL statements by storage engine during database diagnostics and performance tuning. To support this workflow, TiDB adds storage engine identifier fields to statement summary tables and slow query logs.

    The new fields help you identify whether a SQL statement accesses TiKV or TiFlash, making it easier to locate workload patterns and diagnose performance issues.

    For more information, see [Statement Summary Tables](/statement-summary-tables.md) and [Identify Slow Queries](/identify-slow-queries.md).
```

### Sub-feature list: one feature with multiple user-facing benefits

Why this shape: log backup compaction has three distinct benefits worth calling out. A bulleted list makes each benefit scannable instead of burying them in prose.

```markdown
* Point-in-time recovery (PITR) supports recovery from compacted log backups for faster restores [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen)

    TiDB introduces offline compaction for log backups, which converts unstructured log backup data into structured SST files. This feature provides the following benefits:

    - Improved recovery performance: SST files can be imported into the cluster more quickly.
    - Reduced storage space consumption: redundant data is removed during compaction.
    - Reduced impact on applications: Recovery Point Objectives (RPOs) can be maintained with less frequent full snapshot backups.

    For more information, see [documentation](/br/br-compact-log-backup.md).
```

### Benchmark modifier applied: performance optimization with sourced metrics

Why this combination: the entry uses a sub-feature list shape (optimization strategies as bullet points) combined with the benchmark modifier. The benchmark table is the core evidence, framed by the optimization strategy and caveats.

```markdown
* Introduce significant performance improvements for certain lossy DDL operations (such as `BIGINT → INT` and `CHAR(120) → VARCHAR(60)`): when no data truncation occurs, the execution time of these operations can be reduced from hours to minutes, seconds, or even milliseconds, delivering performance gains ranging from tens to hundreds of thousands of times [#63366](https://github.com/pingcap/tidb/issues/63366) @[wjhuang2016](https://github.com/wjhuang2016), @[tangenta](https://github.com/tangenta), @[fzzf678](https://github.com/fzzf678)

    The optimization strategies are as follows:

    - In strict SQL mode, TiDB pre-checks for potential data truncation risks during type conversion.
    - If no data truncation risk is detected, TiDB updates only the metadata and avoids index rebuilding whenever possible.
    - If index rebuilding is required, TiDB uses a more efficient ingest process to significantly improve index rebuild performance.

  The following table shows example performance improvements based on benchmark tests on a table with 114 GiB of data and 600 million rows. The test cluster consists of 3 TiDB nodes, 6 TiKV nodes, and 1 PD node. All nodes are configured with 16 CPU cores and 32 GiB of memory.

    | Scenario | Operation type | Before optimization | After optimization | Performance improvement |
    |----------|----------------|---------------------|--------------------|--------------------------|
    | Non-indexed column | `BIGINT → INT` | 2 hours 34 minutes | 1 minute 5 seconds | 142× faster |
    | Indexed column | `BIGINT → INT` | 6 hours 25 minutes | 0.05 seconds | 460,000× faster |
    | Indexed column | `CHAR(120) → VARCHAR(60)` | 7 hours 16 minutes | 12 minutes 56 seconds | 34× faster |

    Note that the preceding test results are based on the condition that no data truncation occurs during the DDL execution. The optimizations do not apply to conversions between signed and unsigned integer types, conversions between character sets, or tables with TiFlash replicas.

    For more information, see [documentation](/sql-statements/sql-statement-modify-column.md).
```

### Experimental feature with enablement details

Why this shape: this is a new experimental feature that is disabled by default. Users need to know how to enable it and what to expect. The entry combines direct capability with explicit enablement and caveat information.

```markdown
* Support table-level data affinity to improve query performance (experimental) [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024)

    Starting from v8.5.5, you can configure the `AFFINITY` table option as `table` or `partition` when creating or altering a table. When this option is enabled, PD groups Regions that belong to the same table or partition into a single affinity group and prioritizes placing their Leaders and Voter replicas on the same subset of TiKV nodes. This reduces latency caused by cross-node scattered queries and can improve query performance.

    Note that this feature is currently experimental and is disabled by default. To enable it, set the PD configuration item `schedule.affinity-schedule-limit` to a value greater than `0`.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/table-affinity).
```

### GA transition: experimental feature promoted to GA

Why this shape: users who enabled this feature experimentally need to know the version history and what changes with GA. Users who are new need to understand why the feature exists.

```markdown
* Provide the Active PD Follower feature to enhance the scalability of PD's Region information query service (GA) [#7431](https://github.com/tikv/pd/issues/7431) @[okJiang](https://github.com/okJiang)

    In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances and a high concurrency of Region information requests, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.

    TiDB v7.6.0 introduces Active PD Follower as an experimental feature. In v8.5.0, this feature becomes generally available (GA). After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader.

    For more information, see [documentation](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service).
```

## Review checklist

Three core questions (must all be answered):

- [ ] **What is this feature?** — The entry clearly names the capability in user-facing terms.
- [ ] **What value does it provide?** — The entry states a concrete benefit, not just what changed technically.
- [ ] **Anything to pay attention to?** — Enablement, maturity state, caveats, and limitations are included when they exist; omitted when they do not.

Shape and structure:

- [ ] The narrative shape fits the feature. A simple feature is not padded with unnecessary context; a complex feature is not compressed into one paragraph.
- [ ] The entry does not repeat the same opening pattern as neighboring entries in the target file.
- [ ] The title line is concise, has issue links and PR author links, and has no trailing period.
- [ ] Performance claims include sourced metrics and test conditions, not vague adjectives.

Formatting and accuracy:

- [ ] Variables, config parameters, SQL statements, error messages, literal values, and links use the formatting rules in [SKILL.md](../SKILL.md).
- [ ] Every technical claim is traceable to the source input.
- [ ] The entry ends with a valid documentation link or an explicit placeholder for follow-up.
