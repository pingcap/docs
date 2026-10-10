---
title: system.clusters
summary: クラスター ノードに関する情報を含みます。
---

# system.clusters

クラスター ノードに関する情報を含みます。

> **Note:**
>
> `clusters` テーブルへのアクセスは、設定オプション `disable_system_table_load` を使用して無効化できます。
>
> たとえば、{{{ .lake }}} ユーザーはこのテーブルを表示できません。

```sql
SELECT * FROM system.clusters;
+------------------------+---------+------+
| name                   | host    | port |
+------------------------+---------+------+
| 2KTgGnTDuKHw3wu9CCVIf6 | 0.0.0.0 | 9093 |
| bZTEWpQGLwRgcRyHre1xL3 | 0.0.0.0 | 9092 |
| plhQlHvVfT0p1T5QdnvhC4 | 0.0.0.0 | 9091 |
+------------------------+---------+------+
```