# Bilingual alignment and translation

Use this file for checking English/Chinese alignment of a paired release note file, translating entries in either direction, or auditing alignment by issue number. The cross-cutting rules in SKILL.md apply here too.

## Contents

- Alignment checklist
- Revision workflow
- English to Chinese translation
- Chinese to English translation

## Alignment checklist

### Must-be-identical items (no translation needed)

- Issue/PR numbers and URLs: `[#NNNNN](https://github.com/pingcap/tidb/issues/NNNNN)`
- Contributor handles and URLs: `@[contributor](https://github.com/contributor)`
- Inline code spans: `` `variable_name` ``, `` `COMMAND` ``, `` `--flag` ``
- Component names in section headers: `TiDB`, `TiKV`, `PD`, `TiFlash`, `BR`, `TiCDC`, `TiDB Lightning`
- Version numbers: `v7.5.0`, `v8.1.0`

### Anchor suffix convention

- English anchor for new variables/parameters: `#var_name-new-in-vXYZ`
- Chinese anchor for new variables/parameters: `#var_name-从-vXYZ-版本开始引入`
- Both link to the same doc page; only the anchor fragment differs
- Pre-existing variables (not new in this version): no suffix in either language — just `#var_name`

### Section presence parity

- Each English section must have an exact Chinese counterpart.  
- Example: If the English file has `### Behavior changes`, the Chinese file must have `### 行为变更`.  
- Treat missing sections as defects. See SKILL.md for section heading mappings.

### Table parity

- English and Chinese compatibility tables must have:

    - Same number of rows
    - Same row order
    - Same variable/parameter names
    - Matching change-type translations (`Newly added` ↔ `新增`, `Modified` ↔ `修改`, etc.)

### Note block punctuation

- English: `> **Note:**` (ASCII colon, no space after `**`)
- Chinese: `> **注意：**` (full-width colon `：`, inside the bold span)

### Contributors section

- English first-time contributor tag: `- [handle](url) (First-time contributor)`
- Chinese first-time contributor tag: `- [handle](url)（首次贡献者）` (full-width parentheses)

## Revision workflow

### Reviewing an existing entry

1. Identify the section (Compatibility changes, Improvements, or Bug fixes) and load the corresponding reference file
2. Check the opening pattern against section rules
3. Verify trailing punctuation (no `.` in English; no `。` in Chinese)
4. Verify inline code spans for all technical terms: variables, configs, SQL keywords/functions, error messages
5. Verify the issue link and contributor link at the end of the line
6. For Chinese entries: verify `修复` as the opening verb for bug fixes, or an approved opening verb for improvements

### Writing a new entry from a PR or issue description

1. Read the PR title and description. For bug fixes, prioritize the linked GitHub Issue (user-facing symptoms) over the PR diff (code changes)
2. Identify the component (TiDB, TiKV, PD, TiFlash, BR, TiCDC, TiDB Lightning)
3. Draft the English entry:
   - Bug fix: `Fix the issue that [concise repro condition and observed symptom] [#NNNNN](https://github.com/pingcap/tidb/issues/NNNNN) @[contributor](https://github.com/contributor)`
   - Improvement: `[Action verb] [what was improved, added, or supported] [#NNNNN](https://github.com/pingcap/tidb/issues/NNNNN) @[contributor](https://github.com/contributor)` — for approved opening verbs and usage guidance, see [improvements.md](improvements.md)
4. Draft the Chinese entry with the matching pattern
5. Verify issue numbers match exactly between English and Chinese
6. Verify the anchor suffix format if you include documentation links

## English to Chinese translation

1. Identify if the entry is a bug fix or improvement
2. Map the opening verb/phrase:
   - `Fix the issue that X` → `修复 [X 的中文表述] 的问题`
   - `Fix the issue that X might Y` → `修复 [X] 可能 [Y] 的问题`
   - `Fix the issue of X that occurs when Y` → `修复 [Y] 时 [X] 的问题`
   - `Improve/Optimize/Support/Add/Avoid X` → `优化/支持/新增/避免 [X 的中文表述]`
3. Keep all inline code unchanged
4. Keep all issue links and contributor links unchanged
5. Update doc anchor suffixes: `-new-in-vXYZ` → `-从-vXYZ-版本开始引入`
6. Do not add a trailing period

## Chinese to English translation

1. Identify the pattern:
   - `修复 [X] 的问题` → `Fix the issue that [X in English]`
   - `修复 [X] 可能 [Y] 的问题` → `Fix the issue that [X in English] might [Y in English]`
   - `修复 [X] 导致 [Y] 的问题` → `Fix the issue that [X] causes [Y]`
   - Chinese improvement verb maps to the corresponding English action verb (see improvements.md)
2. Keep all inline code unchanged
3. Keep all issue links and contributor links unchanged
4. Update doc anchor suffixes: `-从-vXYZ-版本开始引入` → `-new-in-vXYZ`
5. Do not add a trailing period
