---
title: Quick Start with TiDB Data Migration
summary: TiUP Playground を使用してデータ移行環境をすばやくセットアップする方法を学びます。
---

# TiDBデータ移行のクイックスタート {#quick-start-with-tidb-data-migration}

[TiDB データ移行 (DM)](/dm/dm-overview.md) 、MySQL互換データベースからTiDBにデータを複製する強力なツールです。このガイドでは、 [TiUPプレイグラウンド](/tiup/tiup-playground.md)使用して開発またはテスト用のローカルTiDB DM環境を迅速に構築する方法と、ソースMySQLデータベースからターゲットTiDBデータベースへのデータ移行という簡単なタスクを段階的に説明します。

> **注記：**
>
> 本番への展開については、 [TiUPを使用して DMクラスタをデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)参照してください。

## ステップ1: テスト環境をセットアップする {#step-1-set-up-the-test-environment}

[TiUP](/tiup/tiup-overview.md)はクラスタ運用・保守ツールです。Playground機能を使用すると、開発・テスト用にTiDBデータベースとTiDB DMを備えた一時的なローカル環境を迅速に起動できます。

1.  TiUPをインストールします:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    > **注記：**
    >
    > 既にTiUPがインストールされている場合は、フラグ`--dm-master`と`--dm-worker`使用するには、v1.16.1 以降にアップデートされていることを確認してください。現在のバージョンを確認するには、次のコマンドを実行します。
    >
    > ```shell
    > tiup --version
    > ```
    >
    > TiUP を最新バージョンにアップグレードするには、次のコマンドを実行します。
    >
    > ```shell
    > tiup update --self
    > ```

2.  ターゲット TiDB データベースと DM コンポーネントを使用してTiUP Playground を起動します。

    ```shell
    tiup playground v8.5.3 --dm-master 1 --dm-worker 1 --tiflash 0 --without-monitor
    ```

3.  出力で TiDB と DM が実行されているかどうかを確認して環境を確認します。

    ```text
    TiDB Playground Cluster is started, enjoy!

    Connect TiDB:    mysql --host 127.0.0.1 --port 4000 -u root
    Connect DM:      tiup dmctl --master-addr 127.0.0.1:8261
    TiDB Dashboard:  http://127.0.0.1:2379/dashboard
    ```

4.  現在のターミナルで`tiup playground`を実行したままにして、次の手順のために新しいターミナルを開きます。

    このプレイグラウンド環境は、ターゲットTiDBデータベースとレプリケーションエンジン（DMマスターとDMワーカー）の実行プロセスを提供します。MySQL（ソース）→ DM（レプリケーションエンジン）→ TiDB（ターゲット）というデータフローを処理します。

## ステップ2: ソースデータベースを準備する（オプション） {#step-2-prepare-a-source-database-optional}

