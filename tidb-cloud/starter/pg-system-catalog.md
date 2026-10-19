---
title: PostgreSQL システムカタログ
summary: PostgreSQL 互換の TiDB Cloud Starter でシステムカタログを使用してデータベースオブジェクトを調べる方法を学びます。
---

# PostgreSQL システムカタログ

PostgreSQL 互換の {{{ .starter }}} では、データベース、スキーマ、テーブル、カラム、インデックス、制約、関数、ロール、その他のデータベースオブジェクトを調べるために、`pg_catalog` リレーションと `information_schema` ビューが提供されています。

## `pg_catalog` リレーション {#pg-catalog-relations}

以下の、よく使用される `pg_catalog` リレーションを利用できます。

| リレーション | 説明 |
| --- | --- |
| `pg_tables` | ユーザーテーブル。 |
| `pg_views` | ビュー。 |
| `pg_class` | テーブル、インデックス、シーケンス、およびビュー。 |
| `pg_attribute` | テーブルカラム。 |
| `pg_attrdef` | カラムのデフォルト値。 |
| `pg_namespace` | スキーマ。 |
| `pg_type` | データ型。 |
| `pg_index` | インデックスメタデータ。 |
| `pg_indexes` | `indexdef` を含むインデックス定義。 |
| `pg_constraint` | 主キー、外部キー、check、一意、および not-null 制約。 |
| `pg_proc` | 関数およびプロシージャ。 |
| `pg_trigger` | トリガーメタデータ。 |
| `pg_enum` | Enum 値。 |
| `pg_sequence` | シーケンスメタデータ。 |
| `pg_extension` | データベースに登録された拡張機能。 |
| `pg_collation` | 組み込みの照合順序。 |
| `pg_roles` | データベースロール。 |
| `pg_user` | ログインユーザー。 |
| `pg_auth_members` | ロールメンバーシップ。 |
| `pg_db_role_setting` | ロールごとのセッションパラメータのデフォルト値。 |
| `pg_database` | データベース。 |
| `pg_description` | オブジェクトコメントおよび説明。 |
| `pg_depend` | オブジェクト依存関係メタデータ。 |
| `pg_am` | インデックスアクセスメソッド。 |
| `pg_stat_user_tables` | ユーザーテーブル統計。 |
| `pg_inherits` | テーブル継承メタデータ。 |
| `pg_range` | 範囲型メタデータ。 |
| `pg_opclass` | 演算子クラス。 |
| `pg_policy` | 行レベルセキュリティポリシーのメタデータ。 |
| `pg_policies` | 読み取り可能な行レベルセキュリティポリシー定義。 |
| `pg_settings` | ランタイムパラメータ。 |
| `pg_timezone_names` | タイムゾーン名と UTC オフセット。 |
| `pg_rewrite` | ビューで使用される書き換えルール。 |
| `pg_aggregate` | 集計関数メタデータ。 |

一部のカタログリレーションは、対応する PostgreSQL 機能がサポートされていない場合でも、主に PostgreSQL 互換性のために存在します。カタログリレーションが存在することを、基盤となる PostgreSQL 機能が利用可能である証拠として扱わないでください。

たとえば、レプリケーション関連のカタログオブジェクトが一部存在する場合でも、論理レプリケーションはサポートされていません。 

## `information_schema` ビュー {#information-schema-views}

以下の `information_schema` ビューを利用できます。

| ビュー | 説明 |
| --- | --- |
| `tables` | テーブルおよびビュー。 |
| `columns` | 生成カラムのメタデータを含むテーブルカラム。 |
| `schemata` | スキーマ。 |
| `sequences` | シーケンス。 |
| `routines` | 関数およびプロシージャ。 |
| `table_constraints` | 主キー、外部キー、check、および一意制約。 |
| `key_column_usage` | 主キー、一意、および外部キー制約内のカラム。 |
| `referential_constraints` | 外部キー関係。 |
| `check_constraints` | check 制約。 |
| `constraint_column_usage` | 制約によって参照されるカラム。 |
| `table_privileges` | テーブル権限。 |
| `triggers` | トリガー定義、タイミング、および向き。 |

> **Note:**
>
> `information_schema.views` は利用できません。ビューを一覧表示するには、`pg_views` をクエリするか、`table_type = 'VIEW'` で `information_schema.tables` をフィルタリングしてください。

カラムの NULL 許容性については、`information_schema.columns.is_nullable` または `pg_attribute.attnotnull` を使用してください。

## スキーマ内のテーブルを一覧表示する {#list-tables-in-a-schema}

`pg_tables` を使用します。

```sql
SELECT
    tablename AS table,
    tableowner AS owner,
    hasindexes AS indexed,
    hastriggers AS has_triggers
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

より移植性の高いクエリには、`information_schema.tables` を使用します。

```sql
SELECT
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

## テーブルのカラムを一覧表示する {#list-columns-of-a-table}

`information_schema.columns` を使用します。

```sql
SELECT
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default,
    ordinal_position
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'my_table'
ORDER BY ordinal_position;
```

より低レベルのメタデータについては、`pg_attribute` をクエリします。

```sql
SELECT
    a.attname AS column_name,
    pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
    a.attnotnull AS not_null,
    a.attnum AS position
FROM pg_attribute AS a
JOIN pg_class AS c
    ON c.oid = a.attrelid
JOIN pg_namespace AS n
    ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relname = 'my_table'
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY a.attnum;
```

## テーブルのインデックスを見つける {#find-indexes-on-a-table}

`pg_indexes` を使用します。

```sql
SELECT
    indexname AS index_name,
    indexdef AS definition
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'my_table'
ORDER BY indexname;
```

