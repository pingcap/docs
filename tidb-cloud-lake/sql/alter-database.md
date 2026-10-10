---
title: ALTER DATABASE
summary: データベース名を変更するか、データベースのデフォルトストレージオプションを設定します。
---

# ALTER DATABASE

データベース名を変更するか、データベースのデフォルトストレージオプションを設定します。

## 構文 {#syntax}

```sql
-- Rename a database
ALTER DATABASE [ IF EXISTS ] <name> RENAME TO <new_db_name>

-- Set default storage options
ALTER DATABASE [ IF EXISTS ] <name> SET OPTIONS (
    DEFAULT_STORAGE_CONNECTION = '<connection_name>'
  | DEFAULT_STORAGE_PATH = '<path>'
)
```

## パラメーター {#parameters}

| パラメーター | 説明 |
|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| `DEFAULT_STORAGE_CONNECTION` | このデータベース内のテーブルに対するデフォルトのストレージ接続として使用する、既存の接続（`CREATE CONNECTION` で作成）の名前です。 |
| `DEFAULT_STORAGE_PATH`       | このデータベース内のテーブルに対するデフォルトのストレージパス URI（例: `s3://bucket/path/`）です。`/` で終わる必要があり、接続のストレージタイプと一致している必要があります。 |

> **Note:**
>
> - `SET OPTIONS` は、この文の実行後に作成されるテーブルにのみ影響します。既存のテーブルは変更されません。
> - もう一方のオプションがすでにデータベースに存在していれば、一度に 1 つのオプションを更新できます。

## 例 {#examples}

### データベース名を変更する {#rename-a-database}

```sql
CREATE DATABASE LAKE;
```

```sql
SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| LAKE           |
| information_schema |
| default            |
| system             |
+--------------------+
```

```sql
ALTER DATABASE `LAKE` RENAME TO `NEW_LAKE`;
```

```sql
SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| NEW_LAKE       |
| default            |
| system             |
+--------------------+
```

### デフォルトのストレージオプションを設定する {#set-default-storage-options}

```sql
ALTER DATABASE analytics SET OPTIONS (
    DEFAULT_STORAGE_CONNECTION = 'my_s3',
    DEFAULT_STORAGE_PATH = 's3://mybucket/analytics_v2/'
);
```

## タグ操作 {#tag-operations}

データベースにタグを割り当てたり削除したりします。タグは事前に [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) で作成しておく必要があります。詳細は [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md) を参照してください。

### 構文 {#syntax}

```sql
ALTER DATABASE [ IF EXISTS ] <name> SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

ALTER DATABASE [ IF EXISTS ] <name> UNSET TAG <tag_name> [, <tag_name> ...]
```

### 例 {#examples}

```sql
ALTER DATABASE mydb SET TAG env = 'prod', owner = 'team_a';
ALTER DATABASE mydb UNSET TAG env, owner;
```