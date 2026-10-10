---
title: SHOW WORKERS
summary: SHOW WORKERS を使用して、worker とそのメタデータを一覧表示します。
---

# SHOW WORKERS

> **Note:**
>
> v1.3.0 で導入されました。

現在のテナント内の worker を一覧表示します。

> **Note:**
>
> このコマンドを使用するには、cloud control が有効になっている必要があります。

## 構文 {#syntax}

```sql
SHOW WORKERS
```

## 出力 {#output}

`SHOW WORKERS` は、次のカラムを返します。

| カラム | 説明 |
|--------|-------------|
| `name` | worker 名 |
| `tags` | JSON 形式の worker タグ |
| `options` | JSON 形式の worker オプション |
| `created_at` | worker の作成タイムスタンプ |
| `updated_at` | worker の更新タイムスタンプ |

## 例 {#examples}

```sql
SHOW WORKERS;
```

出力例:

```text
read_env,{},"{""auto_resume"":""true"",""auto_suspend"":""300"",""max_cluster_count"":""3"",""min_cluster_count"":""1"",""size"":""small""}",2026-04-23T11:40:27.942797+00:00,2026-04-23T11:40:27.942797+00:00
```

## 関連トピック {#related-topics}

- [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) - worker を作成します
- [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) - worker のタグ、オプション、または状態を変更します
- [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) - worker を削除します