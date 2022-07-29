---
title: Check Cluster Status
summary: Learn how to check the running status of the TiDB cluster.
---

# クラスタステータスを確認する {#check-cluster-status}

TiDBクラスタをデプロイした後、クラスタが正常に実行されているかどうかを確認する必要があります。このドキュメントでは、TiUPコマンド[TiDBダッシュボード](/dashboard/dashboard-intro.md)とGrafanaを使用してクラスタのステータスを確認する方法と、TiDBデータベースにログインして簡単なSQL操作を実行する方法を紹介します。

## TiDBクラスタのステータスを確認する {#check-the-tidb-cluster-status}

このセクションでは、TiUPコマンド[TiDBダッシュボード](/dashboard/dashboard-intro.md)とGrafanaを使用してTiDBクラスタのステータスを確認する方法について説明します。

### TiUPを使用する {#use-tiup}

`tiup cluster display <cluster-name>`コマンドを使用して、クラスタのステータスを確認します。例えば：

{{< copyable "" >}}

```shell
tiup cluster display tidb-test
```

期待される出力：各ノードの`Status`の情報が`Up`の場合、クラスタは正常に実行されます。

### TiDBダッシュボードを使用する {#use-tidb-dashboard}

1.  `${pd-ip}:${pd-port}/dashboard`でTiDBダッシュボードにログインします。ユーザー名とパスワードは、 `root`ユーザーのものと同じです。 `root`パスワードを変更した場合は、変更したパスワードを入力します。デフォルトでは、パスワードは空です。

    ![TiDB-Dashboard](/media/tiup/tidb-dashboard.png)

2.  ホームページには、TiDBクラスタのノード情報が表示されます。

    ![TiDB-Dashboard-status](/media/tiup/tidb-dashboard-status.png)

### Grafanaを使用する {#use-grafana}

1.  `${Grafana-ip}:3000`でGrafanaモニタリングにログインします。デフォルトのユーザー名とパスワードはどちらも`admin`です。

2.  TiDBポートのステータスと負荷監視情報を確認するには、[**概要**]をクリックします。

    ![Grafana-overview](/media/tiup/grafana-overview.png)

## データベースにログインして、簡単な操作を実行します {#log-in-to-the-database-and-perform-simple-operations}

> **ノート：**
>
> データベースにログインする前に、MySQLクライアントをインストールしてください。

次のコマンドを実行して、データベースにログインします。

{{< copyable "" >}}

```shell
mysql -u root -h ${tidb_server_host_IP_address} -P 4000
```

`${tidb_server_host_IP_address}`は、 `10.0.1.7`のように[クラスタトポロジファイルを初期化します](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)のときに`tidb_servers`に設定されるIPアドレスの1つです。

次の情報は、ログインが成功したことを示しています。

```sql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.25-TiDB-v5.0.0 TiDB Server (Apache License 2.0) Community Edition, MySQL 5.7 compatible
Copyright (c) 2000, 2015, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
```

### データベース操作 {#database-operations}

-   TiDBのバージョンを確認してください。

    {{< copyable "" >}}

    ```sql
    select tidb_version()\G
    ```

    期待される出力：

    ```sql
    *************************** 1. row ***************************
    tidb_version(): Release Version: v5.0.0
    Edition: Community
    Git Commit Hash: 689a6b6439ae7835947fcaccf329a3fc303986cb
    Git Branch: HEAD
    UTC Build Time: 2020-05-28 11:09:45
    GoVersion: go1.13.4
    Race Enabled: false
    TiKV Min Version: v3.0.0-60965b006877ca7234adaced7890d7b029ed1306
    Check Table Before Drop: false
    1 row in set (0.00 sec)
    ```

-   `pingcap`という名前のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    create database pingcap;
    ```

    期待される出力：

    ```sql
    Query OK, 0 rows affected (0.10 sec)
    ```

    `pingcap`のデータベースに切り替えます。

    {{< copyable "" >}}

    ```sql
    use pingcap;
    ```

    期待される出力：

    ```sql
    Database changed
    ```

-   `tab_tidb`という名前のテーブルを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE TABLE `tab_tidb` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(20) NOT NULL DEFAULT '',
    `age` int(11) NOT NULL DEFAULT 0,
    `version` varchar(20) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`),
    KEY `idx_age` (`age`));
    ```

    期待される出力：

    ```sql
    Query OK, 0 rows affected (0.11 sec)
    ```

-   データの挿入：

    {{< copyable "" >}}

    ```sql
    insert into `tab_tidb` values (1,'TiDB',5,'TiDB-v5.0.0');
    ```

    期待される出力：

    ```sql
    Query OK, 1 row affected (0.03 sec)
    ```

-   `tab_tidb`のエントリをビューします：

    {{< copyable "" >}}

    ```sql
    select * from tab_tidb;
    ```

    期待される出力：

    ```sql
    +----+------+-----+-------------+
    | id | name | age | version     |
    +----+------+-----+-------------+
    |  1 | TiDB |   5 | TiDB-v5.0.0 |
    +----+------+-----+-------------+
    1 row in set (0.00 sec)
    ```

-   ビューのストアの状態、 `store_id` 、容量、および稼働時間を表示します。

    {{< copyable "" >}}

    ```sql
    select STORE_ID,ADDRESS,STORE_STATE,STORE_STATE_NAME,CAPACITY,AVAILABLE,UPTIME from INFORMATION_SCHEMA.TIKV_STORE_STATUS;
    ```

    期待される出力：

    ```sql
    +----------+--------------------+-------------+------------------+----------+-----------+--------------------+
    | STORE_ID | ADDRESS            | STORE_STATE | STORE_STATE_NAME | CAPACITY | AVAILABLE | UPTIME             |
    +----------+--------------------+-------------+------------------+----------+-----------+--------------------+
    |        1 | 10.0.1.1:20160 |           0 | Up               | 49.98GiB | 46.3GiB   | 5h21m52.474864026s |
    |        4 | 10.0.1.2:20160 |           0 | Up               | 49.98GiB | 46.32GiB  | 5h21m52.522669177s |
    |        5 | 10.0.1.3:20160 |           0 | Up               | 49.98GiB | 45.44GiB  | 5h21m52.713660541s |
    +----------+--------------------+-------------+------------------+----------+-----------+--------------------+
    3 rows in set (0.00 sec)
    ```

-   TiDBを終了します。

    {{< copyable "" >}}

    ```sql
    exit
    ```

    期待される出力：

    ```sql
    Bye
    ```