ソースデータベースとして、1つ以上のMySQLインスタンスを使用できます。MySQL互換インスタンスを既にお持ちの場合は、 [ステップ3](#step-3-configure-a-tidb-dm-source)に進んでください。そうでない場合は、以下の手順に従ってテスト用のインスタンスを作成してください。

<SimpleTab groupId="os">

<div label="Docker" value="docker">

Docker を使用すると、テスト用の MySQL 8.0 インスタンスをすばやくデプロイできます。

1.  MySQL 8.0 Docker コンテナを実行します。

    ```shell
    docker run --name mysql80 \
        -e MYSQL_ROOT_PASSWORD=MyPassw0rd! \
        -p 3306:3306 \
        -d mysql:8.0
    ```

2.  MySQLに接続します。

    ```shell
    docker exec -it mysql80 mysql -uroot -pMyPassw0rd!
    ```

3.  DM テストに必要な権限を持つ専用ユーザーを作成します。

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

4.  サンプルデータを作成します。

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

<div label="macOS" value="macos">

macOS では、 [Homebrew](https://brew.sh)使用して MySQL 8.0 をローカルにすばやくインストールして起動できます。

1.  Homebrewを更新し、MySQL 8.0 をインストールします。

    ```shell
    brew update
    brew install mysql@8.0
    ```

2.  MySQL コマンドをシステム パスでアクセスできるようにします。

    ```shell
    brew link mysql@8.0 --force
    ```

3.  MySQL サービスを開始します。

    ```shell
    brew services start mysql@8.0
    ```

4.  `root`ユーザーとして MySQL に接続します。

    ```shell
    mysql -uroot
    ```

5.  DM テストに必要な権限を持つ専用ユーザーを作成します。

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

6.  サンプルデータを作成します。

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

<div label="CentOS" value="centos">

CentOS などのエンタープライズ Linux ディストリビューションでは、MySQL Yum リポジトリから MySQL 8.0 をインストールできます。

1.  [MySQL Yumリポジトリのダウンロードページ](https://dev.mysql.com/downloads/repo/yum)から MySQL Yum リポジトリ パッケージをダウンロードしてインストールします。Linux バージョン 9 以外の場合は、次の URL の`el9` (Enterprise Linux バージョン 9) を置き換え、MySQL バージョン 8.0 の場合は`mysql80`そのままにする必要があります。

    ```shell
    sudo yum install -y https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm
    ```

2.  MySQLをインストールします。

    ```shell
    sudo yum install -y mysql-community-server --nogpgcheck
    ```

3.  MySQLを起動します。

    ```shell
    sudo systemctl start mysqld
    ```

4.  MySQL ログで一時的な root パスワードを見つけます。

    ```shell
    sudo grep 'temporary password' /var/log/mysqld.log
    ```

5.  一時パスワードを使用して`root`ユーザーとして MySQL に接続します。

    ```shell
    mysql -uroot -p
    ```

6.  `root`パスワードをリセットします:

    ```sql
    ALTER USER 'root'@'localhost'
        IDENTIFIED BY 'MyPassw0rd!';
    ```

7.  DM テストに必要な権限を持つ専用ユーザーを作成します。

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

8.  サンプルデータを作成します。

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

<div label="Ubuntu" value="ubuntu">

Ubuntu では、公式の Ubuntu リポジトリから MySQL をインストールできます。

1.  パッケージリストを更新します:

    ```shell
    sudo apt-get update
    ```

2.  MySQLをインストールします。

    ```shell
    sudo apt-get install -y mysql-server
    ```

3.  `mysql`サービスが実行されているかどうかを確認し、必要に応じてサービスを開始します。

    ```shell
    sudo systemctl status mysql
    sudo systemctl start mysql
    ```

4.  ソケット認証を使用して`root`ユーザーとして MySQL に接続します。

    ```shell
    sudo mysql
    ```

5.  DM テストに必要な権限を持つ専用ユーザーを作成します。

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

6.  サンプルデータを作成します。

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

</SimpleTab>

## ステップ3: TiDB DMソースを構成する {#step-3-configure-a-tidb-dm-source}

ソースMySQLデータベースを準備したら、TiDB DMをそのデータベースに接続するための設定を行います。そのためには、接続の詳細を含むソース設定ファイルを作成し、 `dmctl`ツールを使用して設定を適用します。

1.  ソース構成ファイル`mysql-01.yaml`を作成します。

    > **注記：**
    >
    > この手順では、 [ステップ2](#step-2-prepare-a-source-database-optional)で説明されているように、ソース データベースにレプリケーション権限を持つ`tidb-dm`ユーザーがすでに作成されていることを前提としています。

    ```yaml
    source-id: "mysql-01"
    from:
      host: "127.0.0.1"
      user: "tidb-dm"
      password: "MyPassw0rd!"    # In production environments, it is recommended to use a password encrypted with dmctl.
      port: 3306
    ```

2.  DM データ ソースを作成します。

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 operate-source create mysql-01.yaml
    ```

## ステップ4: TiDB DMタスクを作成する {#step-4-create-a-tidb-dm-task}

ソースデータベースを設定したら、TiDB DM で移行タスクを作成できます。このタスクは、ソース MySQL インスタンスを参照し、ターゲット TiDB データベースへの接続詳細を定義します。

1.  DMタスク構成ファイル`tiup-playground-task.yaml`を作成します。

    ```yaml
    # Task
    name: tiup-playground-task
    task-mode: "all"              # Execute all phases - full data migration and incremental sync.

    # Source (MySQL)
    mysql-instances:
      - source-id: "mysql-01"

    ## Target (TiDB)
    target-database:
      host: "127.0.0.1"
      port: 4000
      user: "root"
      password: ""                # If the password is not empty, it is recommended to use a password encrypted with dmctl.
    ```

2.  構成ファイルを使用してタスクを開始します。

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 start-task tiup-playground-task.yaml
    ```

## ステップ5: データ複製を確認する {#step-5-verify-the-data-replication}

移行タスクを開始したら、データレプリケーションが期待どおりに動作しているかどうかを確認します。1 `dmctl`を使用してタスクのステータスを確認し、ターゲット TiDB データベースに接続して、ソース MySQL データベースからデータが正常に複製されていることを確認します。

1.  TiDB DM タスクのステータスを確認します。

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 query-status
    ```

2.  ターゲット TiDB データベースに接続します。

    ```shell
    mysql --host 127.0.0.1 --port 4000 -u root --prompt 'tidb> '
    ```

3.  複製されたデータを確認します。1 [ステップ2](#step-2-prepare-a-source-database-optional)サンプルデータを作成した場合、MySQLソースデータベースからターゲットTiDBデータベースに複製されたテーブル`hello_tidb`が表示されます。

    ```sql
    SELECT * FROM hello.hello_tidb;
    ```

    出力は次のようになります。

    ```sql
    +----+-------------+
    | id | name        |
    +----+-------------+
    |  1 | Hello World |
    +----+-------------+
    1 row in set (0.00 sec)
    ```

## ステップ6: クリーンアップ（オプション） {#step-6-clean-up-optional}

テストが完了したら、 TiUP Playground を停止し、ソース MySQL インスタンス (テスト用に作成された場合) を削除し、不要なファイルを削除することで、環境をクリーンアップできます。

1.  TiUP Playgroundを停止します。

    TiUP Playground が実行中のターミナルで、 <kbd>Control</kbd> + <kbd>C</kbd>を押してプロセスを終了します。これにより、すべての TiDB および DM コンポーネントが停止し、ターゲット環境が削除されます。

2.  ソース MySQL インスタンスを停止して削除します。

    [ステップ2](#step-2-prepare-a-source-database-optional)でテスト用のソース MySQL インスタンスを作成した場合は、次の手順に従ってそれを停止し、削除します。

    <SimpleTab groupId="os">

    <div label="Docker" value="docker">

    Docker コンテナを停止して削除するには:

    ```shell
    docker stop mysql80
    docker rm mysql80
    ```

    </div>

    <div label="macOS" value="macos">

    テスト目的のみでHomebrewを使用して MySQL 8.0 をインストールした場合は、サービスを停止してアンインストールします。

    ```shell
    brew services stop mysql@8.0
    brew uninstall mysql@8.0
    ```

    > **注記：**
    >
    > すべての MySQL データ ファイルを削除する場合は、MySQL データ ディレクトリ (通常は`/opt/homebrew/var/mysql`にあります) を削除します。

    </div>

    <div label="CentOS" value="centos">

    テスト目的のみで MySQL Yum リポジトリから MySQL 8.0 をインストールした場合は、サービスを停止してアンインストールします。

    ```shell
    sudo systemctl stop mysqld
    sudo yum remove -y mysql-community-server
    ```

    > **注記：**
    >
    > すべての MySQL データ ファイルを削除する場合は、MySQL データ ディレクトリ (通常は`/var/lib/mysql`にあります) を削除します。

    </div>

    <div label="Ubuntu" value="ubuntu">

    テスト目的のみで公式 Ubuntu リポジトリから MySQL をインストールした場合は、サービスを停止してアンインストールします。

    ```shell
    sudo systemctl stop mysql
    sudo apt-get remove --purge -y mysql-server
    sudo apt-get autoremove -y
    ```

    > **注記：**
    >
    > すべての MySQL データ ファイルを削除する場合は、MySQL データ ディレクトリ (通常は`/var/lib/mysql`にあります) を削除します。

    </div>

    </SimpleTab>

3.  TiDB DM 構成ファイルが不要になった場合は削除します。

    ```shell
    rm mysql-01.yaml tiup-playground-task.yaml
    ```

4.  TiUPが不要になった場合は、アンインストールできます。

    ```shell
    rm -rf ~/.tiup
    ```

## 次は何？ {#what-s-next}

テスト環境でソース MySQL データベースからターゲット TiDB データベースにデータを移行するタスクを正常に作成したので、次の操作を実行できます。

-   探索[TiDB DM の機能](/dm/dm-overview.md)
-   [TiDB DMアーキテクチャ](/dm/dm-arch.md)について学ぶ
-   セットアップ[概念実証または本番環境用の TiDB DM](/dm/deploy-a-dm-cluster-using-tiup.md)
-   高度な設定[DMタスク](/dm/dm-task-configuration-guide.md)
