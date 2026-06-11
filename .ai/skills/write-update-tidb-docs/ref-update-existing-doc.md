# Reference: Update Existing TiDB Documentation

This reference covers the full workflow for updating existing documentation pages
in `pingcap/docs`. Read this after the main SKILL.md has determined that one or
more existing pages need updating.

## When to update existing docs

Update rather than create when:

- A feature gains a new option, parameter, configuration item, or behavior mode
  that fits in the existing page structure.
- A default value, behavior, or limitation changes.
- A system variable, config parameter, or command-line flag is added or modified.
- A code change affects user-visible behavior documented on an existing page.
- A compatibility or deprecation note needs to be added.
- An existing page has outdated, incomplete, or incorrect information.

Prefer targeted edits over broad rewrites. Change only the sections affected by
the update unless the existing structure is clearly inadequate.

## Step 1: Identify target docs from code changes

Use the code change patterns to find which docs likely need updating:

| Code pattern | Primary target doc(s) |
| --- | --- |
| New/changed `SysVar` / `DefValue` | `system-variables.md`, `system-variable-reference.md` |
| New/changed config struct field / `toml` tag | `tidb-configuration-file.md`, `tikv-configuration-file.md`, `tiflash/tiflash-configuration.md`, `pd-configuration-file.md`, or equivalent |
| New/changed command-line flag | `command-line-flags-for-*-configuration.md` |
| Changed SQL grammar (parser `.y`) | `sql-statements/sql-statement-<name>.md` |
| New/changed built-in function | `functions-and-operators/` relevant file |
| New `INFORMATION_SCHEMA` table column | `information-schema/information-schema-<name>.md` |
| Changed metric or alert rule | `grafana-*.md` or monitoring docs |
| Changed default behavior | Feature doc + possibly release notes |
| New error code or message | Error reference docs |
| Changed API endpoint or response | API reference docs |

### Search strategies

Find existing docs by keyword, feature name, or path:

```bash
rg -l "<system-variable-name>|<config-name>|<feature-keyword>" --type md
rg -n "<keyword>" TOC*.md
```

When the code change touches a specific component, also check the component's
directory (`ticdc/`, `tiflash/`, `tiproxy/`, `dm/`, `br/`) for related docs.

## Step 2: Assess related and associated docs

A single code change often affects multiple documentation pages. Assess the full
impact before editing:

### Direct impact

Pages that directly describe the changed behavior:

- The primary reference page (config file, system variables, command flags)
- The feature or task page that explains how to use the behavior
- The SQL statement page if syntax changed

### Indirect impact

Pages that reference or summarize the changed behavior:

- **Overview pages**: pages that list or summarize features in a category (for
  example, `functions-and-operators-overview.md`, `sql-statement-overview.md`)
- **Compatibility pages**: `mysql-compatibility.md`, feature compatibility tables
- **Limitation pages**: `tidb-limitations.md`, feature-specific limitations
- **Release notes**: if the change is user-facing in a specific version
- **FAQ pages**: if the change affects commonly asked questions
- **Best practice pages**: if the change affects recommended workflows
- **Troubleshooting pages**: if the change resolves or introduces known issues

### Discovering related pages

```bash
# Find pages that mention the feature or config item
rg -l "<feature-name>|<config-name>" --type md

# Find pages that link to the target page
rg -l "/path-to-target-doc.md" --type md

# Check if the feature appears in overview or summary docs
rg -l "<feature-keyword>" *-overview.md basic-features.md
```

### Scope discipline

- Update direct-impact pages in the same edit.
- For indirect-impact pages, assess whether the update is **required for
  correctness** or merely **nice to have**.
- If an indirect page update is required (for example, a limitation was removed
  and the limitations page still lists it), include it.
- If an indirect page update is nice to have (for example, an overview page could
  mention the enhancement), flag it in the output notes but do not expand scope
  unless the user confirms.

## Step 3: Understand the existing page before editing

Before making changes, read the target page (or relevant sections) to understand:

