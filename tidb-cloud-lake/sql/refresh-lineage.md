---
title: REFRESH LINEAGE
summary: 为 {{{ .lake }}} 中现有视图回填或协调 lineage。
---

# REFRESH LINEAGE

为 `default` catalog 中的现有视图回填或协调 lineage。在已包含视图的部署上启用 data lineage 后，请使用此命令。启用 lineage 后新创建的视图会被自动跟踪。

此命令需要全局 `SUPER` 权限，并且必须已启用 lineage。参见[数据 lineage](/tidb-cloud-lake/guides/data-lineage.md#enable-data-lineage)。

## 语法 {#syntax}

```sql
REFRESH LINEAGE FOR ALL VIEWS [ DRY RUN ]
```

`DRY RUN` 会计算并报告变更，但不会将其写入。建议先运行它，以查看执行 refresh 时将进行的操作。

## 输出列 {#output-columns}

| 列 | 描述 |
|--------|-------------|
| `object_domain` | 对象域；当前为 `VIEW`。 |
| `catalog` | 包含该视图的 catalog；当前为 `default`。 |
| `database` | 包含该视图的数据库。 |
| `object_name` | 视图名称。 |
| `status` | `DRY_RUN`、`REFRESHED` 或 `ERROR`。 |
| `edge_count` | 在当前视图定义中找到的 lineage 边数量。 |
| `upsert_count` | 需要新增或修改的缺失或已变更边数量。 |
| `delete_count` | 需要删除的过期边数量。 |
| `error` | 当 `status` 为 `ERROR` 时的错误详情；否则为 `NULL`。 |

对于成功且无变更的视图，结果中不会显示。

## 示例 {#examples}

预览现有视图所需的变更：

```sql
REFRESH LINEAGE FOR ALL VIEWS DRY RUN;
```

应用这些变更：

```sql
REFRESH LINEAGE FOR ALL VIEWS;
```

命令完成后，可使用 [`GET_LINEAGE`](/tidb-cloud-lake/sql/get-lineage.md) 查询某个视图的上游 lineage：

```sql
SELECT
    distance,
    source_object_database,
    source_object_name,
    target_object_database,
    target_object_name
FROM GET_LINEAGE(
    'lineage_demo.sales_view',
    'VIEW',
    'UPSTREAM',
    1
);
```

> **注意：**
>
> 如需修改逻辑视图定义，请使用 [`CREATE OR REPLACE VIEW`](/tidb-cloud-lake/sql/create-view.md)。不支持 `ALTER VIEW ... AS ...`，因为在不重建视图的情况下修改定义，可能会导致持久化的 lineage 不一致。