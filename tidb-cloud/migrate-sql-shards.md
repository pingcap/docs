---
title: Migrate and Merge MySQL Shards of Large Datasets to TiDB Cloud
summary: Learn how to migrate and merge MySQL shards of large datasets to TiDB Cloud.
---

# 大規模なデータセットの MySQL シャードをTiDB Cloudに移行およびマージする {#migrate-and-merge-mysql-shards-of-large-datasets-to-tidb-cloud}

このドキュメントでは、大規模な MySQL データセット (たとえば、1 TiB を超える) をさまざまなパーティションからTiDB Cloudに移行してマージする方法について説明します。完全なデータ移行の後、 [TiDB データ移行 (DM)](https://docs.pingcap.com/tidb/stable/dm-overview)を使用して、ビジネス ニーズに応じて増分移行を実行できます。

このドキュメントの例では、複数の MySQL インスタンスにまたがる複雑なシャード移行タスクを使用し、自動インクリメント主キーの競合を処理します。この例のシナリオは、単一の MySQL インスタンス内の異なるシャード テーブルからのデータのマージにも適用できます。

## 例の環境情報 {#environment-information-in-the-example}

このセクションでは、例で使用される上流クラスター、DM、および下流クラスターの基本情報について説明します。

### アップストリーム クラスター {#upstream-cluster}

上流クラスタの環境情報は以下の通りです。

-   MySQL バージョン: MySQL v5.7.18
-   MySQL インスタンス 1:
    -   スキーマ`store_01`と表`[sale_01, sale_02]`
    -   スキーマ`store_02`と表`[sale_01, sale_02]`
-   MySQL インスタンス 2:
    -   スキーマ`store_01`と表`[sale_01, sale_02]`
    -   スキーマ`store_02`と表`[sale_01, sale_02]`
-   テーブル構造:

    ```sql
    CREATE TABLE sale_01 (
    id bigint(20) NOT NULL auto_increment,
    uid varchar(40) NOT NULL,
    sale_num bigint DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY ind_uid (uid)
    );
    ```

### DM {#dm}

DM のバージョンは v5.3.0 です。 TiDB DM を手動でデプロイする必要があります。詳細な手順については、 [TiUPを使用して DMクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)を参照してください。

### 外部storage {#external-storage}

このドキュメントでは、Amazon S3 を例として使用します。

### ダウンストリーム クラスター {#downstream-cluster}

シャードされたスキーマとテーブルは、テーブル`store.sales`にマージされます。

## MySQL からTiDB Cloudへの完全なデータ移行を実行する {#perform-full-data-migration-from-mysql-to-tidb-cloud}

以下は、MySQL シャードの全データをTiDB Cloudに移行およびマージする手順です。

次の例では、テーブルのデータを**CSV**形式にエクスポートするだけで済みます。

### ステップ 1.Amazon S3 バケットにディレクトリを作成する {#step-1-create-directories-in-the-amazon-s3-bucket}

Amazon S3 バケットに第 1 レベルのディレクトリ`store` (データベースのレベルに対応) と第 2 レベルのディレクトリ`sales` (テーブルのレベルに対応) を作成します。 `sales`で、各 MySQL インスタンスに第 3 レベルのディレクトリを作成します (MySQL インスタンスのレベルに対応)。例えば：

-   MySQL instance1 のデータを`s3://dumpling-s3/store/sales/instance01/`に移行する
-   MySQL instance2 のデータを`s3://dumpling-s3/store/sales/instance02/`に移行します

複数のインスタンスにまたがるシャードがある場合は、データベースごとに第 1 レベルのディレクトリを 1 つ作成し、シャード テーブルごとに第 2 レベルのディレクトリを 1 つ作成できます。次に、管理を容易にするために、各 MySQL インスタンスに第 3 レベルのディレクトリを作成します。たとえば、テーブル`stock_N.product_N`を MySQL インスタンス 1 と MySQL インスタンス 2 からTiDB Cloudのテーブル`stock.products`に移行してマージする場合は、次のディレクトリを作成できます。

-   `s3://dumpling-s3/stock/products/instance01/`
-   `s3://dumpling-s3/stock/products/instance02/`

### ステップ 2. Dumpling を使用してデータを Amazon S3 にエクスポートする {#step-2-use-dumpling-to-export-data-to-amazon-s3}

Dumplingのインストール方法については、 [Dumpling紹介](/dumpling-overview.md)を参照してください。

Dumplingを使用してデータを Amazon S3 にエクスポートする場合は、次の点に注意してください。

-   アップストリーム クラスターのbinlog を有効にします。
-   正しい Amazon S3 ディレクトリとリージョンを選択します。
-   アップストリーム クラスタへの影響を最小限に抑えるために`-t`オプションを設定するか、バックアップ データベースから直接エクスポートして、適切な同時実行数を選択します。このパラメーターの使用方法について詳しくは、 [Dumplingのオプション一覧](/dumpling-overview.md#option-list-of-dumpling)を参照してください。
-   `--filetype csv`と`--no-schemas`に適切な値を設定します。これらのパラメーターの使用方法について詳しくは、 [Dumplingのオプション一覧](/dumpling-overview.md#option-list-of-dumpling)を参照してください。

次のように CSV ファイルに名前を付けます。

-   1 つのテーブルのデータが複数の CSV ファイルに分割されている場合は、これらの CSV ファイルに数値のサフィックスを追加します。たとえば、 `${db_name}.${table_name}.000001.csv`と`${db_name}.${table_name}.000002.csv`です。数値サフィックスは連続していなくてもかまいませんが、昇順でなければなりません。また、数字の前にゼロを追加して、すべてのサフィックスが同じ長さになるようにする必要もあります。

> **ノート：**
>
> 上記のルールに従って CSV ファイル名を更新できない場合 (たとえば、CSV ファイルのリンクが他のプログラムでも使用されている場合など) は、ファイル名を変更せずに[ステップ 5](#step-5-perform-the-data-import-task)**ファイル パターン**を使用してソース データをインポートできます。単一のターゲット テーブルに。

データを Amazon S3 にエクスポートするには、次の手順を実行します。

1.  Amazon S3 バケットの`AWS_ACCESS_KEY_ID`と`AWS_SECRET_ACCESS_KEY`を取得します。

    ```shell
    [root@localhost ~]# export AWS_ACCESS_KEY_ID={your_aws_access_key_id}
    [root@localhost ~]# export AWS_SECRET_ACCESS_KEY= {your_aws_secret_access_key}
    ```

2.  MySQL instance1 から Amazon S3 バケットの`s3://dumpling-s3/store/sales/instance01/`ディレクトリにデータをエクスポートします。

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql01-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance01/" --s3.region "ap-northeast-1"
    ```

    パラメータの詳細については、 [Dumplingのオプション一覧](/dumpling-overview.md#option-list-of-dumpling)を参照してください。

3.  MySQL instance2 から Amazon S3 バケットの`s3://dumpling-s3/store/sales/instance02/`ディレクトリにデータをエクスポートします。

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql02-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance02/" --s3.region "ap-northeast-1"
    ```

詳細な手順については、 [データを Amazon S3 クラウドstorageにエクスポートする](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage)を参照してください。

### ステップ 3. TiDB Cloudクラスターでスキーマを作成する {#step-3-create-schemas-in-tidb-cloud-cluster}

次のように、 TiDB Cloudクラスターにスキーマを作成します。

```sql
mysql> CREATE DATABASE store;
Query OK, 0 rows affected (0.16 sec)
mysql> use store;
Database changed
```

この例では、上流のテーブル`sale_01`と`sale_02`の列 ID が自動インクリメントの主キーです。ダウンストリーム データベースでシャード テーブルをマージすると、競合が発生する場合があります。次の SQL ステートメントを実行して、ID 列を主キーではなく通常のインデックスとして設定します。

```sql
mysql> CREATE TABLE `sales` (
   ->   `id` bigint(20) NOT NULL ,
   ->   `uid` varchar(40) NOT NULL,
   ->   `sale_num` bigint DEFAULT NULL,
   ->   INDEX (`id`),
   ->   UNIQUE KEY `ind_uid` (`uid`)
   -> );
Query OK, 0 rows affected (0.17 sec)
```

このような競合を解決するソリューションの詳細については、 [列から PRIMARY KEY 属性を削除します](https://docs.pingcap.com/tidb/stable/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column)を参照してください。

### ステップ 4.Amazon S3 アクセスを構成する {#step-4-configure-amazon-s3-access}

[Amazon S3 アクセスの構成](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)の手順に従って、ソースデータにアクセスするためのロール ARN を取得します。

次の例では、主要なポリシー構成のみを一覧表示しています。 Amazon S3 パスを独自の値に置き換えます。

```yaml
{
   "Version": "2012-10-17",
   "Statement": [
       {
           "Sid": "VisualEditor0",
           "Effect": "Allow",
           "Action": [
               "s3:GetObject",
               "s3:GetObjectVersion"
           ],
           "Resource": [
               "arn:aws:s3:::dumpling-s3/*"
           ]
       },
       {
           "Sid": "VisualEditor1",
           "Effect": "Allow",
           "Action": [
               "s3:ListBucket",
               "s3:GetBucketLocation"
           ],

           "Resource": "arn:aws:s3:::dumpling-s3"
       }
   ]
}
```

### ステップ 5. データ インポート タスクを実行する {#step-5-perform-the-data-import-task}

Amazon S3 アクセスを設定したら、次のようにTiDB Cloudコンソールでデータ インポート タスクを実行できます。

1.  ターゲット クラスターの**[インポート]**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅の ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **[インポート]**ページで、右上隅にある<strong>[データのインポート]</strong>をクリックし、 <strong>[S3 から]</strong>を選択します。

3.  **[S3 からインポート]**ページで、次の情報を入力します。

    -   **データ形式**: <strong>CSV</strong>を選択します。
    -   **バケット URI** : ソース データのバケット URI を入力します。テーブルに対応する第 2 レベルのディレクトリ (この例では`s3://dumpling-s3/store/sales`を使用して、 TiDB Cloud がすべての MySQL インスタンスのデータを一度にインポートして`store.sales`にマージできるようにします。
    -   **Role ARN** : 取得した Role-ARN を入力します。

    バケットの場所がクラスターと異なる場合は、クロス リージョンのコンプライアンスを確認します。 **[次へ]**をクリックします。

    TiDB Cloud は、指定されたバケット URI でデータにアクセスできるかどうかの検証を開始します。検証後、 TiDB Cloud はデフォルトのファイル命名パターンを使用してデータ ソース内のすべてのファイルをスキャンしようとし、次のページの左側にスキャンの概要結果を返します。 `AccessDenied`エラーが発生した場合は、 [S3 からのデータ インポート中のアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。

4.  ファイル パターンを変更し、必要に応じてテーブル フィルター ルールを追加します。

    -   **ファイル パターン**: ファイル名が特定のパターンに一致する CSV ファイルを単一のターゲット テーブルにインポートする場合は、ファイル パターンを変更します。

        > **ノート：**
        >
        > この機能を使用すると、1 つのインポート タスクで一度に 1 つのテーブルにのみデータをインポートできます。この機能を使用してデータを別のテーブルにインポートする場合は、インポートするたびに別のターゲット テーブルを指定して、複数回インポートする必要があります。

        ファイル パターンを変更するには、 **[変更]**をクリックし、次のフィールドで CSV ファイルと単一のターゲット テーブルとの間のカスタム マッピング ルールを指定して、 <strong>[スキャン]</strong>をクリックします。

        -   **ソース ファイル名**: インポートする CSV ファイルの名前と一致するパターンを入力します。 CSV ファイルが 1 つしかない場合は、ここにファイル名を直接入力します。 CSV ファイルの名前には、サフィックス「.csv」を含める必要があることに注意してください。

            例えば：

            -   `my-data?.csv` : `my-data`と 1 文字 ( `my-data1.csv`と`my-data2.csv`など) で始まるすべての CSV ファイルが同じターゲット テーブルにインポートされます。
            -   `my-data*.csv` : `my-data`で始まるすべての CSV ファイルが同じターゲット テーブルにインポートされます。

        -   **ターゲット テーブル名**: TiDB Cloudのターゲット テーブルの名前を入力します。これは`${db_name}.${table_name}`形式である必要があります。たとえば、 `mydb.mytable`です。このフィールドは特定のテーブル名を 1 つしか受け付けないため、ワイルドカードはサポートされていないことに注意してください。

    -   **テーブル フィルター**: インポートするテーブルをフィルター処理する場合は、この領域で[テーブル フィルター](/table-filter.md#syntax)ルールを 1 つ以上指定できます。

5.  **[次へ]**をクリックします。

6.  **プレビュー**ページでは、データのプレビューを表示できます。プレビューされたデータが期待どおりでない場合は、 <strong>[ここをクリックして csv 構成を編集します] リンクを</strong>クリックして、区切り記号、区切り記号、ヘッダー、 `backslash escape` 、および`trim last separator`を含む CSV 固有の構成を更新します。

    > **ノート：**
    >
    > 区切り記号、区切り記号、およびヌルの構成では、英数字と特定の特殊文字の両方を使用できます。サポートされている特殊文字には、 `\t` 、 `\b` 、 `\n` 、 `\r` 、 `\f` 、および`\u0001`が含まれます。

7.  **[インポートの開始]**をクリックします。

8.  インポートの進行状況が**Finished**と表示されたら、インポートされたテーブルを確認します。

データがインポートされた後、 TiDB Cloudの Amazon S3 アクセスを削除する場合は、追加したポリシーを削除するだけです。

## MySQL からTiDB Cloudへの増分データ複製を実行する {#perform-incremental-data-replication-from-mysql-to-tidb-cloud}

binlogに基づくデータ変更を上流クラスターの指定された位置からTiDB Cloudに複製するには、TiDB Data Migration (DM) を使用して増分複製を実行できます。

### あなたが始める前に {#before-you-begin}

TiDB Cloudコンソールは、増分データ複製に関する機能をまだ提供していません。増分データを移行するには、TiDB DM をデプロイする必要があります。詳細な手順については、 [TiUPを使用して DMクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)を参照してください。

### 手順 1. データ ソースを追加する {#step-1-add-the-data-source}

1.  新しいデータ ソース ファイル`dm-source1.yaml`を作成して、アップストリーム データ ソースを DM に構成します。次のコンテンツを追加します。

    ```yaml
    # MySQL Configuration.
    source-id: "mysql-replica-01"
    # Specifies whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
    # The prerequisite is that you have already enabled GTID in the upstream MySQL.
    # If you have configured the upstream database service to switch master between different nodes automatically, you must enable GTID.
    enable-gtid: true
    from:
     host: "${host}"           # For example: 192.168.10.101
     user: "user01"
     password: "${password}"   # Plaintext passwords are supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.
     port: ${port}             # For example: 3307
    ```

2.  別の新しいデータ ソース ファイル`dm-source2.yaml`を作成し、次の内容を追加します。

    ```yaml
    # MySQL Configuration.
    source-id: "mysql-replica-02"
    # Specifies whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
    # The prerequisite is that you have already enabled GTID in the upstream MySQL.
    # If you have configured the upstream database service to switch master between different nodes automatically, you must enable GTID.
    enable-gtid: true
    from:
     host: "192.168.10.102"
     user: "user02"
     password: "${password}"
     port: 3308
    ```

3.  ターミナルで次のコマンドを実行します。 `tiup dmctl`を使用して、最初のデータ ソース構成を DM クラスターに読み込みます。

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr ${advertise-addr} operate-source create dm-source1.yaml
    ```

    上記のコマンドで使用されるパラメーターは、次のとおりです。

    | パラメータ                   | 説明                                                                             |
    | ----------------------- | ------------------------------------------------------------------------------ |
    | `--master-addr`         | `dmctl`が接続されるクラスター内の任意の DM マスター ノードの`{advertise-addr}` 。例: 192.168.11.110:9261 |
    | `operate-source create` | データ ソースを DM クラスターに読み込みます。                                                      |

    次に出力例を示します。

    ```shell
    tiup is checking updates for component dmctl ...

    Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source1.yaml

    {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "source": "mysql-replica-01",
               "worker": "dm-192.168.11.111-9262"
           }
       ]
    }

    ```

4.  ターミナルで次のコマンドを実行します。 `tiup dmctl`を使用して、2 番目のデータ ソース構成を DM クラスターに読み込みます。

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source2.yaml
    ```

    次に出力例を示します。

    ```shell
    tiup is checking updates for component dmctl ...

    Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source2.yaml

    {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "source": "mysql-replica-02",
               "worker": "dm-192.168.11.112-9262"
           }
       ]
    }
    ```

### 手順 2. レプリケーション タスクを作成する {#step-2-create-a-replication-task}

1.  レプリケーション タスク用に`test-task1.yaml`ファイルを作成します。

2.  Dumplingによってエクスポートされた MySQL instance1 のメタデータ ファイルで開始点を見つけます。例えば：

    ```toml
    Started dump at: 2022-05-25 10:16:26
    SHOW MASTER STATUS:
           Log: mysql-bin.000002
           Pos: 246546174
           GTID:b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801
    Finished dump at: 2022-05-25 10:16:27
    ```

3.  Dumplingによってエクスポートされた MySQL instance2 のメタデータ ファイルで開始点を見つけます。例えば：

    ```toml
    Started dump at: 2022-05-25 10:20:32
    SHOW MASTER STATUS:
           Log: mysql-bin.000001
           Pos: 1312659
           GTID:cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036
    Finished dump at: 2022-05-25 10:20:32
    ```

4.  タスク構成ファイル`test-task1`を編集して、各データ ソースの増分レプリケーション モードとレプリケーションの開始点を構成します。

    ```yaml
    ## ********* Task Configuration *********
    name: test-task1
    shard-mode: "pessimistic"
    # Task mode. The "incremental" mode only performs incremental data migration.
    task-mode: incremental
    # timezone: "UTC"

    ## ******** Data Source Configuration **********
    ## (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data migration error.
    ##  This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
    syncers:           # The running configurations of the sync processing unit.
     global:           # Configuration name.
       safe-mode: false # # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database,
                        # # and changes UPDATE of the data source to DELETE and REPLACE for the target database.
                        # # This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly.
                        # # In the first minute of starting or resuming an incremental migration task, DM automatically enables the safe mode.
    mysql-instances:
    - source-id: "mysql-replica-01"
       block-allow-list:  "bw-rule-1"
       route-rules: ["store-route-rule", "sale-route-rule"]
       filter-rules: ["store-filter-rule", "sale-filter-rule"]
       syncer-config-name: "global"
       meta:
         binlog-name: "mysql-bin.000002"
         binlog-pos: 246546174
         binlog-gtid: "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801"
    - source-id: "mysql-replica-02"
       block-allow-list:  "bw-rule-1"
       route-rules: ["store-route-rule", "sale-route-rule"]
       filter-rules: ["store-filter-rule", "sale-filter-rule"]
       syncer-config-name: "global"
       meta:
         binlog-name: "mysql-bin.000001"
         binlog-pos: 1312659
         binlog-gtid: "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036"

    ## ******** Configuration of the target TiDB cluster on TiDB Cloud **********
    target-database:       # The target TiDB cluster on TiDB Cloud
     host: "tidb.xxxxxxx.xxxxxxxxx.ap-northeast-1.prod.aws.tidbcloud.com"
     port: 4000
     user: "root"
     password: "${password}"  # If the password is not empty, it is recommended to use a dmctl-encrypted cipher.

    ## ******** Function Configuration **********
    routes:
     store-route-rule:
       schema-pattern: "store_*"
       target-schema: "store"
     sale-route-rule:
       schema-pattern: "store_*"
       table-pattern: "sale_*"
       target-schema: "store"
       target-table:  "sales"
    filters:
     sale-filter-rule:
       schema-pattern: "store_*"
       table-pattern: "sale_*"
       events: ["truncate table", "drop table", "delete"]
       action: Ignore
     store-filter-rule:
       schema-pattern: "store_*"
       events: ["drop database"]
       action: Ignore
    block-allow-list:
     bw-rule-1:
       do-dbs: ["store_*"]

    ## ******** Ignore check items **********
    ignore-checking-items: ["table_schema","auto_increment_ID"]
    ```

詳細なタスク構成については、 [DM タスク構成](https://docs.pingcap.com/tidb/stable/task-configuration-file-full)を参照してください。

データ複製タスクをスムーズに実行するために、DM はタスクの開始時に事前チェックを自動的にトリガーし、チェック結果を返します。 DM は、事前チェックに合格した後にのみレプリケーションを開始します。事前チェックを手動でトリガーするには、check-task コマンドを実行します。

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml
```

次に出力例を示します。

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml

{
   "result": true,
   "msg": "check pass!!!"
}
```

### ステップ 3. 複製タスクを開始する {#step-3-start-the-replication-task}

`tiup dmctl`を使用して次のコマンドを実行し、データ複製タスクを開始します。

```shell
[root@localhost ~]# tiup dmctl --master-addr ${advertise-addr}  start-task dm-task.yaml
```

上記のコマンドで使用されるパラメーターは、次のとおりです。

| パラメータ           | 説明                                                                             |
| --------------- | ------------------------------------------------------------------------------ |
| `--master-addr` | `dmctl`が接続されるクラスター内の任意の DM マスター ノードの`{advertise-addr}` 。例: 192.168.11.110:9261 |
| `start-task`    | 移行タスクを開始します。                                                                   |

次に出力例を示します。

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 start-task dm-task.yaml

{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-01",
           "worker": "dm-192.168.11.111-9262"
       },

       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-02",
           "worker": "dm-192.168.11.112-9262"
       }
   ],
   "checkResult": ""
}
```

タスクの開始に失敗した場合は、プロンプト メッセージを確認し、構成を修正します。その後、上記のコマンドを再実行してタスクを開始できます。

問題が発生した場合は、 [DM エラー処理](https://docs.pingcap.com/tidb/stable/dm-error-handling)および[DMFAQ](https://docs.pingcap.com/tidb/stable/dm-faq)を参照してください。

### 手順 4. レプリケーション タスクのステータスを確認する {#step-4-check-the-replication-task-status}

DM クラスターに進行中のレプリケーション タスクがあるかどうかを確認し、タスクの状態を表示するには、 `tiup dmctl`使用して`query-status`コマンドを実行します。

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 query-status test-task1
```

次に出力例を示します。

```shell
{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "sourceStatus": {
               "source": "mysql-replica-01",
               "worker": "dm-192.168.11.111-9262",
               "result": null,
               "relayStatus": null
           },

           "subTaskStatus": [
               {
                   "name": "test-task1",
                   "stage": "Running",
                   "unit": "Sync",
                   "result": null,
                   "unresolvedDDLLockID": "",
                   "sync": {
                       "totalEvents": "4048",
                       "totalTps": "3",
                       "recentTps": "3",
                       "masterBinlog": "(mysql-bin.000002, 246550002)",
                       "masterBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194813",
                       "syncerBinlog": "(mysql-bin.000002, 246550002)",
                       "syncerBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194813",
                       "blockingDDLs": [
                       ],
                       "unresolvedGroups": [
                       ],
                       "synced": true,
                       "binlogType": "remote",
                       "secondsBehindMaster": "0",
                       "blockDDLOwner": "",
                       "conflictMsg": ""
                   }
               }
           ]
       },
       {
           "result": true,
           "msg": "",
           "sourceStatus": {
               "source": "mysql-replica-02",
               "worker": "dm-192.168.11.112-9262",
               "result": null,
               "relayStatus": null
           },
           "subTaskStatus": [
               {
                   "name": "test-task1",
                   "stage": "Running",
                   "unit": "Sync",
                   "result": null,
                   "unresolvedDDLLockID": "",
                   "sync": {
                       "totalEvents": "33",
                       "totalTps": "0",
                       "recentTps": "0",
                       "masterBinlog": "(mysql-bin.000001, 1316487)",
                       "masterBinlogGtid": "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4048",
                       "syncerBinlog": "(mysql-bin.000001, 1316487)",
                       "syncerBinlogGtid": "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4048",
                       "blockingDDLs": [
                       ],
                       "unresolvedGroups": [
                       ],
                       "synced": true,
                       "binlogType": "remote",
                       "secondsBehindMaster": "0",
                       "blockDDLOwner": "",
                       "conflictMsg": ""
                   }
               }
           ]
       }
   ]
}
```

結果の詳細な解釈については、 [クエリのステータス](https://docs.pingcap.com/tidb/stable/dm-query-status)を参照してください。
