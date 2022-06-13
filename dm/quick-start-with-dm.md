---
title: TiDB Data Migration Quick Start
summary: Learn how to quickly deploy a DM cluster using binary packages.
---

# TiDBデータ移行のクイックスタートガイド {#quick-start-guide-for-tidb-data-migration}

このドキュメントでは、 [TiDBデータ移行](https://github.com/pingcap/dm) （DM）を使用してMySQLからTiDBにデータを移行する方法について説明します。このガイドはDM機能の簡単なデモであり、実稼働環境にはお勧めしません。

## ステップ1：DMクラスタをデプロイする {#step-1-deploy-a-dm-cluster}

1.  TiUPをインストールし、TiUPを使用して[`dmctl`](/dm/dmctl-introduction.md)をインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    tiup install dm dmctl
    ```

2.  DMクラスタの最小限のデプロイメントトポロジファイルを生成します。

    {{< copyable "" >}}

    ```
    tiup dm template
    ```

3.  出力の構成情報をコピーし、変更したIPアドレスを持つ`topology.yaml`ファイルとして保存します。 TiUPを使用して、 `topology.yaml`のファイルでDMクラスタをデプロイします。

    {{< copyable "" >}}

    ```shell
    tiup dm deploy dm-test 6.0.0 topology.yaml -p
    ```

## ステップ2：データソースを準備する {#step-2-prepare-the-data-source}

1つまたは複数のMySQLインスタンスをアップストリームデータソースとして使用できます。

1.  次のように、各データソースの構成ファイルを作成します。

    {{< copyable "" >}}

    ```yaml
    source-id: "mysql-01"
    from:
      host: "127.0.0.1"
      user: "root"
      password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="  # encrypt with `tiup dmctl --encrypt "123456"`
      port: 3306
    ```

2.  次のコマンドを実行して、ソースをDMクラスタに追加します。 `mysql-01.yaml`は、前の手順で作成した構成ファイルです。

    {{< copyable "" >}}

    ```bash
    tiup dmctl --master-addr=127.0.0.1:8261 operate-source create mysql-01.yaml # use one of master_servers as the argument of --master-addr
    ```

テスト用のMySQLインスタンスがない場合は、次の手順を実行してDockerでMySQLインスタンスを作成できます。

1.  MySQL構成ファイルを作成します。

    {{< copyable "" >}}

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

2.  Dockerを使用してMySQLインスタンスを起動します。

    {{< copyable "" >}}

    ```shell
    docker run --name mysql-01 -v /tmp/mysqltest:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=my-secret-pw -d -p 3306:3306 mysql:5.7
    ```

3.  MySQLインスタンスが開始されたら、インスタンスにアクセスします。

    > **ノート：**
    >
    > このコマンドは、データ移行の試行にのみ適しており、実稼働環境やストレステストでは使用できません。

    {{< copyable "" >}}

    ```shell
    mysql -uroot -p -h 127.0.0.1 -P 3306
    ```

## ステップ3：ダウンストリームデータベースを準備する {#step-3-prepare-a-downstream-database}

データ移行のターゲットとして既存のTiDBクラスタを選択できます。

テスト用のTiDBクラスタがない場合は、次のコマンドを実行して、デモンストレーション環境をすばやく構築できます。

{{< copyable "" >}}

```shell
tiup playground
```

## ステップ4：テストデータを準備する {#step-4-prepare-test-data}

1つまたは複数のデータソースにテストテーブルとデータを作成します。既存のMySQLデータベースを使用していて、データベースに使用可能なデータが含まれている場合は、この手順をスキップできます。

{{< copyable "" >}}

```sql
drop database if exists `testdm`;
create database `testdm`;
use `testdm`;
create table t1 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
insert into t1 (id, uid, name) values (1, 10001, 'Gabriel García Márquez'), (2, 10002, 'Cien años de soledad');
insert into t2 (id, uid, name) values (3, 20001, 'José Arcadio Buendía'), (4, 20002, 'Úrsula Iguarán'), (5, 20003, 'José Arcadio');
```

## ステップ5：データ移行タスクを作成する {#step-5-create-a-data-migration-task}

1.  タスク構成ファイルを作成する`testdm-task.yaml` ：

    {{< copyable "" >}}

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

2.  dmctlを使用してタスクを作成します。

    {{< copyable "" >}}

    ```bash
    tiup dmctl --master-addr 127.0.0.1:8261 start-task testdm-task.yaml
    ```

これで、 `mysql-01`のデータベースからTiDBにデータを移行するタスクが正常に作成されました。

## ステップ6：タスクのステータスを確認します {#step-6-check-the-status-of-the-task}

タスクが作成されたら、 `dmctl query-status`コマンドを使用してタスクのステータスを確認できます。

{{< copyable "" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 query-status testdm
```
