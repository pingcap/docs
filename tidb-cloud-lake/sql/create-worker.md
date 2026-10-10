---
title: CREATE WORKER
summary: オプションのキーと値のリストを指定して worker を作成します。
---

# CREATE WORKER

> **Note:**
>
> v1.3.0 で導入されました。

worker を作成します。

> **Note:**
>
> このコマンドを使用するには、cloud control が有効になっている必要があります。

## 構文 {#syntax}

```sql
CREATE WORKER [ IF NOT EXISTS ] <worker_name>
    [ WITH <option_name> = <option_value> [ , <option_name> = <option_value> ... ] ]
```

## パラメーター {#parameters}

| パラメーター | 説明 |
|-----------|-------------|
| `IF NOT EXISTS` | 任意です。worker がすでに存在する場合、変更を加えずに成功します。 |
| `<worker_name>` | worker 名です。 |
| `<option_name>` | worker オプションのキーです。 |
| `<option_value>` | worker オプションの値です。 |

## オプション {#options}

{{{ .lake }}} は、単一の `WITH` 句と、それに続くカンマ区切りのオプションリストを受け付けます。一般的な worker オプションは次のとおりです。

| オプション | 値の例 | 説明 |
|--------|---------------|-------------|
| `size` | `'small'` | worker のコンピュートサイズを制御します。 |
| `auto_suspend` | `'300'` | 自動サスペンドまでのアイドルタイムアウトです。 |
| `auto_resume` | `'true'` | worker を自動的に再開するかどうかを制御します。 |
| `max_cluster_count` | `'3'` | オートスケーリングするクラスター数の上限です。 |
| `min_cluster_count` | `'1'` | オートスケーリングするクラスター数の下限です。 |

- `WITH` は最大 1 回だけ指定できます。
- オプションはカンマで区切ります。
- オプション名は、リクエスト送信前に小文字へ正規化されます。
- `option_value` は、文字列リテラル、裸の識別子、符号なし整数、または boolean として記述できます。
- `CREATE WORKER` は `TAG` 句をサポートしていません。

## 例 {#examples}

オプションなしで worker を作成します。

```sql
CREATE WORKER read_env;
```

`IF NOT EXISTS` を指定して worker を作成します。

```sql
CREATE WORKER IF NOT EXISTS read_env;
```

カスタムオプションを指定して worker を作成します。

```sql
CREATE WORKER IF NOT EXISTS read_env
WITH size = 'small',
     auto_suspend = '300',
     auto_resume = 'true',
     max_cluster_count = '3',
     min_cluster_count = '1';
```

## 関連トピック {#related-topics}

- [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) - worker のタグ、オプション、または状態を変更します
- [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) - worker とそのメタデータを一覧表示します
- [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) - worker を削除します