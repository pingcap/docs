---
title: Migrate and Merge MySQL Shards of Large Datasets to TiDB Cloud
summary: 大規模なデータセットの MySQL シャードをTiDB Cloudに移行およびマージする方法を学びます。
---

# 大規模データセットのMySQLシャードをTiDB Cloudに移行および統合する {#migrate-and-merge-mysql-shards-of-large-datasets-to-tidb-cloud}

このドキュメントでは、大規模なMySQLデータセット（例えば1TiB以上）を異なるパーティションからTiDB Cloudに移行し、マージする方法について説明します。完全なデータ移行後、 [TiDB データ移行 (DM)](https://docs.pingcap.com/tidb/stable/dm-overview)使用してビジネスニーズに応じて増分移行を実行できます。

このドキュメントの例では、複数のMySQLインスタンスにまたがる複雑なシャード移行タスクを使用し、自動インクリメントの主キーにおける競合の処理を伴います。この例のシナリオは、単一のMySQLインスタンス内の異なるシャードテーブルからのデータのマージにも適用できます。

## 例の環境情報 {#environment-information-in-the-example}

このセクションでは、例で使用されるアップストリーム クラスタ、DM、およびダウンストリーム クラスタの基本情報について説明します。

### 上流クラスター {#upstream-cluster}

アップストリーム クラスターの環境情報は次のとおりです。

-   MySQLバージョン: MySQL v5.7.18
-   MySQLインスタンス1:
    -   スキーマ`store_01`と表`[sale_01, sale_02]`
    -   スキーマ`store_02`と表`[sale_01, sale_02]`
-   MySQLインスタンス2:
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

DMのバージョンはv5.3.0です。TiDB DMを手動でデプロイする必要があります。詳細な手順については、 [TiUPを使用して DMクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)参照してください。

### 外部storage {#external-storage}

このドキュメントでは、Amazon S3 を例として使用します。

### 下流クラスター {#downstream-cluster}

シャードされたスキーマとテーブルはテーブル`store.sales`にマージされます。

## MySQLからTiDB Cloudへの完全なデータ移行を実行する {#perform-full-data-migration-from-mysql-to-tidb-cloud}

以下は、MySQL シャードの全データをTiDB Cloudに移行してマージする手順です。

次の例では、テーブル内のデータを**CSV**形式でエクスポートするだけです。

### ステップ1. Amazon S3バケットにディレクトリを作成する {#step-1-create-directories-in-the-amazon-s3-bucket}

Amazon S3 バケットに、第 1 レベルのディレクトリ`store` （データベースのレベルに対応）と第 2 レベルのディレクトリ`sales` （テーブルのレベルに対応）を作成します`sales`で、各 MySQL インスタンス（MySQL インスタンスのレベルに対応）ごとに第 3 レベルのディレクトリを作成します。例:

-   MySQLインスタンス1のデータを`s3://dumpling-s3/store/sales/instance01/`に移行する
-   MySQLインスタンス2のデータを`s3://dumpling-s3/store/sales/instance02/`に移行する

複数のインスタンスにシャードがある場合は、データベースごとに1つの第1レベルディレクトリを作成し、シャードされたテーブルごとに1つの第2レベルディレクトリを作成します。次に、管理を容易にするために、各MySQLインスタンスごとに第3レベルディレクトリを作成します。例えば、MySQLインスタンス1とMySQLインスタンス2のテーブル`stock_N.product_N` TiDB Cloudのテーブル`stock.products`に移行してマージする場合、以下のディレクトリを作成できます。

-   `s3://dumpling-s3/stock/products/instance01/`
-   `s3://dumpling-s3/stock/products/instance02/`

### ステップ2. Dumplingを使用してデータをAmazon S3にエクスポートする {#step-2-use-dumpling-to-export-data-to-amazon-s3}

Dumplingのインストール方法については、 [Dumplingの紹介](https://docs.pingcap.com/tidb/stable/dumpling-overview)参照してください。

Dumplingを使用してデータを Amazon S3 にエクスポートする場合は、次の点に注意してください。

-   アップストリーム クラスターのbinlogを有効にします。
-   正しい Amazon S3 ディレクトリとリージョンを選択します。
-   上流クラスターへの影響を最小限に抑えるには、 `-t`オプションを設定して適切な同時実行性を選択するか、バックアップデータベースから直接エクスポートしてください。このパラメータの使用方法の詳細については、 [Dumplingのオプションリスト](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)参照してください。
-   `--filetype csv`と`--no-schemas`に適切な値を設定します。これらのパラメータの使用方法の詳細については、 [Dumplingのオプションリスト](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)参照してください。

CSV ファイルに次のように名前を付けます。

-   1つのテーブルのデータが複数のCSVファイルに分割されている場合は、これらのCSVファイルに数値の接尾辞を追加します。例： `${db_name}.${table_name}.000001.csv`と`${db_name}.${table_name}.000002.csv`数値の接尾辞は連続していなくても構いませんが、昇順である必要があります。また、すべての接尾辞の長さを揃えるため、数値の前にゼロを追加する必要があります。

> **注記：**
>
> 場合によっては、前述のルールに従って CSV ファイル名を更新できないことがあります (たとえば、CSV ファイル リンクが他のプログラムでも使用されている場合)。ファイル名を変更せずに、 [ステップ5](#step-5-perform-the-data-import-task)の**マッピング設定**を使用して、ソース データを単一のターゲット テーブルにインポートできます。

データを Amazon S3 にエクスポートするには、次の手順を実行します。

1.  Amazon S3 バケットの`AWS_ACCESS_KEY_ID`と`AWS_SECRET_ACCESS_KEY`取得します。

    ```shell
    [root@localhost ~]# export AWS_ACCESS_KEY_ID={your_aws_access_key_id}
    [root@localhost ~]# export AWS_SECRET_ACCESS_KEY= {your_aws_secret_access_key}
    ```

2.  MySQL インスタンス 1 から Amazon S3 バケット内の`s3://dumpling-s3/store/sales/instance01/`ディレクトリにデータをエクスポートします。

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql01-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance01/" --s3.region "ap-northeast-1"
    ```

    パラメータの詳細については、 [Dumplingのオプションリスト](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)参照してください。

3.  MySQL インスタンス 2 から Amazon S3 バケット内の`s3://dumpling-s3/store/sales/instance02/`ディレクトリにデータをエクスポートします。

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql02-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance02/" --s3.region "ap-northeast-1"
    ```

詳細な手順については、 [Amazon S3クラウドstorageにデータをエクスポートする](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-data-to-amazon-s3-cloud-storage)参照してください。

### ステップ3. TiDB Cloudクラスターでスキーマを作成する {#step-3-create-schemas-in-tidb-cloud-cluster}

次のように、 TiDB Cloudクラスターにスキーマを作成します。

```sql
mysql> CREATE DATABASE store;
Query OK, 0 rows affected (0.16 sec)
mysql> use store;
Database changed
```

この例では、上流テーブル`sale_01`と`sale_02`の列IDは自動増分主キーです。下流データベースでシャードテーブルをマージすると、競合が発生する可能性があります。次のSQL文を実行して、ID列を主キーではなく通常のインデックスとして設定します。

```sql
mysql> CREATE TABLE `sales` (
         `id` bigint(20) NOT NULL ,
         `uid` varchar(40) NOT NULL,
         `sale_num` bigint DEFAULT NULL,
         INDEX (`id`),
         UNIQUE KEY `ind_uid` (`uid`)
        );
Query OK, 0 rows affected (0.17 sec)
```

このような競合を解決するためのソリューションの詳細については、 [列からPRIMARY KEY属性を削除します](https://docs.pingcap.com/tidb/stable/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column)参照してください。

### ステップ4. Amazon S3アクセスを構成する {#step-4-configure-amazon-s3-access}

[Amazon S3 アクセスを構成する](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)の手順に従って、ソース データにアクセスするためのロール ARN を取得します。

以下の例では、主要なポリシー設定のみをリストしています。Amazon S3 パスを実際の値に置き換えてください。

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

### ステップ5. データインポートタスクを実行する {#step-5-perform-the-data-import-task}

Amazon S3 アクセスを構成したら、次のようにしてTiDB Cloudコンソールでデータ インポート タスクを実行できます。

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

        > **ヒント：**
        >
        > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

2.  **「Cloud Storage からデータをインポート」**を選択し、 **「Amazon S3」**をクリックします。

3.  **「Amazon S3 からのデータのインポート」**ページで、次の情報を入力します。

    -   **インポートファイル数**： TiDB Cloud Serverlessの場合は**「複数ファイル」**を選択してください。このフィールドはTiDB Cloud Dedicatedでは使用できません。
    -   **含まれるスキーマ ファイル**: **[いいえ]**を選択します。
    -   **データ形式**: **CSV**を選択します。
    -   **フォルダURI** : ソースデータのバケットURIを入力します。テーブルに対応する第2階層のディレクトリ（この例では`s3://dumpling-s3/store/sales/` ）を使用すると、 TiDB CloudはすべてのMySQLインスタンスのデータを一度に`store.sales`のインスタンスにインポートしてマージできます。
    -   **バケットアクセス**&gt; **AWS ロール ARN** : 取得したロール ARN を入力します。

    バケットの場所がクラスターと異なる場合は、クロスリージョンのコンプライアンスを確認してください。

    TiDB Cloudは、指定されたバケットURI内のデータにアクセスできるかどうかの検証を開始します。検証後、 TiDB Cloudはデフォルトのファイル名パターンを使用してデータソース内のすべてのファイルをスキャンし、次のページの左側にスキャンの概要結果を返します。1 `AccessDenied`エラーが発生した場合は、 [S3 からのデータインポート中に発生するアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)参照してください。

4.  **[接続]**をクリックします。

5.  **[宛先]**セクションで、ターゲット データベースとテーブルを選択します。

    複数のファイルをインポートする場合、 **「詳細設定」** &gt; **「マッピング設定」**を使用して、各ターゲットテーブルとそれに対応するCSVファイルに対してカスタムマッピングルールを定義できます。その後、データソースファイルは指定されたカスタムマッピングルールに基づいて再スキャンされます。

    ソースファイルのURIと名前を**「ソースファイルのURIと名前」**に入力する際は、必ず次の形式`s3://[bucket_name]/[data_source_folder]/[file_name].csv`に従ってください。例えば、 `s3://sampledata/ingest/TableName.01.csv` 。

    ソースファイルの一致にはワイルドカードも使用できます。例:

    -   `s3://[bucket_name]/[data_source_folder]/my-data?.csv` : そのフォルダー内の`my-data`で始まり、その後に 1 文字 ( `my-data1.csv`や`my-data2.csv`など) が続くすべての CSV ファイルが同じターゲット テーブルにインポートされます。

    -   `s3://[bucket_name]/[data_source_folder]/my-data*.csv` : フォルダー内の`my-data`で始まるすべての CSV ファイルが同じターゲット テーブルにインポートされます。

    サポートされているのは`?`と`*`のみであることに注意してください。

    > **注記：**
    >
    > URI にはデータ ソース フォルダーが含まれている必要があります。

6.  必要に応じて CSV 構成を編集します。

    また、 **「CSV 構成の編集」を**クリックして、バックスラッシュ エスケープ、セパレーター、および区切り文字を構成し、よりきめ細かな制御を行うこともできます。

    > **注記：**
    >
    > セパレーター、区切り文字、およびNULLの設定では、英数字と特定の特殊文字の両方を使用できます。サポートされている特殊文字には、 `\t` 、 `\b` 、 `\n` 、 `\r` 、 `\f` 、 `\u0001`が含まれます。

7.  **[インポートの開始]を**クリックします。

8.  インポートの進行状況に**「完了」と**表示されたら、インポートされたテーブルを確認します。

データがインポートされた後、 TiDB Cloudの Amazon S3 アクセスを削除する場合は、追加したポリシーを削除するだけです。

## MySQLからTiDB Cloudへの増分データレプリケーションを実行する {#perform-incremental-data-replication-from-mysql-to-tidb-cloud}

アップストリーム クラスター内の指定された位置からbinlogに基づいてデータの変更をTiDB Cloudに複製するには、TiDB Data Migration (DM) を使用して増分レプリケーションを実行できます。

### 始める前に {#before-you-begin}

増分データを移行し、MySQLシャードをTiDB Cloudにマージする場合、 TiDB Cloud はMySQLシャードの移行とマージをまだサポートしていないため、TiDB DMを手動でデプロイする必要があります。詳細な手順については、 [TiUPを使用して DMクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)参照してください。

### ステップ1. データソースを追加する {#step-1-add-the-data-source}

1.  DMにアップストリームデータソースを設定するために、新しいデータソースファイル`dm-source1.yaml`を作成します。以下の内容を追加します。

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

2.  別の新しいデータ ソース ファイル`dm-source2.yaml`を作成し、次のコンテンツを追加します。

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

3.  ターミナルで次のコマンドを実行します。1 `tiup dmctl`使用して、最初のデータソース構成をDMクラスターにロードします。

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr ${advertise-addr} operate-source create dm-source1.yaml
    ```

    上記のコマンドで使用されるパラメータは次のとおりです。

    | パラメータ                   | 説明                                                                      |
    | ----------------------- | ----------------------------------------------------------------------- |
    | `--master-addr`         | `dmctl`が接続されるクラスタ内の任意のDMマスターノードの`{advertise-addr}`例：192.168.11.110:9261 |
    | `operate-source create` | データ ソースを DM クラスターにロードします。                                               |

    出力例は次のとおりです。

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

4.  ターミナルで次のコマンドを実行します。1 `tiup dmctl`使用して、2番目のデータソース構成をDMクラスターにロードします。

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source2.yaml
    ```

    出力例は次のとおりです。

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

### ステップ2. レプリケーションタスクを作成する {#step-2-create-a-replication-task}

1.  レプリケーション タスク用に`test-task1.yaml`ファイルを作成します。

2.  Dumplingによってエクスポートされた MySQL インスタンス 1 のメタデータファイルで開始点を見つけます。例:

    ```toml
    Started dump at: 2022-05-25 10:16:26
    SHOW MASTER STATUS:
           Log: mysql-bin.000002
           Pos: 246546174
           GTID:b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801
    Finished dump at: 2022-05-25 10:16:27
    ```

3.  Dumplingによってエクスポートされた MySQL インスタンス2 のメタデータファイルで開始点を見つけます。例:

    ```toml
    Started dump at: 2022-05-25 10:20:32
    SHOW MASTER STATUS:
           Log: mysql-bin.000001
           Pos: 1312659
           GTID:cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036
    Finished dump at: 2022-05-25 10:20:32
    ```

4.  タスク構成ファイル`test-task1`を編集して、各データ ソースの増分レプリケーション モードとレプリケーション開始点を構成します。

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

詳細なタスク構成については、 [DM タスク構成](https://docs.pingcap.com/tidb/stable/task-configuration-file-full)参照してください。

データレプリケーションタスクをスムーズに実行するために、DMはタスク開始時に自動的に事前チェックを実行し、チェック結果を返します。DMは事前チェックに合格した場合にのみレプリケーションを開始します。事前チェックを手動で実行するには、check-taskコマンドを実行します。

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml
```

出力例は次のとおりです。

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml

{
   "result": true,
   "msg": "check pass!!!"
}
```

### ステップ3. レプリケーションタスクを開始する {#step-3-start-the-replication-task}

`tiup dmctl`使用して次のコマンドを実行し、データ複製タスクを開始します。

```shell
[root@localhost ~]# tiup dmctl --master-addr ${advertise-addr}  start-task dm-task.yaml
```

上記のコマンドで使用されるパラメータは次のとおりです。

| パラメータ           | 説明                                                                      |
| --------------- | ----------------------------------------------------------------------- |
| `--master-addr` | `dmctl`が接続されるクラスタ内の任意のDMマスターノードの`{advertise-addr}`例：192.168.11.110:9261 |
| `start-task`    | 移行タスクを開始します。                                                            |

出力例は次のとおりです。

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

タスクの開始に失敗した場合は、プロンプトメッセージを確認し、設定を修正してください。その後、上記のコマンドを再実行してタスクを開始できます。

問題が発生した場合は、 [DMエラー処理](https://docs.pingcap.com/tidb/stable/dm-error-handling)と[DMFAQ](https://docs.pingcap.com/tidb/stable/dm-faq)を参照してください。

### ステップ4. レプリケーションタスクのステータスを確認する {#step-4-check-the-replication-task-status}

DM クラスターに進行中のレプリケーション タスクがあるかどうかを確認し、タスクのステータスを表示するには、 `tiup dmctl`使用して`query-status`コマンドを実行します。

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 query-status test-task1
```

出力例は次のとおりです。

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

結果の詳細な解釈については、 [クエリステータス](https://docs.pingcap.com/tidb/stable/dm-query-status)参照してください。
