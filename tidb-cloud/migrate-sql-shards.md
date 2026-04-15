---
title: Migrate and Merge MySQL Shards of Large Datasets to TiDB Cloud
summary: 大規模データセットのMySQLシャードをTiDB Cloudに移行およびマージする方法を学びましょう。
---

# 大規模データセットのMySQLシャードをTiDB Cloudに移行およびマージする {#migrate-and-merge-mysql-shards-of-large-datasets-to-tidb-cloud}

このドキュメントでは、異なるパーティションに分散した大規模な MySQL データセット (例えば、1 TiB 以上) をTiDB Cloudに移行および統合する方法について説明します。データ移行が完了したら、 [TiDBデータ移行（DM）](https://docs.pingcap.com/tidb/stable/dm-overview)を使用して、ビジネスニーズに応じて増分移行を実行できます。

このドキュメントの例では、複数のMySQLインスタンスにまたがる複雑なシャード移行タスクを使用しており、自動インクリメント主キーの競合処理が含まれています。この例のシナリオは、単一のMySQLインスタンス内の異なるシャードテーブルのデータをマージする場合にも適用できます。

## 例の環境情報 {#environment-information-in-the-example}

このセクションでは、例で使用されているアップストリームクラスタ、DM、およびダウンストリームTiDB Cloudの基本情報について説明します。

### 上流クラスター {#upstream-cluster}

上流クラスターの環境情報は以下のとおりです。

-   MySQLバージョン：MySQL v5.7.18
-   MySQLインスタンス1：
    -   スキーマ`store_01`およびテーブル`[sale_01, sale_02]`
    -   スキーマ`store_02`およびテーブル`[sale_01, sale_02]`
-   MySQLインスタンス2：
    -   スキーマ`store_01`およびテーブル`[sale_01, sale_02]`
    -   スキーマ`store_02`およびテーブル`[sale_01, sale_02]`
-   テーブル構造：

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

DM のバージョンは v5.3.0 です。 TiDB DM を手動でデプロイする必要があります。詳細な手順については、 [TiUPを使用してDMクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)を参照してください。

### 外部storage {#external-storage}

この文書では、Amazon S3を例として使用します。

### TiDB Cloudのダウンストリーム {#downstream-tidb-cloud}

シャーディングされたスキーマとテーブルは、テーブル`store.sales`にマージされます。

## MySQLからTiDB Cloudへの完全なデータ移行を実行する {#perform-full-data-migration-from-mysql-to-tidb-cloud}

以下は、MySQLシャードの全データをTiDB Cloudに移行およびマージする手順です。

以下の例では、テーブル内のデータを**CSV**形式にエクスポートするだけで済みます。

### ステップ1. Amazon S3バケット内にディレクトリを作成する {#step-1-create-directories-in-the-amazon-s3-bucket}

Amazon S3 バケット内に、第 1 階層ディレクトリ`store` (データベースのレベルに対応) と第 2 階層ディレクトリ`sales` (テーブルのレベルに対応) を作成します。 `sales`内に、MySQL インスタンスごとに第 3 階層ディレクトリ (MySQL インスタンスのレベルに対応) を作成します。例:

-   MySQLインスタンス1のデータを`s3://dumpling-s3/store/sales/instance01/`に移行します。
-   MySQLインスタンス2のデータを`s3://dumpling-s3/store/sales/instance02/`に移行します。

複数のインスタンスにシャードがある場合は、データベースごとに第 1 レベルのディレクトリを 1 つ作成し、シャードされたテーブルごとに第 2 レベルのディレクトリを 1 つ作成します。次に、管理を容易にするために、MySQL インスタンスごとに第 3 レベルのディレクトリを作成します。たとえば、MySQL インスタンス 1 と MySQL インスタンス 2 のテーブル`stock_N.product_N`をTiDB Cloudのテーブル`stock.products`に移行およびマージする場合は、次のディレクトリを作成できます。

-   `s3://dumpling-s3/stock/products/instance01/`
-   `s3://dumpling-s3/stock/products/instance02/`

### ステップ2. Dumplingを使用してデータをAmazon S3にエクスポートする {#step-2-use-dumpling-to-export-data-to-amazon-s3}

Dumpling のインストール方法については、 [Dumplingの紹介](https://docs.pingcap.com/tidb/stable/dumpling-overview)参照してください。

Dumplingを使用してデータをAmazon S3にエクスポートする場合、以下の点に注意してください。

-   アップストリームクラスターのbinlogを有効にします。
-   適切なAmazon S3ディレクトリとリージョンを選択してください。
-   上流クラスタへの影響を最小限に抑えるには、 `-t`オプションを設定して適切な同時実行数を選択するか、バックアップ データベースから直接エクスポートしてください。このパラメータの使用方法の詳細については、 [Dumplingのオプション一覧](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)参照してください。
-   `--filetype csv`と`--no-schemas`に適切な値を設定します。これらのパラメーターの使用方法の詳細については、 [Dumplingのオプション一覧](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)参照してください。

CSVファイルの名前は以下のようにしてください。

-   1つのテーブルのデータが複数のCSVファイルに分割されている場合は、これらのCSVファイルに数値サフィックスを追加してください。例えば、 `${db_name}.${table_name}.000001.csv`と`${db_name}.${table_name}.000002.csv`のようにです。数値サフィックスは連続していなくても構いませんが、昇順である必要があります。また、すべてのサフィックスの長さが同じになるように、数値の前にゼロを追加する必要があります。

> **注記：**
>
> 場合によっては、前述のルールに従ってCSVファイル名を更新できない場合（たとえば、CSVファイルリンクが他のプログラムでも使用されている場合）、ファイル名を変更せずに、[ステップ5](#step-5-perform-the-data-import-task)の**マッピング設定**を使用してソースデータを単一のターゲットテーブルにインポートできます。

データをAmazon S3にエクスポートするには、以下の手順を実行してください。

1.  Amazon S3 バケットの`AWS_ACCESS_KEY_ID`と`AWS_SECRET_ACCESS_KEY`を取得します。

    ```shell
    [root@localhost ~]# export AWS_ACCESS_KEY_ID={your_aws_access_key_id}
    [root@localhost ~]# export AWS_SECRET_ACCESS_KEY= {your_aws_secret_access_key}
    ```

2.  MySQL instance1 から Amazon S3 バケット内の`s3://dumpling-s3/store/sales/instance01/`ディレクトリにデータをエクスポートします。

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql01-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance01/" --s3.region "ap-northeast-1"
    ```

    パラメータの詳細については、 [Dumplingのオプション一覧](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)参照してください。

3.  MySQL instance2 から Amazon S3 バケット内の`s3://dumpling-s3/store/sales/instance02/`ディレクトリにデータをエクスポートします。

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql02-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance02/" --s3.region "ap-northeast-1"
    ```

詳細な手順については、 [データをAmazon S3クラウドstorageにエクスポートする](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-data-to-amazon-s3-cloud-storage)参照してください。

### ステップ3. スキーマを作成します<customcontent plan="starter">TiDB Cloud Starterインスタンス</customcontent><customcontent plan="essential">TiDB Cloud Essentialインスタンス</customcontent><customcontent plan="premium">TiDB Cloud Premiumインスタンス</customcontent><customcontent plan="dedicated">TiDB Cloud Dedicatedクラスター</customcontent> {#step-3-create-schemas-in-customcontent-plan-starter-tidb-cloud-starter-instance-customcontent-customcontent-plan-essential-tidb-cloud-essential-instance-customcontent-customcontent-plan-premium-tidb-cloud-premium-instance-customcontent-customcontent-plan-dedicated-tidb-cloud-dedicated-cluster-customcontent}

<CustomContent plan="starter">TiDB Cloud Starterインスタンス</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>でスキーマを次のように作成します。

```sql
mysql> CREATE DATABASE store;
Query OK, 0 rows affected (0.16 sec)
mysql> use store;
Database changed
```

この例では、上流テーブル`sale_01`と`sale_02`の列 ID は自動インクリメント主キーです。下流データベースでシャーディングされたテーブルをマージすると、競合が発生する可能性があります。次の SQL ステートメントを実行して、ID 列を主キーではなく通常のインデックスとして設定します。

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

このような競合を解決する解決策の詳細については、 [列からPRIMARY KEY属性を削除します](https://docs.pingcap.com/tidb/stable/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column)参照してください。

### ステップ4. Amazon S3へのアクセスを設定する {#step-4-configure-amazon-s3-access}

[Amazon S3へのアクセスを設定する](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)」の手順に従って、ソースデータにアクセスするためのロール ARN を取得します。

以下の例では、主要なポリシー設定のみを示しています。Amazon S3 のパスを、ご自身の値に置き換えてください。

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

### ステップ5．データインポートタスクを実行する {#step-5-perform-the-data-import-task}

Amazon S3へのアクセスを設定した後、 TiDB Cloudコンソールで次のようにデータインポートタスクを実行できます。

1.  ターゲットの<CustomContent plan="starter">TiDB Cloud Starterインスタンス</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>の**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  ターゲットの<CustomContent plan="starter">TiDB Cloud Starterインスタンス</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>の名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート] を**クリックします。

2.  **「クラウドストレージからデータをインポート」**を選択し、次に**「Amazon S3」**をクリックします。

3.  **Amazon S3からデータをインポートする**ページで、以下の情報を入力してください。

    -   **インポートするファイル数**： TiDB Cloud StarterまたはTiDB Cloud Essentialの場合は、 **「複数のファイル」**を選択してください。このフィールドはTiDB Cloud Dedicatedでは利用できません。
    -   **含まれるスキーマ ファイル**:**いいえ**を選択します。
    -   **データ形式**： **CSV**を選択してください。
    -   **フォルダー URI** : ソース データのバケット URI を入力してください。この例では、テーブルに対応する第 2 階層のディレクトリ`s3://dumpling-s3/store/sales/`を使用することで、 TiDB Cloud はすべての MySQL インスタンスのデータを`store.sales`に一度にインポートしてマージできます。
    -   **バケットアクセス**&gt; **AWSロールARN** ：取得したロールARNを入力してください。

    バケットの場所が<CustomContent plan="starter">TiDB Cloud Starterインスタンス</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>クラスターと異なる場合は、クロスリージョンのコンプライアンスを確認してください。

    TiDB Cloudは、指定されたバケット URI 内のデータにアクセスできるかどうかの検証を開始します。検証後、 TiDB Cloudはデフォルトのファイル命名パターンを使用してデータ ソース内のすべてのファイルのスキャンを試行し、次のページの左側にスキャンの概要結果を返します。 `AccessDenied`エラーが発生した場合は、 [S3からのデータインポート中に発生するアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)参照してください。

4.  **「接続」**をクリックしてください。

5.  **「宛先」**セクションで、対象のデータベースとテーブルを選択します。

    複数のファイルをインポートする場合、 **「詳細設定」** ＞ **「マッピング設定」**を使用して、各ターゲットテーブルとその対応するCSVファイルごとにカスタムマッピングルールを定義できます。その後、データソースファイルは、指定されたカスタムマッピングルールを使用して再スキャンされます。

    ソースファイルURIと名前を**「ソースファイルURIと名前」**に入力する際は、 `s3://[bucket_name]/[data_source_folder]/[file_name].csv`の形式になっていることを確認してください。例: `s3://sampledata/ingest/TableName.01.csv` 。

    ワイルドカードを使用してソースファイルを照合することもできます。例：

    -   `s3://[bucket_name]/[data_source_folder]/my-data?.csv` : そのフォルダ内の`my-data`で始まり、その後に 1 文字が続くすべての CSV ファイル (例えば`my-data1.csv`や`my-data2.csv` ) は、同じターゲット テーブルにインポートされます。

    -   `s3://[bucket_name]/[data_source_folder]/my-data*.csv` : `my-data`で始まるフォルダ内のすべての CSV ファイルは、同じターゲット テーブルにインポートされます。

    `?`と`*`のみがサポートされていることに注意してください。

    > **注記：**
    >
    > URIにはデータソースフォルダを含める必要があります。

6.  必要に応じてCSV設定を編集してください。

    また、 **「CSV設定の編集」を**クリックすると、バックスラッシュエスケープ、セパレータ、区切り文字を設定して、より詳細な制御を行うことができます。

    > **注記：**
    >
    > セパレータ、デリミタ、およびヌルの設定には、英数字と特定の特殊文字の両方を使用できます。サポートされている特殊文字には、 `\t` 、 `\b` 、 `\n` 、 `\r` 、 `\f` 、および`\u0001`が含まれます。

7.  **「インポート開始」**をクリックしてください。

8.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。

データのインポート後、 TiDB CloudのAmazon S3アクセスを削除したい場合は、追加したポリシーを削除するだけで済みます。

## MySQLからTiDB Cloudへの増分データレプリケーションを実行する {#perform-incremental-data-replication-from-mysql-to-tidb-cloud}

上流クラスタの指定された位置からbinlogに基づいてデータ変更をTiDB Cloudに複製するには、TiDBデータ移行（DM）を使用して増分レプリケーションを実行できます。

### 始める前に {#before-you-begin}

増分データを移行し、MySQL シャードをTiDB Cloudにマージする場合は、TiDB DM を手動でデプロイする必要があります。これは、 TiDB Cloud がMySQL シャードの移行とマージをまだサポートしていないためです。詳細な手順については、 [TiUPを使用してDMクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)を参照してください。

### ステップ1. データソースを追加する {#step-1-add-the-data-source}

1.  DMにアップストリームデータソースを設定するために、新しいデータソースファイル`dm-source1.yaml`を作成します。以下の内容を追加してください。

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

2.  別の新しいデータソースファイル`dm-source2.yaml`を作成し、以下の内容を追加してください。

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

3.  ターミナルで次のコマンドを実行します。 `tiup dmctl`を使用して、最初のデータソース構成をDMクラスタにロードします。

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr ${advertise-addr} operate-source create dm-source1.yaml
    ```

    上記のコマンドで使用されるパラメータは、以下のように説明されます。

    | パラメータ                   | 説明                                                                        |
    | ----------------------- | ------------------------------------------------------------------------- |
    | `--master-addr`         | `{advertise-addr}`が接続されるクラスタ内の任意のDMマスターノードの`dmctl` 。例：192.168.11.110:9261 |
    | `operate-source create` | データソースをDMクラスターにロードします。                                                    |

    以下は出力例です。

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

4.  ターミナルで次のコマンドを実行します。 `tiup dmctl`を使用して、2番目のデータソース構成をDMクラスタにロードします。

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source2.yaml
    ```

    以下は出力例です。

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

1.  レプリケーションタスク用に`test-task1.yaml`ファイルを作成します。

2.  DumplingによってエクスポートされたMySQLインスタンス1のメタデータファイルから開始点を見つけます。例：

    ```toml
    Started dump at: 2022-05-25 10:16:26
    SHOW MASTER STATUS:
           Log: mysql-bin.000002
           Pos: 246546174
           GTID:b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801
    Finished dump at: 2022-05-25 10:16:27
    ```

3.  DumplingによってエクスポートされたMySQLインスタンス2のメタデータファイル内で開始点を見つけます。例：

    ```toml
    Started dump at: 2022-05-25 10:20:32
    SHOW MASTER STATUS:
           Log: mysql-bin.000001
           Pos: 1312659
           GTID:cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036
    Finished dump at: 2022-05-25 10:20:32
    ```

4.  タスク構成ファイル`test-task1`を編集して、各データソースの増分レプリケーションモードとレプリケーション開始点を設定します。

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

    ## ******** Configuration of the target TiDB database on TiDB Cloud **********
    target-database:       # The target TiDB database on TiDB Cloud
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

タスク構成の詳細については、 [DMタスク構成](https://docs.pingcap.com/tidb/stable/task-configuration-file-full)参照してください。

データレプリケーションタスクをスムーズに実行するために、DM はタスクの開始時に自動的に事前チェックをトリガーし、チェック結果を返します。DM は事前チェックに合格した後にのみレプリケーションを開始します。事前チェックを手動でトリガーするには、check-task コマンドを実行します。

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml
```

以下は出力例です。

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml

{
   "result": true,
   "msg": "check pass!!!"
}
```

### ステップ3. レプリケーションタスクを開始します {#step-3-start-the-replication-task}

`tiup dmctl`を使用して、次のコマンドを実行し、データレプリケーションタスクを開始します。

```shell
[root@localhost ~]# tiup dmctl --master-addr ${advertise-addr}  start-task dm-task.yaml
```

上記のコマンドで使用されるパラメータは、以下のように説明されます。

| パラメータ           | 説明                                                                        |
| --------------- | ------------------------------------------------------------------------- |
| `--master-addr` | `{advertise-addr}`が接続されるクラスタ内の任意のDMマスターノードの`dmctl` 。例：192.168.11.110:9261 |
| `start-task`    | 移行タスクを開始します。                                                              |

以下は出力例です。

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

タスクの開始に失敗した場合は、プロンプトメッセージを確認し、設定を修正してください。その後、上記のコマンドを再度実行してタスクを開始できます。

問題が発生した場合は、 [DMエラー処理](https://docs.pingcap.com/tidb/stable/dm-error-handling)および[DMに関するFAQ](https://docs.pingcap.com/tidb/stable/dm-faq)を参照してください。

### ステップ4．レプリケーションタスクのステータスを確認する {#step-4-check-the-replication-task-status}

DM クラスターでレプリケーション タスクが進行中かどうかを確認し、タスクの状態を表示するには、 `query-status`を使用して`tiup dmctl`コマンドを実行します。

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 query-status test-task1
```

以下は出力例です。

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
