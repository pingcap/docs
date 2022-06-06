---
title: Create a Data Migration Task
summary: Learn how to create a migration task after the DM cluster is deployed.
---

# データ移行タスクを作成する {#create-a-data-migration-task}

このドキュメントでは、DMクラスタが正常にデプロイされた後に簡単なデータ移行タスクを作成する方法について説明します。

## サンプルシナリオ {#sample-scenario}

このサンプルシナリオに基づいてデータ移行タスクを作成するとします。

-   デプロイが有効になっている2つのMySQLインスタンスと1つのTiDBインスタンスをローカルにデプロイします
-   DMクラスタのDMマスターを使用して、クラスタおよびデータ移行タスクを管理します。

各ノードの情報は以下のとおりです。

| 実例     | サーバーアドレス  | ポート  |
| :----- | :-------- | :--- |
| MySQL1 | 127.0.0.1 | 3306 |
| MySQL2 | 127.0.0.1 | 3307 |
| TiDB   | 127.0.0.1 | 4000 |
| DMマスター | 127.0.0.1 | 8261 |

このシナリオに基づいて、次のセクションでは、データ移行タスクを作成する方法について説明します。

### MySQLのアップストリームを開始します {#start-upstream-mysql}

2つの実行可能なMySQLインスタンスを準備します。 Dockerを使用してMySQLをすばやく起動することもできます。コマンドは次のとおりです。

{{< copyable "" >}}

```bash
docker run --rm --name mysql-3306 -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql:5.7.22 --log-bin=mysql-bin --port=3306 --bind-address=0.0.0.0 --binlog-format=ROW --server-id=1 --gtid_mode=ON --enforce-gtid-consistency=true > mysql.3306.log 2>&1 &
docker run --rm --name mysql-3307 -p 3307:3307 -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql:5.7.22 --log-bin=mysql-bin --port=3307 --bind-address=0.0.0.0 --binlog-format=ROW --server-id=1 --gtid_mode=ON --enforce-gtid-consistency=true > mysql.3307.log 2>&1 &
```

### データを準備する {#prepare-data}

-   サンプルデータをmysql-3306に書き込みます。

    {{< copyable "" >}}

    ```sql
    drop database if exists `sharding1`;
    create database `sharding1`;
    use `sharding1`;
    create table t1 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
    create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
    insert into t1 (id, uid, name) values (1, 10001, 'Gabriel García Márquez'), (2 ,10002, 'Cien años de soledad');
    insert into t2 (id, uid, name) values (3,20001, 'José Arcadio Buendía'), (4,20002, 'Úrsula Iguarán'), (5,20003, 'José Arcadio');
    ```

-   サンプルデータをmysql-3307に書き込みます。

    {{< copyable "" >}}

    ```sql
    drop database if exists `sharding2`;
    create database `sharding2`;
    use `sharding2`;
    create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
    create table t3 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
    insert into t2 (id, uid, name, info) values (6, 40000, 'Remedios Moscote', '{}');
    insert into t3 (id, uid, name, info) values (7, 30001, 'Aureliano José', '{}'), (8, 30002, 'Santa Sofía de la Piedad', '{}'), (9, 30003, '17 Aurelianos', NULL);
    ```

### ダウンストリームTiDBを開始します {#start-downstream-tidb}

TiDBサーバーを実行するには、次のコマンドを使用します。

{{< copyable "" >}}

```bash
wget https://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
tar -xzvf tidb-latest-linux-amd64.tar.gz
mv tidb-latest-linux-amd64/bin/tidb-server ./
./tidb-server
```

> **警告：**
>
> このドキュメントのTiDBの展開方法は、実稼働環境または開発環境に**は適用されません**。

## MySQLデータソースを構成する {#configure-the-mysql-data-source}

データ移行タスクを開始する前に、MySQLデータソースを構成する必要があります。

### パスワードを暗号化する {#encrypt-the-password}

> **ノート：**
>
> -   データベースにパスワードがない場合は、この手順をスキップできます。
> -   プレーンテキストのパスワードを使用して、DMv1.0.6以降のバージョンでソース情報を構成できます。

安全上の理由から、暗号化されたパスワードを構成して使用することをお勧めします。 dmctlを使用して、MySQL/TiDBパスワードを暗号化できます。パスワードが「123456」であるとします。

{{< copyable "" >}}

```bash
./bin/dmctl encrypt "123456"
```

