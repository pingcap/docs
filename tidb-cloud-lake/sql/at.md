---
title: AT
summary: AT 句を使用すると、snapshot ID、timestamp、stream 名、または時間間隔を指定して、データの以前のバージョンを取得できます。
---

# AT

AT 句を使用すると、snapshot ID、timestamp、stream 名、または時間間隔を指定して、データの以前のバージョンを取得できます。

{{{ .lake }}} はデータ更新が発生すると自動的に snapshot を作成するため、snapshot は過去のある時点におけるデータのビューと見なせます。snapshot には、snapshot ID または snapshot が作成された timestamp を使ってアクセスできます。snapshot ID と timestamp の取得方法については、[snapshot ID と timestamp の取得](#obtaining-snapshot-id-and-timestamp)を参照してください。

これは {{{ .lake }}} の Time Travel 機能の一部であり、保持期間内（デフォルトでは 24 時間）であれば、データの以前のバージョンに対してクエリ、バックアップ、リストアを実行できます。

## 構文 {#syntax}

```sql
SELECT ...
FROM ...
AT (
       SNAPSHOT => '<snapshot_id>' |
       TIMESTAMP => <timestamp> |
       STREAM => <stream_name> |
       OFFSET => <time_interval>
   )
```

| パラメータ | 説明 |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SNAPSHOT  | 以前のデータをクエリする対象となる特定の snapshot ID を指定します。 |
| TIMESTAMP | データを取得する特定の timestamp を指定します。 |
| STREAM    | 指定した stream が作成された時点のデータをクエリすることを示します。 |
| OFFSET    | 現在時刻からさかのぼる秒数を指定します。負の整数の形式で指定する必要があり、その絶対値が秒単位の時間差を表します。たとえば、`-3600` は 1 時間（3,600 秒）過去にさかのぼることを表します。 |
| TAG       | `ALTER TABLE ... CREATE TAG` で作成した名前付きタグを指定し、そのタグに関連付けられた snapshot をクエリします。これは実験的機能であり、`SET enable_experimental_table_ref = 1` が必要です。[スナップショットタグ操作](/tidb-cloud-lake/sql/alter-table.md#snapshot-tag-operations) を参照してください。 |

## snapshot ID と timestamp の取得 {#obtaining-snapshot-id-and-timestamp}

テーブルのすべての snapshot の snapshot ID と timestamp を返すには、[FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md) 関数を使用します。

```sql
SELECT snapshot_id,
       timestamp
FROM   FUSE_SNAPSHOT('<database_name>', '<table_name>');
```

## 例 {#examples}

この例では、AT 句を使用して、snapshot ID、timestamp、stream に基づいて以前のデータバージョンを取得する方法を示します。

1. `a` という 1 つのカラムを持つ `t` という名前のテーブルを作成し、値 1 と 2 の 2 行をテーブルに挿入します。

    ```sql
    CREATE TABLE t(a INT);

    INSERT INTO t VALUES(1);
    INSERT INTO t VALUES(2);
    ```

2. テーブル `t` に対して `s` という名前の stream を作成し、値 3 の行をさらに 1 行テーブルに追加します。

    ```sql
    CREATE STREAM s ON TABLE t;

    INSERT INTO t VALUES(3);
    ```

3. Time Travel クエリを実行して、以前のデータバージョンを取得します。

```sql
-- Return snapshot IDs and corresponding timestamps for table 't'
SELECT snapshot_id, timestamp FROM FUSE_SNAPSHOT('default', 't');
┌───────────────────────────────────────────────────────────────┐
│            snapshot_id           │          timestamp         │
├──────────────────────────────────┼────────────────────────────┤
│ 296349da841d4fa8820bbf8e228d75f3 │ 2024-04-02 15:25:21.456574 │
│ aaa4857c5935401790db2c9f0f2818be │ 2024-04-02 15:19:02.484304 │
│ e66ad2bc3f21416e87903dc9cd0388a3 │ 2024-04-02 15:18:40.766361 │
└───────────────────────────────────────────────────────────────┘

-- These queries retrieve the same data but using different methods:
-- by snapshot_id:
SELECT * FROM t AT (SNAPSHOT => 'aaa4857c5935401790db2c9f0f2818be');
-- by timestamp:
SELECT * FROM t AT (TIMESTAMP => '2024-04-02 15:19:02.484304'::TIMESTAMP);
-- by stream:
SELECT * FROM t AT (STREAM => s);

┌─────────────────┐
│        a        │
├─────────────────┤
│               1 │
│               2 │
└─────────────────┘

-- Retrieve all columns from table 't' with data from 60 seconds ago
SELECT * FROM t AT (OFFSET => -60);
```