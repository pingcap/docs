# Feature descriptions

Rules for the `## Feature details` (major/DMR releases) and `## Features` (patch releases) sections. The cross-cutting rules in SKILL.md (user perspective, inline-code conventions, issue and contributor links, and component names) also apply here.

## Contents

- Section heading and grouping
- Entry structure (anatomy of a feature description)
- Title line conventions
- Body paragraphs: structure and required content
- Documentation link
- GA, experimental, and version-lifecycle language
- Style rules (tone, sentence structure, metrics, trailing periods, Chinese-specific)
- Differences between major and patch releases
- Common review findings

## Section heading and grouping

### Major and DMR releases

Major releases (for example, v8.5.0) and DMR releases (for example, v8.4.0-DMR) use `## Feature details` as the section heading.

Features are grouped under level-3 category headings. Common categories include:

- `### Scalability`
- `### Performance`
- `### Reliability`
- `### Availability`
- `### SQL`
- `### DB Operations and Observability` (or separate `### DB operations` and `### Observability`)
- `### Security`
- `### Data Migration`

Each feature is a top-level bullet (`*`) followed by one or more indented body paragraphs.

### Patch releases

Patch releases (for example, v8.5.4, v8.5.5) use `## Features` as the section heading.

When there are enough features, they are grouped under the same level-3 category headings as major releases. When a patch has only a few features and no clear grouping, features may appear as direct children of `## Features` without level-3 headings (as in v8.5.4).

For the full EN/ZH heading mapping, see the section heading mapping table in [SKILL.md](../SKILL.md).

## Entry structure

A complete feature description contains up to five parts, in order:

### 1. Title line

The title line is the first line of the entry. It serves as a concise summary of the feature. It includes the feature name, maturity tag, issue/PR links, and contributor links.

### 2. Before paragraph (the problem or limitation)

Describes the situation before this feature exists, or the problem/limitation this feature addresses. This sets the context and motivation.

### 3. After paragraph (what changes starting from this version)

Describes what the feature does and how it works starting from this version. This is the core of the description.

### 4. Additional details (optional)

Provides supplementary information such as caveats, limitations, usage notes, configuration details, or performance benchmarks. May use sub-lists, tables, or code examples.

### 5. Documentation link

A closing line that points the reader to detailed documentation.

Not all five parts are always present. The minimum viable entry includes the title line, the after paragraph, and the documentation link. The before paragraph is strongly recommended for any feature that changes existing behavior or solves a pre-existing limitation.

## Title line conventions

### Format

The title line starts with `*` (not `-`), followed by the feature name and a maturity tag (if applicable), then issue/PR links and contributor links.

```
* Feature name (maturity tag) [#NNNNN](https://github.com/org/repo/issues/NNNNN) @[contributor](https://github.com/contributor)
```

### Maturity tags

| Tag | When to use | English | Chinese |
|-----|-------------|---------|---------|
| GA | Feature reaches general availability in this version | `(GA)` or `(GA in vX.Y.Z)` | `(GA)` |
| Experimental | Feature is newly introduced as experimental | `(experimental)` | `(实验特性)` |
| GA from experimental | Feature transitions from experimental to GA | Include version history in the title or body | Same |

Examples:

- `* Support foreign keys (GA) [#36982](...)`
- `* Support redistributing data of a specific table (experimental) [#63260](...)`
- `* TiDB accelerated table creation becomes generally available (GA), significantly reducing data migration and cluster initialization time [#50052](...)`

### Title style

The title is a concise noun phrase or verb phrase that names the feature and its key benefit. Two common patterns:

**Pattern A: Verb phrase describing the capability**

```
* Support foreign keys (GA) [#36982](...) @[YangKeao](...)
* Support pushing index lookups down to TiKV to improve query performance [#62575](...) @[lcwangchao](...)
* Support gracefully shutting down TiFlash [#10266](...) @[gengliqi](...)
```

**Pattern B: Noun phrase naming the feature with a benefit clause**

```
* TiDB accelerated table creation becomes generally available (GA), significantly reducing data migration and cluster initialization time [#50052](...) @[D3Hunter](...)
* Introduce significant performance improvements for certain lossy DDL operations ... [#63366](...) @[wjhuang2016](...)
* Foreign key checks now support shared locks [#66154](...) @[you06](...)
```

