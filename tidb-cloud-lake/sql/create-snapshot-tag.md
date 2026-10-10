---
title: CREATE SNAPSHOT TAG
summary: FUSE テーブルに名前付きスナップショットタグを作成し、テーブル履歴内の特定時点をブックマークしてクエリできるようにします。
---

# CREATE SNAPSHOT TAG

FUSE テーブルに名前付きスナップショットタグを作成します。スナップショットタグは、テーブルの特定時点の状態をブックマークするもので、後からその状態を [AT](/tidb-cloud-lake/sql/at.md) 句でクエリできます。

> **Note:**
>
> - これは**実験的**機能です。使用する前に、まず有効にしてください: `SET enable_experimental_table_ref = 1;`。
> - FUSE engine テーブルでのみサポートされます。Memory engine テーブルおよび一時テーブルはサポートされません。

## 構文 {#syntax}

```sql
ALTER TABLE [<database_name>.]<table_name> CREATE TAG <tag_name>
    [ AT (
        SNAPSHOT => '<snapshot_id>' |
        TIMESTAMP => <timestamp> |
        STREAM => <stream_name> |
        OFFSET => <time_interval> |
        TAG => <tag_name>
    ) ]
    [ RETAIN <n> { DAYS | SECONDS } ]
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| tag_name  | タグの名前です。テーブル内で一意である必要があります。 |
| AT        | タグが参照するスナップショットを指定します。省略した場合、タグは現在の（最新の）スナップショットを参照します。[AT](/tidb-cloud-lake/sql/at.md) 句と同じオプションに加えて、既存のタグからコピーするための `TAG` もサポートします。 |
| RETAIN    | 自動有効期限を設定します。指定した期間が経過すると、次回の [VACUUM](/tidb-cloud-lake/sql/vacuum-table.md) 操作中にタグが削除されます。`RETAIN` を指定しない場合、明示的に削除されるまでタグは保持されます。 |

## 例 {#examples}

### 現在のスナップショットにタグを付ける {#tag-the-current-snapshot}

```sql
SET enable_experimental_table_ref = 1;

CREATE TABLE t1(a INT, b STRING);
INSERT INTO t1 VALUES (1, 'a'), (2, 'b'), (3, 'c');

-- Create a tag at the current snapshot
ALTER TABLE t1 CREATE TAG v1_0;

-- Insert more data
INSERT INTO t1 VALUES (4, 'd'), (5, 'e');

-- Query the tagged snapshot (returns 3 rows, not 5)
SELECT * FROM t1 AT (TAG => v1_0) ORDER BY a;
```

### 既存の参照からタグを作成する {#tag-from-an-existing-reference}

```sql
-- Copy from an existing tag
ALTER TABLE t1 CREATE TAG v1_0_copy AT (TAG => v1_0);

-- Tag a specific snapshot
ALTER TABLE t1 CREATE TAG before_migration
    AT (SNAPSHOT => 'aaa4857c5935401790db2c9f0f2818be');

-- Tag the state from 1 hour ago
ALTER TABLE t1 CREATE TAG hourly_checkpoint AT (OFFSET => -3600);
```

### 自動有効期限付きのタグ {#tag-with-automatic-expiration}

```sql
-- Tag expires after 7 days
ALTER TABLE t1 CREATE TAG temp_tag RETAIN 7 DAYS;

-- Tag expires after 3600 seconds
ALTER TABLE t1 CREATE TAG debug_snapshot RETAIN 3600 SECONDS;
```