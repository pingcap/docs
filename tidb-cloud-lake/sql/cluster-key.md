---
title: クラスターキー
summary: このページでは、{{{ .lake }}} におけるクラスターキー操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。
---

# クラスターキー

このページでは、{{{ .lake }}} におけるクラスターキー操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。

## クラスターキー管理 {#cluster-key-management}

| コマンド | 説明 |
|---------|-------------|
| [SET CLUSTER KEY](/tidb-cloud-lake/sql/set-cluster-key.md) | テーブルのクラスターキーを作成または置き換えます |
| [ALTER CLUSTER KEY](/tidb-cloud-lake/sql/alter-cluster-key.md) | 既存のクラスターキーを変更します |
| [DROP CLUSTER KEY](/tidb-cloud-lake/sql/drop-cluster-key.md) | テーブルからクラスターキーを削除します |
| [RECLUSTER TABLE](/tidb-cloud-lake/sql/recluster-table.md) | クラスターキーに基づいてテーブルデータを再編成します |

## 関連トピック {#related-topics}

- [クラスターキー](/tidb-cloud-lake/guides/cluster-key-performance.md)

> **Note:**
>
> {{{ .lake }}} のクラスターキーは、関連するデータを近接配置することでクエリ性能を向上させるために、テーブル内のデータを物理的に整理するために使用されます。