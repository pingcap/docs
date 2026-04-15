# Compatibility changes

Rules for the `## Compatibility changes` / `## 兼容性变更` section, including the upgrade note block, behavior-change paragraphs, system-variable tables, and configuration-file-parameter tables.

## Contents

- Upgrade note block
- Behavior changes (paragraph format, required content, examples)
- System variables table (format, change-type vocabulary, anchor convention)
- Configuration parameters table
- Common review findings

## Upgrade note block

Each Compatibility changes section begins with a note block that specifies the explicit "from" version and the current version. Do not write "from the previous version" without version numbers.

**English**

```markdown
> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from vA.B.C to the current version (vX.Y.Z). If you are upgrading from vA.B.C or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.
```

**Chinese**

```markdown
> **注意：**
>
> 以下为从 vA.B.C 升级至当前版本 (vX.Y.Z) 所需兼容性变更信息。如果从 vA.B.C 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。
```

Note block punctuation: English uses `**Note:**` (ASCII colon). Chinese uses `**注意：**` (full-width colon inside the bold span).

## Behavior changes

Write each behavior change as a paragraph, not a table row. A complete entry must include:

1. The old behavior: "In earlier versions, ..." / "Before vX.X.X, ..." / "在此前版本中，......"
2. The new behavior starting from this version: "Starting from vX.X.X, ..." / "从 vX.X.X 开始，......"
3. The reason for the change (optional but recommended for significant changes)
4. A documentation link: "For more information, see [documentation](/path.md#anchor)." / "更多信息，请参考[用户文档](/path.md#锚点)。"

Treat the omission of either the old behavior or the new behavior as a defect.

**English example** (from v8.1.0):

```markdown
* In earlier versions, when processing a transaction containing `UPDATE` changes, if the primary key or non-null unique index value is modified in an `UPDATE` event, TiCDC splits this event into `DELETE` and `INSERT` events. In v8.1.0, when using the MySQL sink, TiCDC splits an `UPDATE` event into `DELETE` and `INSERT` events if the transaction `commitTS` for the `UPDATE` change is less than TiCDC `thresholdTS` (which is the current timestamp that TiCDC fetches from PD at TiCDC startup). This behavior change addresses the issue of downstream data inconsistencies caused by the potentially incorrect order of `UPDATE` events received by TiCDC, which can lead to an incorrect order of split `DELETE` and `INSERT` events. For more information, see [documentation](/ticdc/ticdc-split-update-behavior.md#split-update-events-for-mysql-sinks).
```

**Chinese equivalent**:

```markdown
* 在此前版本中，TiCDC 在处理包含 `UPDATE` 变更的事务时，如果 `UPDATE` 事件中主键或非空唯一索引的列值发生改变，TiCDC 会将该条事件拆分为 `DELETE` 和 `INSERT` 两条事件。从 v8.1.0 开始，当使用 MySQL Sink 时，只有当 `UPDATE` 变更的事务 `commitTS` 小于 TiCDC `thresholdTS`（即 TiCDC 在启动时从 PD 获取的当前时间戳）时，TiCDC 才会将 `UPDATE` 事件拆分为 `DELETE` 和 `INSERT` 事件。该行为变更解决了由于 TiCDC 接收到的 `UPDATE` 事件顺序可能不正确而导致的下游数据不一致问题。更多信息，请参考[用户文档](/ticdc/ticdc-split-update-behavior.md#针对-mysql-sink-的-update-事件拆分)。
```

## System variables table

**English**

```markdown
| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`var_name`](/system-variables.md#var_name-new-in-vXYZ) | Deprecated | Starting from vX.Y.Z, ... |
| [`var_name`](/system-variables.md#var_name) | Modified | Changes the default value from `A` to `B`. |
| [`var_name`](/system-variables.md#var_name-new-in-vXYZ) | Newly added | Controls whether ... |
```

**Chinese**

```markdown
| 变量名 | 修改类型 | 描述 |
|--------|------------------------------|------|
| [`var_name`](/system-variables.md#var_name-从-vXYZ-版本开始引入) | 废弃 | 从 vX.Y.Z 起，该变量被废弃。 |
| [`var_name`](/system-variables.md#var_name) | 修改 | 经进一步的测试后，默认值由 `A` 改为 `B`。 |
| [`var_name`](/system-variables.md#var_name-从-vXYZ-版本开始引入) | 新增 | 用于控制是否...... |
```

### Change-type vocabulary

| English | Chinese |
|---------|---------|
| `Newly added` | `新增` |
| `Modified` | `修改` |
| `Deprecated` | `废弃` |
| `Deleted` | `删除` |

Do not use variants such as `New` or `Modify`.

### Anchor suffix convention

For variables that you introduce in this version, include a version suffix in the documentation anchor:

- English: `#var_name-new-in-vXYZ`, for example `#tidb_build_sampling_stats_concurrency-new-in-v750`
- Chinese: `#var_name-从-vXYZ-版本开始引入`, for example `#tidb_build_sampling_stats_concurrency-从-v750-版本开始引入`

For pre-existing variables (not introduced in this version), use no suffix — only `#var_name` in both languages.

Both links point to the same documentation page; only the anchor fragment differs.

## Configuration parameters table

**English**

```markdown
| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`param`](/tidb-configuration-file.md#param-new-in-vXYZ) | Newly added | Controls whether ... The default value is `false`. |
| TiKV | [`raftstore.param`](/tikv-configuration-file.md#param) | Modified | Changes the default value from `"500ms"` to `"100ms"` ... |
| TiCDC | [`sink.param`](/ticdc/ticdc-changefeed-config.md) | Newly added | Controls ... The default value is `true`. |
| TiDB Lightning | `--flag` | Deleted | ... |
```

**Chinese**

```markdown
| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`param`](/tidb-configuration-file.md#param-从-vXYZ-版本开始引入) | 新增 | 控制是否......默认值为 `false`。 |
| TiKV | [`raftstore.param`](/tikv-configuration-file.md#param) | 修改 | 经过算法调优后，默认值由 `"500ms"` 调整为 `"100ms"`。 |
| TiCDC | [`sink.param`](/ticdc/ticdc-changefeed-config.md) | 新增 | 控制......默认值为 `true`。 |
| TiDB Lightning | `--flag` | 删除 | ...... |
```

Configuration file names in the first column are identical in English and Chinese: `TiDB`, `TiKV`, `PD`, `TiFlash`, `TiDB Lightning`, `BR`, `TiCDC`.

## Common review findings

| Finding | Correct |
|---------|---------|
| Change type is "New" | Use `Newly added` (English) or `新增` (Chinese) |
| Change type is "Modify" | Use `Modified` (English) or `修改` (Chinese) |
| Chinese anchor uses the English `-new-in-v750` suffix | Change to `-从-v750-版本开始引入` |
| Behavior change item has no documentation link | Append `For more information, see [documentation](/path.md#anchor).` |
| Behavior change omits old or new behavior | Rewrite to include both |
| Upgrade note says "from the previous version" | Replace with explicit version numbers `vA.B.C` and `vX.Y.Z` |
