---
title: Create a Data Migration Task
summary: DM クラスターがデプロイされた後に移行タスクを作成する方法を学習します。
---

# データ移行タスクを作成する {#create-a-data-migration-task}

このドキュメントでは、DM クラスターが正常にデプロイされた後に、簡単なデータ移行タスクを作成する方法について説明します。

## サンプルシナリオ {#sample-scenario}

次のサンプル シナリオに基づいてデータ移行タスクを作成するとします。

-   binlogを有効にした 2 つの MySQL インスタンスと 1 つの TiDB インスタンスをローカルにデプロイ
-   DM クラスターの DM マスターを使用して、クラスターとデータ移行タスクを管理します。

各ノードの情報は以下の通りです。

| 実例     | サーバーアドレス  | ポート  |
| :----- | :-------- | :--- |
| MySQL1 | 127.0.0.1 | 3306 |
| MySQL2 | 127.0.0.1 | 3307 |
| TiDB   | 127.0.0.1 | 4000 |
| DMマスター | 127.0.0.1 | 8261 |

このシナリオに基づいて、次のセクションではデータ移行タスクを作成する方法について説明します。

### アップストリームMySQLを起動する {#start-upstream-mysql}

実行可能なMySQLインスタンスを2つ用意します。Dockerを使ってMySQLを素早く起動することもできます。コマンドは以下のとおりです。

```bash
docker run --rm --name mysql-3306 -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql:5.7.22 --log-bin=mysql-bin --port=3306 --bind-address=0.0.0.0 --binlog-format=ROW --server-id=1 --gtid_mode=ON --enforce-gtid-consistency=true > mysql.3306.log 2>&1 &
docker run --rm --name mysql-3307 -p 3307:3307 -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql:5.7.22 --log-bin=mysql-bin --port=3307 --bind-address=0.0.0.0 --binlog-format=ROW --server-id=1 --gtid_mode=ON --enforce-gtid-consistency=true > mysql.3307.log 2>&1 &
```

### データを準備する {#prepare-data}

-   サンプルデータをmysql-3306に書き込みます。

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

    ```sql
    drop database if exists `sharding2`;
    create database `sharding2`;
    use `sharding2`;
    create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
    create table t3 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
    insert into t2 (id, uid, name, info) values (6, 40000, 'Remedios Moscote', '{}');
    insert into t3 (id, uid, name, info) values (7, 30001, 'Aureliano José', '{}'), (8, 30002, 'Santa Sofía de la Piedad', '{}'), (9, 30003, '17 Aurelianos', NULL);
    ```

### 下流TiDBを開始する {#start-downstream-tidb}

TiDBサーバーを実行するには、次のコマンドを使用します。

```bash
wget https://download.pingcap.org/tidb-community-server-v8.5.3-linux-amd64.tar.gz
tar -xzvf tidb-latest-linux-amd64.tar.gz
mv tidb-latest-linux-amd64/bin/tidb-server ./
./tidb-server
```

> **警告：**
>
> このドキュメントの TiDB のデプロイメント方法は、本番または開発環境には**適用されません**。

## MySQLデータソースを構成する {#configure-the-mysql-data-source}

データ移行タスクを開始する前に、MySQL データ ソースを構成する必要があります。

### パスワードを暗号化する {#encrypt-the-password}

> **注記：**
>
> -   データベースにパスワードがない場合、この手順をスキップできます。
> -   DM v1.0.6 以降のバージョンでは、プレーンテキスト パスワードを使用してソース情報を構成できます。

安全上の理由から、暗号化されたパスワードを設定して使用することをお勧めします。dmctlを使用してMySQL/TiDBのパスワードを暗号化できます。パスワードが「123456」であると仮定します。

> **注記：**
>
> v8.0.0 以降では、 `dmctl encrypt`コマンドを使用する前に、DM-master に[`secret-key-path`](/dm/dm-master-configuration-file.md)設定する必要があります。

```bash
./dmctl encrypt "123456"
```

    fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg=

この暗号化された値を保存し、次の手順で MySQL データ ソースを作成するときに使用します。

### ソース構成ファイルを編集する {#edit-the-source-configuration-file}

次の設定を`conf/source1.yaml`に書き込みます。

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

MySQL2データソースで、上記の設定を`conf/source2.yaml`にコピーします。3 `name` `mysql-replica-02`に変更し、 `password`と`port`適切な値に変更する必要があります。

### ソースを作成する {#create-a-source}

dmctl を使用して MySQL1 のデータ ソース構成を DM クラスターにロードするには、ターミナルで次のコマンドを実行します。

```bash
./dmctl --master-addr=127.0.0.1:8261 operate-source create conf/source1.yaml
```

MySQL2 の場合、上記のコマンドの設定ファイルを MySQL2 の設定ファイルに置き換えます。

## データ移行タスクを作成する {#create-a-data-migration-task}

[準備されたデータ](#prepare-data)インポートすると、MySQL1 インスタンスと MySQL2 インスタンスの両方に複数のシャードテーブルが作成されます。これらのテーブルは構造が同一で、テーブル名に同じプレフィックス「t」が付きます。また、これらのテーブルが配置されているデータベースのプレフィックスはすべて「sharding」です。また、主キーと一意キーの競合はありません（各シャードテーブルの主キーまたは一意キーは、他のテーブルのものと異なります）。

ここで、これらのシャードテーブルをTiDBの`db_target.t_target`テーブルに移行する必要があるとします。手順は以下のとおりです。

1.  タスクの構成ファイルを作成します。

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

2.  dmctl を使用してタスクを作成するには、上記の設定を`conf/task.yaml`ファイルに書き込みます。

    ```bash
    ./dmctl --master-addr 127.0.0.1:8261 start-task conf/task.yaml
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

これで、MySQL1 および MySQL2 インスタンスから TiDB にシャード テーブルを移行するタスクが正常に作成されました。

## データを検証する {#verify-data}

アップストリームのMySQLシャードテーブルのデータを変更できます。その後、 [同期差分インスペクター](/sync-diff-inspector/shard-diff.md)使用して、アップストリームとダウンストリームのデータの整合性を確認します。データの整合性は、移行タスクが正常に機能していることを意味し、クラスタが正常に動作していることを示します。
