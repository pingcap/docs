---
title: CLUSTER_LOG
summary: CLUSTER_LOG` information_schema テーブルについて学習します。
---

# クラスターログ {#cluster-log}

クラスターログテーブル`CLUSTER_LOG`に対してクラスターログのクエリを実行できます。クエリ条件を各インスタンスにプッシュダウンすることで、クエリがクラスターのパフォーマンスに与える影響は、コマンド`grep`よりも小さくなります。

> **注記：**
>
> このテーブルは TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

TiDBクラスターv4.0より前のログを取得するには、各インスタンスにログインしてログを要約する必要がありました。v4.0のこのクラスターログテーブルは、グローバルかつ時系列のログ検索結果を提供するため、フルリンクイベントの追跡が容易になります。例えば、 `region id`でログを検索すると、このリージョンのライフサイクル内のすべてのログを照会できます。同様に、スローログの`txn id`でフルリンクログを検索すると、各インスタンスでこのトランザクションによってスキャンされたフローとキーの数を照会できます。

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

フィールドの説明:

-   `TIME` : ログを印刷する時間。
-   `TYPE` : インスタンスタイプ。オプションの値は`tidb` 、 `pd` 、 `tikv`です。
-   `INSTANCE` : インスタンスのサービス アドレス。
-   `LEVEL` : ログレベル。
-   `MESSAGE` : ログの内容。

> **注記：**
>
> -   クラスターログテーブルのすべてのフィールドは、対応するインスタンスにプッシュダウンされて実行されます。クラスターログテーブルの使用に伴うオーバーヘッドを削減するには、検索に使用するキーワード、時間範囲、そして可能な限り多くの条件を指定する必要があります。例えば、 `select * from cluster_log where message like '%ddl%' and time > '2020-05-18 20:40:00' and time<'2020-05-18 21:40:00' and type='tidb'`に指定します。
>
> -   `message`フィールドは`like`と`regexp`正規表現をサポートしており、対応するパターンは`regexp`としてエンコードされます。複数の`message`条件を指定すると、 `grep`コマンドの`pipeline`形式と同じになります。例えば、 `select * from cluster_log where message like 'coprocessor%' and message regexp '.*slow.*' and time > '2020-05-18 20:40:00' and time<'2020-05-18 21:40:00'`ステートメントを実行すると、すべてのクラスターインスタンスで`grep 'coprocessor' xxx.log | grep -E '.*slow.*'`実行するのと同じになります。

次の例は、 `CLUSTER_LOG`テーブルを使用して DDL ステートメントの実行プロセスをクエリする方法を示しています。

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

上記のクエリ結果は、DDL ステートメントを実行するプロセスを示しています。

1.  DDL JOB ID が`80`のリクエストが`127.0.0.1:4002` TiDB インスタンスに送信されます。
2.  `127.0.0.1:4000` TiDB インスタンスがこの DDL 要求を処理します。これは、 `127.0.0.1:4000`のインスタンスがその時点で DDL 所有者であることを示します。
3.  DDL JOB ID が`80`のリクエストが処理されました。