```
fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg=
```

この暗号化された値を保存し、次の手順でMySQLデータソースを作成するために使用します。

### ソース構成ファイルを編集します {#edit-the-source-configuration-file}

次の構成を`conf/source1.yaml`に書き込みます。

```yaml
# MySQL1 Configuration.

source-id: "mysql-replica-01"

# Indicates whether GTID is enabled
enable-gtid: true

from:
  host: "127.0.0.1"
  user: "root"
  password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
  port: 3306
```

MySQL2データソースで、上記の構成を`conf/source2.yaml`にコピーします。 `name`を`mysql-replica-02`に変更し、 `password`と`port`を適切な値に変更する必要があります。

### ソースを作成する {#create-a-source}

dmctlを使用してMySQL1のデータソース構成をDMクラスタにロードするには、ターミナルで次のコマンドを実行します。

{{< copyable "" >}}

```bash
./bin/dmctl --master-addr=127.0.0.1:8261 operate-source create conf/source1.yaml
```

MySQL2の場合、上記のコマンドの構成ファイルをMySQL2の構成ファイルに置き換えます。

## データ移行タスクを作成する {#create-a-data-migration-task}

[作成したデータ](#prepare-data)をインポートした後、MySQL1インスタンスとMySQL2インスタンスの両方にいくつかのシャードテーブルがあります。これらのテーブルの構造は同じで、テーブル名の接頭辞「t」も同じです。これらのテーブルが配置されているデータベースには、すべて「シャーディング」というプレフィックスが付いています。また、主キーまたは一意キーの間に競合はありません（各シャーディングテーブルで、主キーまたは一意キーは他のテーブルのものとは異なります）。

ここで、これらのシャーディングされたテーブルをTiDBの`db_target.t_target`つのテーブルに移行する必要があるとします。手順は次のとおりです。

1.  タスクの構成ファイルを作成します。

    {{< copyable "" >}}

    ```yaml
    ---
    name: test
    task-mode: all
    shard-mode: "pessimistic"
    target-database:
      host: "127.0.0.1"
      port: 4000
      user: "root"
      password: "" # It is recommended to use password encrypted with dmctl if the password is not empty.

    mysql-instances:
      - source-id: "mysql-replica-01"
        block-allow-list:  "instance"  # This configuration applies to DM versions higher than v2.0.0-beta.2. Use black-white-list otherwise.
        route-rules: ["sharding-route-rules-table", "sharding-route-rules-schema"]
        mydumper-thread: 4
        loader-thread: 16
        syncer-thread: 16
      - source-id: "mysql-replica-02"
        block-allow-list:  "instance"  # This configuration applies to DM versions higher than v2.0.0-beta.2. Use black-white-list otherwise.
        route-rules: ["sharding-route-rules-table", "sharding-route-rules-schema"]
        mydumper-thread: 4
        loader-thread: 16
        syncer-thread: 16
    block-allow-list:  # This configuration applies to DM versions higher than v2.0.0-beta.2. Use black-white-list otherwise.
      instance:
        do-dbs: ["~^sharding[\\d]+"]
        do-tables:
        - db-name: "~^sharding[\\d]+"
          tbl-name: "~^t[\\d]+"
    routes:
      sharding-route-rules-table:
        schema-pattern: sharding*
        table-pattern: t*
        target-schema: db_target
        target-table: t_target
      sharding-route-rules-schema:
        schema-pattern: sharding*
        target-schema: db_target
    ```

2.  dmctlを使用してタスクを作成するには、上記の構成を`conf/task.yaml`のファイルに書き込みます。

    {{< copyable "" >}}

    ```bash
    ./bin/dmctl --master-addr 127.0.0.1:8261 start-task conf/task.yaml
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "worker1"
            },
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-02",
                "worker": "worker2"
            }
        ]
    }
    ```

これで、シャーディングされたテーブルをMySQL1およびMySQL2インスタンスからTiDBに移行するタスクが正常に作成されました。

## データを確認する {#verify-data}

アップストリームのMySQLシャードテーブルのデータを変更できます。次に、 [sync-diff-inspector](/sync-diff-inspector/shard-diff.md)を使用して、アップストリームデータとダウンストリームデータに一貫性があるかどうかを確認します。一貫性のあるデータは、移行タスクが適切に機能することを意味します。これは、クラスタが適切に機能することも示します。
