---
title: REFRESH LINEAGE
summary: "{{{ .lake }}} 内の既存のビューに対してリネージをバックフィルまたは整合します。"
---

# REFRESH LINEAGE

`default` catalog 内の既存のビューに対して、リネージをバックフィルまたは整合します。ビューがすでに含まれているデプロイでデータリネージを有効化した後に、このコマンドを使用します。リネージ有効化後に作成されたビューは自動的に追跡されます。

このコマンドを実行するには、グローバルな `SUPER` 権限が必要であり、リネージが有効になっている必要があります。[Data Lineage](/tidb-cloud-lake/guides/data-lineage.md#enable-data-lineage) を参照してください。

## 構文 {#syntax}

```sql
REFRESH LINEAGE FOR ALL VIEWS [ DRY RUN ]
```

`DRY RUN` は、変更内容を計算して報告しますが、書き込みは行いません。まずこれを実行して、リフレッシュによって実施される内容を確認してください。

## 出力カラム {#output-columns}

| カラム | 説明 |
|--------|-------------|
| `object_domain` | オブジェクトドメイン。現在は `VIEW` です。 |
| `catalog` | ビューを含む catalog。現在は `default` です。 |
| `database` | ビューを含むデータベース。 |
| `object_name` | ビュー名。 |
| `status` | `DRY_RUN`、`REFRESHED`、または `ERROR`。 |
| `edge_count` | 現在のビュー定義で見つかったリネージエッジの数。 |
| `upsert_count` | 追加または更新が必要な、不足または変更されたエッジの数。 |
| `delete_count` | 削除する古いエッジの数。 |
| `error` | `status` が `ERROR` の場合のエラー詳細。それ以外は `NULL`。 |

変更のない成功したビューは、結果に含まれません。

## 例 {#examples}

既存のビューに必要な変更をプレビューします。

```sql
REFRESH LINEAGE FOR ALL VIEWS DRY RUN;
```

変更を適用します。

```sql
REFRESH LINEAGE FOR ALL VIEWS;
```

コマンドの完了後、[`GET_LINEAGE`](/tidb-cloud-lake/sql/get-lineage.md) を使用してビューの上流リネージをクエリします。

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

> **Note:**
>
> 論理ビュー定義を変更するには、[`CREATE OR REPLACE VIEW`](/tidb-cloud-lake/sql/create-view.md) を使用してください。`ALTER VIEW ... AS ...` はサポートされていません。これは、ビューを再作成せずに定義を変更すると、永続化されたリネージの整合性が失われる可能性があるためです。