**Pattern C: Descriptive phrase for GA transitions (version-history style)**

```
* Setting the memory limit for schema cache is now generally available (GA). When the number of tables reaches hundreds of thousands or even millions, this feature significantly reduces the memory usage of schema metadata [#50959](...) @[tiancaiamao](...)
* Provide the Active PD Follower feature to enhance the scalability of PD's Region information query service (GA) [#7431](...) @[okJiang](...)
```

### Verbs used in title lines

| Verb | Usage |
|------|-------|
| `Support` | New capability: `Support column-level privilege management`, `Support gracefully shutting down TiFlash` |
| `Introduce` | New mechanism or architecture: `Introduce a new TiCDC architecture option for improved performance, scalability, and stability` |
| `Provide` | Provide a feature or service: `Provide the Active PD Follower feature to enhance the scalability of PD's Region information query service` |
| `Add` | New element (field, parameter, identifier): `Add storage engine identifiers to statement summary tables and slow query logs` |
| `Improve` | Enhancement: `Improve DDL performance in scenarios with a large number of foreign keys` |
| `Accelerate` | Speed improvement: `Accelerate recovery of system tables from backups` |

### No trailing period on title lines

Title lines do not end with `.` (English) or `。` (Chinese).

## Body paragraphs

### Before paragraph

Describes the world before this feature. Common patterns:

**English**

- `Before vX.Y.Z, ...`
- `In earlier versions, ...`
- `In TiDB versions earlier than vX.Y.Z, ...`
- Problem-oriented: directly states the limitation without a version prefix

**Chinese**

- `在 vX.Y.Z 之前，……`
- `在此前版本中，……`
- `在 vX.Y.Z 之前的版本中，……`

The before paragraph establishes the motivation: why the user should care about this feature. It typically describes a limitation, a pain point, or a suboptimal behavior.

### After paragraph

Describes the new behavior starting from this version. Common patterns:

**English**

- `Starting from vX.Y.Z, ...`
- `In vX.Y.Z, ...`
- `TiDB vX.Y.Z introduces ...`
- `TiDB vX.Y.Z optimizes ...`

**Chinese**

- `从 vX.Y.Z 开始，……`
- `在 vX.Y.Z 中，……`
- `TiDB vX.Y.Z 引入……`
- `TiDB vX.Y.Z 优化了……`

The after paragraph answers: what the feature does, how it works (briefly), and what the user gains.

### Before-after structure examples

**Example 1: Problem → solution (v8.5.6, column-level privilege)**

```markdown
* Support column-level privilege management [#61706](...) @[CbcWestwolf](...) @[fzzf678](...)

    Before v8.5.6, TiDB privilege control covers the database and table levels and does not support granting or revoking privileges on specific columns, unlike MySQL. As a result, you cannot restrict users to access only a subset of sensitive columns in a table.

    Starting from v8.5.6, TiDB supports column-level privilege management. You can use the `GRANT` and `REVOKE` statements to manage privileges on specific columns. TiDB performs privilege checks based on column-level privileges during query processing and execution plan construction, enabling finer-grained access control and better support for sensitive data isolation and the principle of least privilege.

    For more information, see [documentation](...).
```

**Example 2: GA transition with version history (v8.5.0, schema cache)**

```markdown
* Setting the memory limit for schema cache is now generally available (GA). When the number of tables reaches hundreds of thousands or even millions, this feature significantly reduces the memory usage of schema metadata [#50959](...) @[tiancaiamao](...)

    In some SaaS scenarios, where the number of tables reaches hundreds of thousands or even millions, schema metadata can consume a significant amount of memory. With this feature enabled, TiDB uses the Least Recently Used (LRU) algorithm to cache and evict the corresponding schema metadata, effectively reducing memory usage.

    Starting from v8.4.0, this feature is enabled by default with a default value of `536870912` (that is, 512 MiB). You can adjust it as needed using the variable [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800).

    For more information, see [documentation](/schema-cache.md).
```

**Example 3: New feature with performance benchmarks (v8.5.5, lossy DDL)**

