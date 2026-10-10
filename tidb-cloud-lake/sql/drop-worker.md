---
title: DROP WORKER
summary: DROP WORKER を使用して worker を削除します。
---

# DROP WORKER

> **Note:**
>
> v1.3.0 で導入されました。

worker を削除します。

> **Note:**
>
> このコマンドを使用するには、cloud control が有効になっている必要があります。

## 構文 {#syntax}

```sql
DROP WORKER [ IF EXISTS ] <worker_name>
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| `IF EXISTS` | 任意。worker が存在しない場合のエラーを抑制します。 |
| `<worker_name>` | worker 名です。 |

## 例 {#examples}

```sql
DROP WORKER read_env;
```

```sql
DROP WORKER IF EXISTS read_env;
```

## 関連トピック {#related-topics}

- [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) - worker を作成します
- [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) - worker のタグ、オプション、または状態を変更します
- [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) - worker とそのメタデータを一覧表示します