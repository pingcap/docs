---
title: SET TAG and UNSET TAG
summary: データベースオブジェクトにタグを割り当てる、または削除します。
---

# SET TAG and UNSET TAG

データベースオブジェクトにタグを割り当てる、または削除します。タグを割り当てる前に、[CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) を使用して作成しておく必要があります。

関連情報: [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md)、[TAG_REFERENCES](/tidb-cloud-lake/sql/tag-references.md)。

## 構文 {#syntax}

```sql
-- Assign tags
ALTER { DATABASE | TABLE | VIEW | STAGE | CONNECTION
      | USER | ROLE | STREAM | FUNCTION | PROCEDURE }
    [ IF EXISTS ] <object_name>
    SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

-- Remove tags
ALTER { DATABASE | TABLE | VIEW | STAGE | CONNECTION
      | USER | ROLE | STREAM | FUNCTION | PROCEDURE }
    [ IF EXISTS ] <object_name>
    UNSET TAG <tag_name> [, <tag_name> ...]
```

## サポートされるオブジェクトタイプ {#supported-object-types}

| オブジェクトタイプ | オブジェクト名の形式 | 例 |
|-------------|-------------------|---------|
| DATABASE    | `<database>` | `ALTER DATABASE mydb SET TAG env = 'prod'` |
| TABLE       | `[<database>.]<table>` | `ALTER TABLE mydb.users SET TAG env = 'prod'` |
| VIEW        | `[<database>.]<view>` | `ALTER VIEW mydb.active_users SET TAG env = 'prod'` |
| STAGE       | `<stage>` | `ALTER STAGE my_stage SET TAG env = 'prod'` |
| CONNECTION  | `<connection>` | `ALTER CONNECTION my_conn SET TAG env = 'prod'` |
| USER        | `'<user>'` | `ALTER USER 'alice' SET TAG env = 'prod'` |
| ROLE        | `<role>` | `ALTER ROLE analyst SET TAG env = 'prod'` |
| STREAM      | `[<database>.]<stream>` | `ALTER STREAM mydb.my_stream SET TAG env = 'prod'` |
| FUNCTION    | `<function>` | `ALTER FUNCTION my_udf SET TAG env = 'prod'` |
| PROCEDURE   | `<name>(<arg_types>)` | `ALTER PROCEDURE my_proc(INT) SET TAG env = 'prod'` |

> **Notes:**
>
> - タグに `ALLOWED_VALUES` が設定されている場合、値は許可された値のいずれかである必要があります。
> - 存在しないタグ名に対して `UNSET TAG` を実行するとエラーが返されます。ただし、オブジェクト自体が存在せず、かつ `IF EXISTS` が指定されている場合は除きます。
> - PROCEDURE の場合、オブジェクト名には引数型シグネチャを含める必要があります。

## 例 {#examples}

### データベースとテーブルにタグを付ける {#tag-a-database-and-table}

```sql
CREATE TAG env ALLOWED_VALUES = ('dev', 'staging', 'prod');
CREATE TAG owner;

ALTER DATABASE default SET TAG env = 'prod';
ALTER TABLE default.my_table SET TAG env = 'staging', owner = 'team_a';
```

### stage と connection にタグを付ける {#tag-a-stage-and-connection}

```sql
ALTER STAGE data_stage SET TAG env = 'dev', owner = 'data_team';
ALTER CONNECTION my_s3 SET TAG env = 'prod';
```

### ビューにタグを付ける {#tag-a-view}

```sql
ALTER VIEW default.active_users SET TAG env = 'prod', owner = 'analytics';
```

### ユーザーとロールにタグを付ける {#tag-a-user-and-role}

```sql
ALTER USER 'alice' SET TAG env = 'prod', owner = 'security';
ALTER ROLE analyst SET TAG env = 'dev';
```

### UDF とプロシージャにタグを付ける {#tag-a-udf-and-procedure}

```sql
ALTER FUNCTION my_udf SET TAG env = 'dev';
ALTER PROCEDURE my_proc(DECIMAL(10,2)) SET TAG env = 'prod';
```

### タグを削除する {#remove-tags}

```sql
ALTER TABLE default.my_table UNSET TAG env, owner;
ALTER STAGE data_stage UNSET TAG env;
ALTER USER 'alice' UNSET TAG env, owner;
```