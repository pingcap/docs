---
title: FUSE_TAG
summary: テーブルのスナップショットタグを返します。スナップショットタグの詳細については、Snapshot Tags を参照してください。
---

# FUSE_TAG

テーブルのスナップショットタグを返します。スナップショットタグの詳細については、[スナップショットタグ](/tidb-cloud-lake/sql/table-versioning.md#snapshot-tags) を参照してください。

## 構文 {#syntax}

```sql
FUSE_TAG('<database_name>', '<table_name>')
```

## 出力カラム {#output-columns}

| カラム              | 型                   | 説明                                                                        |
|---------------------|----------------------|-----------------------------------------------------------------------------|
| name                | STRING               | タグ名                                                                      |
| snapshot_location   | STRING               | タグが指しているスナップショットファイル                                    |
| expire_at           | TIMESTAMP (nullable) | 有効期限のタイムスタンプ。`CREATE SNAPSHOT TAG` で `RETAIN` を使用した場合に設定されます |

## 例 {#examples}

```sql
SET enable_experimental_table_ref = 1;

CREATE TABLE mytable(a INT, b INT);

INSERT INTO mytable VALUES(1, 1),(2, 2);

-- Create a snapshot tag
ALTER TABLE mytable CREATE TAG v1;

INSERT INTO mytable VALUES(3, 3);

-- Create another tag with expiration
ALTER TABLE mytable CREATE TAG temp RETAIN 2 DAYS;

SELECT * FROM FUSE_TAG('default', 'mytable');

---
| name | snapshot_location                                          | expire_at                  |
|------|------------------------------------------------------------|----------------------------|
| v1   | 1/319/_ss/a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4_v4.mpk        | NULL                       |
| temp | 1/319/_ss/f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3_v4.mpk        | 2025-06-15 10:30:00.000000 |
```