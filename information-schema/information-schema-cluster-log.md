---
title: CLUSTER_LOG
summary: Learn the `CLUSTER_LOG` information_schema table.
---

# CLUSTER_LOG {#cluster-log}

`CLUSTER_LOG`クラスタログテーブルでクラスタログを照会できます。クエリ条件を各インスタンスにプッシュダウンすることにより、クラスタのパフォーマンスに対するクエリの影響は、 `grep`コマンドの影響よりも少なくなります。

v4.0より前のTiDBクラスタのログを取得するには、各インスタンスにログインしてログを要約する必要があります。 4.0のこのクラスタログテーブルは、グローバルで時間順に並べられたログ検索結果を提供します。これにより、フルリンクイベントの追跡が容易になります。たとえば、 `region id`に従ってログを検索することにより、このリージョンのライフサイクル内のすべてのログをクエリできます。同様に、低速ログの`txn id`を介して完全なリンクログを検索することにより、各インスタンスでこのトランザクションによってスキャンされたフローとキーの数を照会できます。

{{< copyable "" >}}

```sql
USE information_schema;
DESC cluster_log;
```

```sql
+----------+------------------+------+------+---------+-------+
| Field    | Type             | Null | Key  | Default | Extra |
+----------+------------------+------+------+---------+-------+
| TIME     | varchar(32)      | YES  |      | NULL    |       |
| TYPE     | varchar(64)      | YES  |      | NULL    |       |
| INSTANCE | varchar(64)      | YES  |      | NULL    |       |
| LEVEL    | varchar(8)       | YES  |      | NULL    |       |
| MESSAGE  | var_string(1024) | YES  |      | NULL    |       |
+----------+------------------+------+------+---------+-------+
5 rows in set (0.00 sec)
```

フィールドの説明：

-   `TIME` ：ログを印刷する時間。
-   `TYPE` ：インスタンスタイプ。オプションの値は`tidb` 、および`pd` `tikv` 。
-   `INSTANCE` ：インスタンスのサービスアドレス。
-   `LEVEL` ：ログレベル。
-   `MESSAGE` ：ログの内容。

> **ノート：**
>
> -   クラスタログテーブルのすべてのフィールドは、実行のために対応するインスタンスにプッシュダウンされます。クラスタログテーブルを使用するオーバーヘッドを減らすには、検索に使用するキーワード、時間範囲、および可能な限り多くの条件を指定する必要があります。たとえば、 `select * from cluster_log where message like '%ddl%' and time > '2020-05-18 20:40:00' and time<'2020-05-18 21:40:00' and type='tidb'` 。
>
> -   `message`フィールドは`like`と`regexp`の正規表現をサポートし、対応するパターンは`regexp`としてエンコードされます。複数の`message`条件を指定することは、 `grep`コマンドの`pipeline`形式と同等です。たとえば、 `select * from cluster_log where message like 'coprocessor%' and message regexp '.*slow.*' and time > '2020-05-18 20:40:00' and time<'2020-05-18 21:40:00'`ステートメントを実行することは、すべてのクラスタインスタンスで`grep 'coprocessor' xxx.log | grep -E '.*slow.*'`を実行することと同じです。

次の例は、 `CLUSTER_LOG`テーブルを使用してDDLステートメントの実行プロセスを照会する方法を示しています。

{{< copyable "" >}}

```sql
SELECT time,instance,left(message,150) FROM cluster_log WHERE message LIKE '%ddl%job%ID.80%' AND type='tidb' AND time > '2020-05-18 20:40:00' AND time < '2020-05-18 21:40:00'
```

```sql
+-------------------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| time                    | instance       | left(message,150)                                                                                                                                      |
+-------------------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| 2020/05/18 21:37:54.784 | 127.0.0.1:4002 | [ddl_worker.go:261] ["[ddl] add DDL jobs"] ["batch count"=1] [jobs="ID:80, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:79, Ro |
| 2020/05/18 21:37:54.784 | 127.0.0.1:4002 | [ddl.go:477] ["[ddl] start DDL job"] [job="ID:80, Type:create table, State:none, SchemaState:none, SchemaID:1, TableID:79, RowCount:0, ArgLen:1, start |
| 2020/05/18 21:37:55.327 | 127.0.0.1:4000 | [ddl_worker.go:568] ["[ddl] run DDL job"] [worker="worker 1, tp general"] [job="ID:80, Type:create table, State:none, SchemaState:none, SchemaID:1, Ta |
| 2020/05/18 21:37:55.381 | 127.0.0.1:4000 | [ddl_worker.go:763] ["[ddl] wait latest schema version changed"] [worker="worker 1, tp general"] [ver=70] ["take time"=50.809848ms] [job="ID:80, Type: |
| 2020/05/18 21:37:55.382 | 127.0.0.1:4000 | [ddl_worker.go:359] ["[ddl] finish DDL job"] [worker="worker 1, tp general"] [job="ID:80, Type:create table, State:synced, SchemaState:public, SchemaI |
| 2020/05/18 21:37:55.786 | 127.0.0.1:4002 | [ddl.go:509] ["[ddl] DDL job is finished"] [jobID=80]                                                                                                  |
+-------------------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
```

上記のクエリ結果は、DDLステートメントを実行するプロセスを示しています。

1.  DDL JOB IDが`80`の要求は、 `127.0.0.1:4002`のTiDBインスタンスに送信されます。
2.  `127.0.0.1:4000`つのTiDBインスタンスがこのDDL要求を処理します。これは、 `127.0.0.1:4000`のインスタンスがその時点でDDL所有者であることを示しています。
3.  DDLJOBIDが`80`の要求が処理されました。