1. **Existing structure**: heading hierarchy, section order, and content flow.
2. **Existing tone and voice**: formal vs. conversational, level of detail,
   whether the page uses imperative ("Configure X") or descriptive ("X is
   configured by") style.
3. **Existing patterns**: how similar items are documented on the same page. For
   example, if system variables use a specific description format, follow it.
4. **Existing terminology**: which terms the page uses for concepts. Do not
   introduce synonyms or alternate terms.
5. **Existing scope**: what the page covers and what it explicitly excludes. Do
   not expand scope without reason.

Key principle: **the updated section should read as if it were written by the
same author as the rest of the page**. Do not let new content stand out
stylistically.

## Step 4: Plan the edit

For each target page, determine:

- **Where** in the page the new content goes (which section, which position
  within the section).
- **What** to add, change, or remove.
- **How much** surrounding context to preserve or adjust for flow.

### Placement within a page

Follow existing ordering conventions on the page:

| Page type | Typical ordering |
| --- | --- |
| System variables | Alphabetical by variable name |
| Config parameters | Grouped by section, then by related functionality |
| SQL statement | Synopsis → Description → Examples → See also |
| Function reference | Syntax → Parameters → Return type → Examples |
| Feature page sections | Conceptual intro → Usage → Limitations → Compatibility |

When adding a new item to a list or table:

- Insert in the correct sort order (alphabetical, logical grouping, or as
  established by neighbors).
- Match the existing column structure and description style exactly.
- Do not reorder existing items unless correcting a clear sorting error.

### Handling additions vs. modifications

**Adding new content** (new parameter, new section, new example):

- Follow the format of adjacent entries.
- If adding a new section, maintain heading level hierarchy—do not skip levels.
- Add transitional context if needed so the addition flows with surroundings.

**Modifying existing content** (changed default, updated behavior):

- Change only the specific facts that are wrong or outdated.
- Preserve the sentence structure and style when possible.
- If the behavioral change is breaking, add a version note or warning.
- Update any version-specific statements (for example, "Starting from v8.4" →
  adjust the version scope).

**Removing content** (deprecated feature, removed limitation):

- Remove cleanly without leaving orphaned references or broken flow.
- Check if other parts of the same page reference the removed content.
- If the removal is for a deprecated feature, consider adding a deprecation note
  instead of deleting entirely.

## Step 5: Maintain style consistency

### Match the existing description format

For structured reference docs (system variables, config files), each entry
typically follows a pattern. Examples:

**System variable entry pattern:**

```markdown
### variable_name

- Scope: SESSION | GLOBAL | SESSION | GLOBAL, SESSION
- Persists to cluster: Yes | No
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes | No
- Type: Boolean | Integer | Enum | ...
- Default value: `<value>`
- Range: `[min, max]` (for numeric types)
- This variable controls ...
```

**Config parameter entry pattern:**

```markdown
### `parameter-name`

- Default value: `<value>`
- Range: ... (if applicable)
- Description text explaining what the parameter controls.
```

When adding new entries, replicate the exact format including field order,
punctuation, backtick usage, and description style.

### Preserve voice and level of detail

- If the page uses terse descriptions, keep new content terse.
- If the page uses full explanatory paragraphs, write comparably.
- If the page includes examples for each item, add an example for new items.
- If the page does not include examples, do not add one only for the new item
  unless it significantly aids understanding.

### Version annotations

When a change is version-specific:

- Use the established format: "Starting from vX.Y, ..." or "This variable was
  introduced in vX.Y."
- Place version notes consistently with how they appear elsewhere on the page.
- For behavior changes, clearly state both the old and new behavior when helpful.

## Step 6: Handle cross-document consistency

After editing, verify that related docs remain consistent:

1. **Same facts in multiple places**: if the same default value, limitation, or
   behavior appears in multiple docs, update all of them.
2. **Links still valid**: if you change a heading, check whether other docs link
   to that anchor.
3. **Feature lists and overviews**: if a feature gains new capabilities,
   check whether summary pages need updating.
4. **Compatibility tables**: if behavior changes for MySQL compatibility,
   `mysql-compatibility.md` may need updating.
5. **Code examples**: if a default changes, examples that rely on the old default
   may produce different output.

## Step 7: Handle version and branch scoping

Decide which branches the update targets:

| Change type | Target branch |
| --- | --- |
| New feature in development | `master` only |
| Behavior change in released version | `master` + cherry-pick label for the release branch |
| Bug fix in documentation (factual error) | `master` + cherry-pick label if error exists in release branch |
| TiDB Cloud documentation | `release-8.5` |
| AI / vector documentation | `release-8.5` |
| Wording improvement not tied to a version | `master` only |

When the update includes version-specific notes, ensure the phrasing is accurate
for the target branch. A note saying "Starting from v8.5" makes sense in
`master` and `release-8.5` but not in `release-8.4`.

## Step 8: Validate

1. Run `./scripts/markdownlint <changed-files>` to catch formatting issues.
2. If headings changed, run `./scripts/verify-links.sh` to detect broken anchors.
3. Re-read the changed section in context (at least 2–3 surrounding sections) to
   verify it reads naturally and consistently.
4. Verify facts against the source (code PR, issue, design doc).
5. For procedural docs, mentally trace the steps with the new information.
6. Check that no orphaned references remain if content was removed or moved.

## Common update patterns

### Adding a new system variable

1. Add the entry in `system-variables.md` in alphabetical order following the
   existing entry format.
2. If the variable is referenced in `system-variable-reference.md`, add it there
   too.
3. Check if the feature page that uses this variable should mention it.
4. If the variable controls a new feature, the feature doc takes priority; the
   variable entry should link to it.

### Adding a new config parameter

1. Add the entry in the corresponding `*-configuration-file.md` under the
   correct `[section]`.
2. Follow the exact format of neighboring entries.
3. If the parameter has a corresponding command-line flag, update the flag doc
   too.

### Updating default values or behavior

1. Change the default value in the parameter/variable description.
2. Add a version note if the change is version-specific.
3. Check if examples elsewhere on the page (or in other docs) assume the old
   default.
4. If the change is breaking, add a compatibility or warning note.

### Adding a limitation or removing a limitation

1. Update the limitations section of the feature doc.
2. If the limitation affects `tidb-limitations.md`, update that page too.
3. If a limitation is removed, check whether workaround documentation should also
   be removed or marked as no longer necessary.

### Documenting a deprecation

1. Add a deprecation notice in the relevant section with the version it was
   deprecated and expected removal timeline.
2. Update any "recommended" guidance that points users to the deprecated feature.
3. Link to the replacement feature or migration path.
4. Do not delete documentation for deprecated features that are still functional.

## Common mistakes to avoid

- Changing only one occurrence of a fact that appears in multiple places.
- Breaking the style or format consistency with surrounding entries.
- Expanding scope into unrelated improvements while making a targeted fix.
- Adding version notes that are inaccurate for the target branch.
- Leaving orphaned cross-references when removing or moving content.
- Introducing different terminology for the same concept within one page.
- Rewriting surrounding content unnecessarily while making a targeted edit.
