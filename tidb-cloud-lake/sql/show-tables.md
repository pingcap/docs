---
title: SHOW TABLES
summary: 現在または指定したデータベース内のテーブルを一覧表示します。
---

# SHOW TABLES

現在または指定したデータベース内のテーブルを一覧表示します。

> **Note:**
>
> バージョン 1.2.415 以降、SHOW TABLES コマンドの結果にはビューが含まれなくなりました。ビューを表示するには、代わりに [SHOW VIEWS](/tidb-cloud-lake/sql/show-views.md) を使用してください。

関連情報: [system.tables](/tidb-cloud-lake/sql/system-tables.md)

## 構文 {#syntax}

```sql
SHOW [ FULL ] TABLES
     [ {FROM | IN} <database_name> ]
     [ HISTORY ]
     [ LIKE '<pattern>' | WHERE <expr> ]
```

| パラメーター | 説明                                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| FULL      | 追加情報を含めて結果を一覧表示します。詳細は [例](#examples) を参照してください。                                  |
| FROM / IN | データベースを指定します。省略した場合、このコマンドは現在のデータベースの結果を返します。                                |
| HISTORY   | 保持期間内（デフォルトでは 24 時間）のテーブル削除時刻を表示します。テーブルがまだ削除されていない場合、`drop_time` の値は NULL です。 |
| LIKE      | 大文字と小文字を区別するパターンマッチングを使用して、名前で結果を絞り込みます。                                                   |
| WHERE     | WHERE 句の式を使用して結果を絞り込みます。                                                                |

## 例 {#examples}

次の例は、現在のデータベース（default）内のすべてのテーブル名を一覧表示します。

```sql
SHOW TABLES;

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ books             │
│ mytable           │
│ ontime            │
│ products          │
└───────────────────┘
```

次の例は、追加情報を含めてすべてのテーブルを一覧表示します。

```sql
SHOW FULL TABLES;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  tables  │ table_type │ database │ catalog │       owner      │ engine │ cluster_by │         create_time        │     num_rows     │     data_size    │ data_compressed_size │    index_size    │
├──────────┼────────────┼──────────┼─────────┼──────────────────┼────────┼────────────┼────────────────────────────┼──────────────────┼──────────────────┼──────────────────────┼──────────────────┤
│ books    │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:53:15.354132 │                0 │                0 │                    0 │                0 │
│ mytable  │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:53:27.968505 │                0 │                0 │                    0 │                0 │
│ ontime   │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:53:42.052399 │                0 │                0 │                    0 │                0 │
│ products │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:54:00.883985 │                0 │                0 │                    0 │                0 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

次の例は、省略可能な HISTORY パラメーターが指定されている場合、結果に削除済みテーブルが含まれることを示しています。

```sql
DROP TABLE products;

SHOW TABLES;

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ books             │
│ mytable           │
│ ontime            │
└───────────────────┘

SHOW TABLES HISTORY;

┌────────────────────────────────────────────────┐
│ Tables_in_default │          drop_time         │
├───────────────────┼────────────────────────────┤
│ books             │ NULL                       │
│ mytable           │ NULL                       │
│ ontime            │ NULL                       │
│ products          │ 2024-01-16 03:55:47.900362 │
└────────────────────────────────────────────────┘
```

次の例は、名前の末尾に文字列 "time" を含むテーブルを一覧表示します。

```sql
SHOW TABLES LIKE '%time';

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ ontime            │
└───────────────────┘

-- CASE-SENSITIVE pattern matching.
-- No results will be returned if you code the previous statement like this:
SHOW TABLES LIKE '%TIME';
```

次の例は、データサイズが 1,000 バイトを超えるテーブルを一覧表示します。

```sql
SHOW TABLES WHERE data_size > 1000 ;

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ ontime            │
└───────────────────┘
```