より詳細なインデックスメタデータについては、次を使用します。

```sql
SELECT
    i.relname AS index_name,
    ix.indisunique AS is_unique,
    ix.indisprimary AS is_primary
FROM pg_index AS ix
JOIN pg_class AS t
    ON t.oid = ix.indrelid
JOIN pg_class AS i
    ON i.oid = ix.indexrelid
JOIN pg_namespace AS n
    ON n.oid = t.relnamespace
WHERE n.nspname = 'public'
  AND t.relname = 'my_table'
ORDER BY i.relname;
```

## テーブル制約を確認する {#check-table-constraints}

一般的な制約を確認するには、`information_schema` を使用します。

```sql
SELECT
    tc.constraint_name,
    tc.constraint_type,
    kcu.column_name,
    cc.check_clause
FROM information_schema.table_constraints AS tc
LEFT JOIN information_schema.key_column_usage AS kcu
    ON kcu.constraint_name = tc.constraint_name
    AND kcu.constraint_schema = tc.constraint_schema
    AND kcu.table_schema = tc.table_schema
    AND kcu.table_name = tc.table_name
LEFT JOIN information_schema.check_constraints AS cc
    ON cc.constraint_name = tc.constraint_name
    AND cc.constraint_schema = tc.constraint_schema
WHERE tc.table_schema = 'public'
  AND tc.table_name = 'my_table'
ORDER BY tc.constraint_type, tc.constraint_name;
```

簡潔な定義を確認するには、`pg_constraint` を使用します。

```sql
SELECT
    conname AS constraint_name,
    contype AS constraint_type,
    pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'public.my_table'::regclass
ORDER BY contype, conname;
```

`pg_constraint` では NOT NULL 制約も確認できます。PostgreSQL 間で移植性の高い方法でカラムの NULL 許容性を確認するには、`information_schema.columns.is_nullable` を使用することを推奨します。

## 外部キーを見つける {#find-foreign-keys}

送信側の外部キーを調べるには、`information_schema` を使用します。

```sql
SELECT
    tc.constraint_name,
    kcu.column_name AS fk_column,
    referenced_kcu.table_name AS referenced_table,
    referenced_kcu.column_name AS referenced_column,
    rc.update_rule,
    rc.delete_rule
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON kcu.constraint_name = tc.constraint_name
    AND kcu.constraint_schema = tc.constraint_schema
    AND kcu.table_schema = tc.table_schema
    AND kcu.table_name = tc.table_name
JOIN information_schema.referential_constraints AS rc
    ON rc.constraint_name = tc.constraint_name
    AND rc.constraint_schema = tc.constraint_schema
JOIN information_schema.key_column_usage AS referenced_kcu
    ON referenced_kcu.constraint_name = rc.unique_constraint_name
    AND referenced_kcu.constraint_schema = rc.unique_constraint_schema
    AND referenced_kcu.ordinal_position = kcu.position_in_unique_constraint
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
  AND tc.table_name = 'my_table'
ORDER BY tc.constraint_name;
```

## 関数とプロシージャを一覧表示する {#list-functions-and-procedures}

`information_schema.routines` を使用します。

```sql
SELECT
    routine_name,
    routine_type,
    data_type AS return_type
FROM information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_name;
```

追加のメタデータを確認するには、`pg_proc` をクエリします。

```sql
SELECT
    p.proname AS function_name,
    format_type(p.prorettype, NULL) AS return_type,
    p.prokind AS kind
FROM pg_proc AS p
JOIN pg_namespace AS n
    ON n.oid = p.pronamespace
WHERE n.nspname = 'public'
ORDER BY p.proname;
```

## ロールと権限を確認する {#inspect-roles-and-privileges}

ロールを一覧表示します。

```sql
SELECT
    rolname,
    rolcanlogin,
    rolinherit,
    rolbypassrls
FROM pg_roles
ORDER BY rolname;
```

テーブル権限を一覧表示します。

```sql
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public'
ORDER BY table_name, grantee, privilege_type;
```

## 行レベルセキュリティを確認する {#inspect-row-level-security}

テーブルのポリシーを一覧表示します。

```sql
SELECT
    policyname AS policy,
    cmd AS command,
    roles AS applies_to,
    qual AS using_expression,
    with_check AS check_expression
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename = 'my_table'
ORDER BY policyname;
```

行レベルセキュリティが有効化されているか、または強制されているかを確認します。

```sql
SELECT
    relname,
    relrowsecurity,
    relforcerowsecurity
FROM pg_class
WHERE oid = 'public.my_table'::regclass;
```

## 拡張機能を確認する {#inspect-extensions}

現在のデータベースに登録されている拡張機能を一覧表示します。

```sql
SELECT
    extname,
    extversion
FROM pg_extension
ORDER BY extname;
```

## システムカタログの互換性 {#system-catalog-compatibility}

PostgreSQL 互換の {{{ .starter }}} は、一般的な PostgreSQL ツールおよびイントロスペクションのワークフローに必要なカタログの表面を実装していますが、カタログの内容やカラムは本家の PostgreSQL と異なる場合があります。

特に、次の点に注意してください。

- 本家の `pg_catalog` または `information_schema` のすべてのリレーションが利用できるわけではありません。
- 一部のカタログリレーションは、基盤となる PostgreSQL 機能がサポートされていない場合でも、互換性のために存在します。
- 一部のカタログリレーションでは、本家の PostgreSQL のカラムの一部のみが公開されています。
- `information_schema.views` は利用できません。
- カスタム照合順序は使用できますが、`pg_collation` には一覧表示されません。
- トリガーのタイミングおよび行/文の向きは、`information_schema.triggers` から確認する必要があります。