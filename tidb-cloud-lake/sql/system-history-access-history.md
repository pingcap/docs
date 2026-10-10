---
title: system_history.access_history
summary: フィールド base_objects_accessed、objects_modified、および object_modified_by_ddl はいずれも JSON オブジェクトの配列です。各オブジェクトには、以下のフィールドが含まれる場合があります。
---

# system_history.access_history

**データリネージとアクセス制御監査** - クエリによってアクセスまたは変更されたすべてのデータベースオブジェクト（テーブル、カラム、stage）を追跡します。以下の用途に不可欠です。

- **データリネージ**: データベース全体におけるデータフローと依存関係を把握する
- **コンプライアンスレポート**: 誰がいつ機密データにアクセスしたかを追跡する
- **変更管理**: DDL 操作とスキーマ変更を監視する
- **セキュリティ分析**: 異常なアクセスパターンや未承認のデータアクセスを特定する

## フィールド {#fields}

| フィールド              | 型        | 説明                                                                        |
|-------------------------|-----------|-----------------------------------------------------------------------------|
| query_id                | VARCHAR   | クエリの ID。                                                               |
| query_start             | TIMESTAMP | クエリの開始時刻。                                                          |
| user_name               | VARCHAR   | クエリを実行したユーザー名。                                                |
| base_objects_accessed   | VARIANT   | クエリによってアクセスされたオブジェクト。                                  |
| direct_objects_accessed | VARIANT   | 将来の使用のために予約済み。現在は使用されていません。                      |
| objects_modified        | VARIANT   | クエリによって変更されたオブジェクト。                                      |
| object_modified_by_ddl  | VARIANT   | DDL（例: `CREATE TABLE`、`ALTER TABLE`）によって変更されたオブジェクト。    |

`base_objects_accessed`、`objects_modified`、`object_modified_by_ddl` フィールドはいずれも JSON オブジェクトの配列です。各オブジェクトには、以下のフィールドが含まれる場合があります。

- `object_domain`: オブジェクトの種類。[`Database`, `Table`, `Stage`] のいずれかです。
- `object_name`: オブジェクト名。stage の場合は stage 名です。
- `columns`: カラム情報。`object_domain` が `Table` の場合にのみ存在します。
- `stage_type`: stage の種類。`object_domain` が `Stage` の場合にのみ存在します。
- `operation_type`: DDL 操作の種類。[`Create`, `Alter`, `Drop`, `Undrop`] のいずれかです。`object_modified_by_ddl` フィールドにのみ存在します。
- `properties`: DDL 操作の詳細情報。`object_modified_by_ddl` フィールドにのみ存在します。

## 例 {#examples}

```sql
CREATE TABLE t (a INT, b string);
```

次のように記録されます。

```
               query_id: c2c1c7be-cee4-4868-a28e-8862b122c365
            query_start: 2025-06-12 03:31:19.042128
              user_name: root
  base_objects_accessed: []
direct_objects_accessed: []
       objects_modified: []
 object_modified_by_ddl: [{"object_domain":"Table","object_name":"default.default.t","operation_type":"Create","properties":{"columns":[{"column_name":"a","sub_operation_type":"Add"},{"column_name":"b","sub_operation_type":"Add"}],"create_options":{"compression":"zstd","database_id":"1","storage_format":"parquet"}}}]
```

`CREATE TABLE` は DDL 操作であるため、`object_modified_by_ddl` フィールドに記録されます。

```sql
INSERT INTO t VALUES (1, 'book');
```

次のように記録されます。

```
               query_id: e92ebc00-a07e-4138-92a9-ea17a06f0165
            query_start: 2025-06-12 03:31:29.849848
              user_name: root
  base_objects_accessed: []
direct_objects_accessed: []
       objects_modified: [{"columns":[{"column_name":"a"},{"column_name":"b"}],"object_domain":"Table","object_name":"default.default.t"}]
 object_modified_by_ddl: []
```

`INSERT INTO` は DML 操作であるため、`objects_modified` フィールドに記録されます。

```sql
COPY INTO @s FROM t;
```

```
               query_id: 7fd74374-c04a-4989-a6f7-bfe8cc27e511
            query_start: 2025-06-12 03:32:25.682248
              user_name: root
  base_objects_accessed: [{"columns":[{"column_name":"a"},{"column_name":"b"}],"object_domain":"Table","object_name":"default.default.t"}]
direct_objects_accessed: []
       objects_modified: [{"object_domain":"Stage","object_name":"s","stage_type":"Internal"}]
 object_modified_by_ddl: []
```

テーブル `t` から internal stage `s` への `COPY INTO` 操作には、読み取りと書き込みの両方のアクションが含まれます。このクエリの実行後、ソーステーブルは `base_objects_accessed` フィールドに記録され、ターゲット stage は `objects_modified` フィールドに記録されます。