```markdown
* Introduce significant performance improvements for certain lossy DDL operations (...) [#63366](...) @[wjhuang2016](...)

    The optimization strategies are as follows:

    - In strict SQL mode, TiDB pre-checks for potential data truncation risks during type conversion.
    - If no data truncation risk is detected, TiDB updates only the metadata and avoids index rebuilding whenever possible.
    - If index rebuilding is required, TiDB uses a more efficient ingest process to significantly improve index rebuild performance.

  The following table shows example performance improvements based on benchmark tests ...

    | Scenario | Operation type | Before optimization | After optimization | Performance improvement |
    |----------|----------------|---------------------|--------------------|--------------------------|
    | Non-indexed column | `BIGINT → INT` | 2 hours 34 minutes | 1 minute 5 seconds | 142× faster |
    | Indexed column | `BIGINT → INT` | 6 hours 25 minutes | 0.05 seconds | 460,000× faster |
    | Indexed column | `CHAR(120) → VARCHAR(60)` | 7 hours 16 minutes | 12 minutes 56 seconds | 34× faster |

    Note that the preceding test results are based on the condition that no data truncation occurs ...

    For more information, see [documentation](...).
```

**Example 4: New architecture with caveats (v8.5.4, TiCDC architecture)**

```markdown
* Introduce a new TiCDC architecture option for improved performance, scalability, and stability [#442](...) @[CharlesCheung96](...)

    This new architecture redesigns TiCDC core components and optimizes its data processing workflows, while maintaining compatibility with the configuration, usage, and APIs of the classic TiCDC architecture.

    When configured to use this new architecture, TiCDC achieves near-linear scalability and can replicate millions of tables with lower resource consumption. It also reduces changefeed latency and delivers more stable performance in scenarios with high write workloads, frequent DDL operations, and cluster scaling. Note that the new architecture currently has some initial limitations.

    To use the new architecture, set the TiCDC configuration item [`newarch`](...) to `true`.

    For more information, see [documentation](...).
```

### Additional details

When extra context is needed, use one or more of the following patterns after the before-after paragraphs:

- **Configuration or usage instructions**: describe how to enable, configure, or use the feature. Include variable names, configuration items, SQL statements, or command-line flags in backticks.
- **Performance benchmarks**: include a table or inline metrics when available. State the test conditions (cluster spec, data size).
- **Caveats and limitations**: describe restrictions, unsupported scenarios, or known issues. Use phrasing like `Note that ...` or a separate paragraph.
- **Sub-list of capabilities**: use `-` items indented under the main entry for enumerating sub-features, supported operations, or optimization strategies.
- **Behavior details**: describe behavior for different conditions (for example, "If X finishes before timeout, Y. If X does not finish, Z.").

## Documentation link

Every feature entry ends with a documentation link.

**English**

```markdown
    For more information, see [documentation](/path-to-doc.md).
    For more information, see [documentation](/path-to-doc.md#anchor).
```

**Chinese**

```markdown
    更多信息，请参考[用户文档](/path-to-doc.md)。
    更多信息，请参考[用户文档](/path-to-doc.md#锚点)。
```

The documentation link is indented at the same level as the body paragraphs (4 spaces under the `*` title line). Both English and Chinese doc link lines end with a period (`.` for English, `。` for Chinese), because they are full sentences within body paragraphs.

## GA, experimental, and version-lifecycle language

### GA features

When a feature transitions to GA, the description should briefly mention its history:

- `The foreign key feature becomes generally available (GA) in v8.5.0.`
- `Starting from v8.5.0, this feature becomes generally available (GA).`
- `In v8.2.0, this feature becomes generally available (GA) and is enabled by default.`
- `TiDB v7.6.0 introduces X as an experimental feature. ... In v8.5.0, this feature becomes generally available (GA).`

Chinese equivalents:

- `外键功能在 v8.5.0 中正式 GA。`
- `从 v8.5.0 开始，该功能正式 GA。`

### Experimental features

When a feature is introduced as experimental, state this clearly:

- `(experimental)` in the title tag
- `This feature is currently experimental and is disabled by default.` in the body (if applicable)

### Version-history references

For features first introduced in an earlier version, mention the version history:

