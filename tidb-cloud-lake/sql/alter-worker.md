---
title: ALTER WORKER
summary: ALTER WORKER を使用して worker のタグ、オプション、または状態を変更します。
---

# ALTER WORKER

> **Note:**
>
> v1.3.0 で導入されました。

worker のタグ、オプション、または状態を変更します。

> **Note:**
>
> このコマンドを使用するには、cloud control を有効にする必要があります。

## 構文 {#syntax}

```sql
ALTER WORKER <worker_name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER WORKER <worker_name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER WORKER <worker_name> SET <option_name> = <option_value> [ , <option_name> = <option_value> ... ]

ALTER WORKER <worker_name> UNSET <option_name> [ , <option_name> ... ]

ALTER WORKER <worker_name> SUSPEND

ALTER WORKER <worker_name> RESUME
```

## パラメーター {#parameters}

| Form | 説明 |
|------|-------------|
| `SET TAG` | worker タグを追加または更新します。タグ値は文字列リテラルである必要があります。 |
| `UNSET TAG` | 1 つ以上の worker タグを削除します。 |
| `SET` | worker オプションを追加または更新します。オプション名は小文字に正規化されます。 |
| `UNSET` | 1 つ以上の worker オプションを削除します。 |
| `SUSPEND` | worker を一時停止します。 |
| `RESUME` | worker を再開します。 |

## 例 {#examples}

worker にタグを設定します。

```sql
ALTER WORKER read_env
SET TAG purpose = 'sandbox', owner = 'ci';
```

worker オプションを更新します。

```sql
ALTER WORKER read_env
SET size = 'medium', auto_suspend = '600';
```

タグとオプションを削除します。

```sql
ALTER WORKER read_env UNSET TAG owner;
ALTER WORKER read_env UNSET auto_suspend;
```

worker の状態を変更します。

```sql
ALTER WORKER read_env SUSPEND;
ALTER WORKER read_env RESUME;
```

## 関連トピック {#related-topics}

- [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) - worker を作成します
- [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) - worker とそのメタデータを一覧表示します
- [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) - worker を削除します