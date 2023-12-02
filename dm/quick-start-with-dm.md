---
title: TiDB Data Migration Quick Start
summary: Learn how to quickly deploy a DM cluster using binary packages.
---

# TiDB データ移行のクイック スタート ガイド {#quick-start-guide-for-tidb-data-migration}

このドキュメントでは、 [TiDB データ移行](https://github.com/pingcap/dm) (DM) を使用して MySQL から TiDB にデータを移行する方法について説明します。このガイドは DM 機能の簡単なデモであり、本番環境には推奨されません。

## ステップ 1: DM クラスターをデプロイ {#step-1-deploy-a-dm-cluster}

1.  TiUPをインストールし、 TiUPを使用して[`dmctl`](/dm/dmctl-introduction.md)をインストールします。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    tiup install dm dmctl
    ```

2.  DM クラスターの最小限のデプロイメント トポロジー ファイルを生成します。

        tiup dm template

3.  出力内の構成情報をコピーし、変更された IP アドレスを含む`topology.yaml`ファイルとして保存します。 TiUPを使用して、 `topology.yaml`ファイルを含む DM クラスターをデプロイ。

    ```shell
    tiup dm deploy dm-test 6.0.0 topology.yaml -p
    ```

## ステップ 2: データソースを準備する {#step-2-prepare-the-data-source}

1 つまたは複数の MySQL インスタンスをアップストリーム データ ソースとして使用できます。

1.  次のように、各データ ソースの構成ファイルを作成します。

    ```yaml
    source-id: "mysql-01"
    from:
      host: "127.0.0.1"
      user: "root"
      password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="  # encrypt with `tiup dmctl --encrypt "123456"`
      port: 3306
    ```

2.  次のコマンドを実行して、ソースを DM クラスターに追加します。 `mysql-01.yaml`は、前の手順で作成した構成ファイルです。

    ```bash
    tiup dmctl --master-addr=127.0.0.1:8261 operate-source create mysql-01.yaml # use one of master_servers as the argument of --master-addr
    ```

テスト用の MySQL インスタンスがない場合は、次の手順を実行して、Docker で MySQL インスタンスを作成できます。

1.  MySQL 構成ファイルを作成します。

    ```shell
    mkdir -p /tmp/mysqltest && cd /tmp/mysqltest

    cat > my.cnf <<EOF
    [mysqld]
    bind-address     = 0.0.0.0
    character-set-server=utf8
    collation-server=utf8_bin
    default-storage-engine=INNODB
    transaction-isolation=READ-COMMITTED
    server-id        = 100
    binlog_format    = row
    log_bin          = /var/lib/mysql/mysql-bin.log
    show_compatibility_56 = ON
    EOF
    ```

2.  Docker を使用して MySQL インスタンスを起動します。

    ```shell
    docker run --name mysql-01 -v /tmp/mysqltest:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=my-secret-pw -d -p 3306:3306 mysql:5.7
    ```

3.  MySQL インスタンスが起動したら、インスタンスにアクセスします。

    > **注記：**
    >
    > このコマンドはデータ移行を試す場合にのみ適しており、本番環境やストレス テストでは使用できません。

    ```shell
    mysql -uroot -p -h 127.0.0.1 -P 3306
    ```

## ステップ 3: ダウンストリーム データベースを準備する {#step-3-prepare-a-downstream-database}

既存の TiDB クラスターをデータ移行のターゲットとして選択できます。

テスト用の TiDB クラスターがない場合は、次のコマンドを実行してデモンストレーション環境を迅速に構築できます。

```shell
tiup playground
```

## ステップ 4: テストデータを準備する {#step-4-prepare-test-data}

1 つまたは複数のデータ ソースにテスト テーブルとデータを作成します。既存の MySQL データベースを使用しており、そのデータベースに利用可能なデータが含まれている場合は、この手順をスキップできます。

```sql
drop database if exists `testdm`;
create database `testdm`;
use `testdm`;
create table t1 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
insert into t1 (id, uid, name) values (1, 10001, 'Gabriel García Márquez'), (2, 10002, 'Cien años de soledad');
insert into t2 (id, uid, name) values (3, 20001, 'José Arcadio Buendía'), (4, 20002, 'Úrsula Iguarán'), (5, 20003, 'José Arcadio');
```

## ステップ 5: データ移行タスクを作成する {#step-5-create-a-data-migration-task}

1.  タスク構成ファイルを作成します`testdm-task.yaml` :

    ```yaml
    name: testdm
    task-mode: all

    target-database:
      host: "127.0.0.1"
      port: 4000
      user: "root"
      password: "" # If the password is not empty, it is recommended to use a password encrypted with dmctl.

    # Configure the information of one or multiple data sources
    mysql-instances:
      - source-id: "mysql-01"
        block-allow-list:  "ba-rule1"

    block-allow-list:
      ba-rule1:
        do-dbs: ["testdm"]
    ```

2.  dmctl を使用してタスクを作成します。

    ```bash
    tiup dmctl --master-addr 127.0.0.1:8261 start-task testdm-task.yaml
    ```

`mysql-01`データベースから TiDB にデータを移行するタスクが正常に作成されました。

## ステップ 6: タスクのステータスを確認する {#step-6-check-the-status-of-the-task}

タスクの作成後、 `dmctl query-status`コマンドを使用してタスクのステータスを確認できます。

```bash
tiup dmctl --master-addr 127.0.0.1:8261 query-status testdm
```
