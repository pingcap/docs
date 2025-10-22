---
title: CLUSTER_INFO
summary: CLUSTER_INFO` クラスター トポロジ情報テーブルについて学習します。
---

# クラスター情報 {#cluster-info}

`CLUSTER_INFO`クラスター トポロジ テーブルには、クラスターの現在のトポロジ情報、各インスタンスのバージョン情報、インスタンス バージョンに対応する Git ハッシュ、各インスタンスの開始時刻、および各インスタンスの実行時刻が示されます。

> **注記：**
>
> このテーブルはクラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では使用できません。

```sql
USE information_schema;
desc cluster_info;
```

```sql
+----------------+-------------+------+------+---------+-------+
| Field          | Type        | Null | Key  | Default | Extra |
+----------------+-------------+------+------+---------+-------+
| TYPE           | varchar(64) | YES  |      | NULL    |       |
| INSTANCE       | varchar(64) | YES  |      | NULL    |       |
| STATUS_ADDRESS | varchar(64) | YES  |      | NULL    |       |
| VERSION        | varchar(64) | YES  |      | NULL    |       |
| GIT_HASH       | varchar(64) | YES  |      | NULL    |       |
| START_TIME     | varchar(32) | YES  |      | NULL    |       |
| UPTIME         | varchar(32) | YES  |      | NULL    |       |
| SERVER_ID      | bigint(21)  | YES  |      | NULL    |       |
+----------------+-------------+------+------+---------+-------+
8 rows in set (0.01 sec)
```

フィールドの説明:

-   `TYPE` : インスタンスタイプ。オプションの値は`tidb` 、 `pd` 、 `tikv`です。
-   `INSTANCE` : インスタンス アドレス`IP:PORT`の形式の文字列です。
-   `STATUS_ADDRESS` : HTTP APIのサービスアドレス。tikv-ctl、pd-ctl、tidb-ctlの一部のコマンドはこのAPIとこのアドレスを使用する場合があります。また、このアドレスを使用して、クラスターの詳細情報を取得することもできます。詳細は[TiDB HTTP API ドキュメント](https://github.com/pingcap/tidb/blob/release-8.5/docs/tidb_http_api.md)を参照してください。
-   `VERSION` : 対応するインスタンスのセマンティックバージョン番号。MySQLのバージョン番号との互換性を保つため、TiDBのバージョンは`${mysql-version}-${tidb-version}`の形式で表示されます。
-   `GIT_HASH` : インスタンス バージョンをコンパイルするときの Git コミット ハッシュ。2 つのインスタンスが完全に一貫したバージョンであるかどうかを識別するために使用されます。
-   `START_TIME` : 対応するインスタンスの開始時刻。
-   `UPTIME` : 対応するインスタンスの稼働時間。
-   `SERVER_ID` : 対応するインスタンスのサーバーID。

```sql
SELECT * FROM cluster_info;
```

```sql
+------+-----------------+-----------------+--------------+------------------------------------------+---------------------------+---------------------+
| TYPE | INSTANCE        | STATUS_ADDRESS  | VERSION      | GIT_HASH                                 | START_TIME                | UPTIME              |
+------+-----------------+-----------------+--------------+------------------------------------------+---------------------------+---------------------+
| tidb | 0.0.0.0:4000    | 0.0.0.0:10080   | 4.0.0-beta.2 | 0df3b74f55f8f8fbde39bbd5d471783f49dc10f7 | 2020-07-05T09:25:53-06:00 | 26h39m4.352862693s  |
| pd   | 127.0.0.1:2379  | 127.0.0.1:2379  | 4.1.0-alpha  | 1ad59bcbf36d87082c79a1fffa3b0895234ac862 | 2020-07-05T09:25:47-06:00 | 26h39m10.352868103s |
| tikv | 127.0.0.1:20165 | 127.0.0.1:20180 | 4.1.0-alpha  | b45e052df8fb5d66aa8b3a77b5c992ddbfbb79df | 2020-07-05T09:25:50-06:00 | 26h39m7.352869963s  |
+------+-----------------+-----------------+--------------+------------------------------------------+---------------------------+---------------------+
3 rows in set (0.00 sec)
```