- `TiDB v7.6.0 introduces X as an experimental feature, controlled by the system variable [`Y`](...). Starting from v8.0.0, this system variable is renamed to [`Z`](...).`
- `In v8.0.0, TiKV encryption at rest experimentally supports using Google Cloud KMS. Starting from v8.5.0, this feature becomes generally available (GA).`

## Style rules

### Tone and perspective

- Write from the user's perspective. Describe what the user can do, what the user observes, or what changes for the user.
- Use present tense for describing the feature's behavior: "TiDB supports ...", "You can use ...".
- Use imperative mood for configuration instructions: "Set the variable to ...", "To enable this feature, ...".

### Sentence structure

- Lead with the most important information. State the capability or benefit before describing the mechanism.
- Avoid passive voice when active voice is natural: prefer "TiDB supports X" over "X is supported by TiDB".
- Use concise compound sentences. Avoid overly long sentences; break complex descriptions into separate sentences.

### Metric claims

Performance claims should include:

- The metric type (for example, "performance", "QPS", "latency")
- The magnitude (for example, "up to 25x", "by 62.5%", "from hours to seconds")
- The test conditions when available (cluster spec, data size)

### Trailing period convention

Feature body paragraphs use normal sentence punctuation with trailing periods. Only the title line omits the trailing period. This differs from single-line improvement and bug-fix entries, which omit the trailing period entirely.

### Chinese-specific rules

Chinese title lines follow the same verb patterns as English but use Chinese verbs:

| English verb | Chinese equivalent |
|-------------|-------------------|
| `Support` | `支持` |
| `Introduce` | `引入` |
| `Provide` | `提供` |
| `Add` | `新增` |
| `Improve` | `提升` / `优化` |
| `Accelerate` | `加速` |

Before-after phrasing:

- Before: `在 vX.Y.Z 之前，……` / `在此前版本中，……`
- After: `从 vX.Y.Z 开始，……` / `TiDB vX.Y.Z 引入了……`

Punctuation:

- Use full-width punctuation in Chinese prose: `，`、`。`、`（`、`）`、`：`
- Documentation link sentence ends with `。`: `更多信息，请参考[用户文档](/path.md)。`
- Title lines do not end with `。`

## Differences between major and patch releases

| Aspect | Major/DMR release | Patch release |
|--------|-------------------|---------------|
| Section heading | `## Feature details` | `## Features` |
| Level-3 category headings | Always present | Present when there are enough features; may be omitted for a small number of features |
| Highlight table | Major releases may include an HTML `<table>` summary of highlights at the top of the file, before `## Feature details` | Not present |
| Scope | New features, GA transitions, and major capability additions | Backported features, GA transitions, and incremental capability additions |
| Version-history detail | More detailed for features that evolved over multiple DMR cycles | Typically shorter; references the original introduction version |

## Common review findings

| Finding | Correct |
|---------|---------|
| Entry uses `-` instead of `*` for the title line | Use `*` for the feature title line (sub-items within the body use `-`) |
| Missing before paragraph for a feature that addresses a pre-existing limitation | Add a before paragraph describing the limitation or pain point |
| Missing documentation link | Add `For more information, see [documentation](/path.md).` |
| Title line ends with `.` | Remove the trailing period from the title line |
| Body omits the version number in `Starting from ...` | Always specify the version: `Starting from v8.5.5, ...` |
| GA transition does not mention the original experimental version | Add version history: `Introduced as experimental in vX.Y.Z.` |
| Feature description only explains what the code does, not the user benefit | Rewrite to explain what the user gains (capability, performance, stability) |
| Chinese doc link missing `。` | Chinese doc link line ends with `。`: `更多信息，请参考[用户文档](/path.md)。` |
| English doc link missing `.` | English doc link line ends with `.`: `For more information, see [documentation](/path.md).` |
| Performance claim without test conditions | Add test environment details (cluster spec, data size) when available |
| Maturity tag missing for experimental features | Add `(experimental)` to the title |
| Maturity tag missing for GA transitions | Add `(GA)` or `(GA in vX.Y.Z)` to the title |
| Chinese anchor uses English suffix | Change `-new-in-vXYZ` to `-从-vXYZ-版本开始引入` in Chinese entries |
| Inline code not applied to variables, configs, or SQL keywords | Apply backtick formatting per the inline-code rules in SKILL.md |
