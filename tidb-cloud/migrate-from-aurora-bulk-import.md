---
title: Migrate from Amazon Aurora MySQL to TiDB Cloud in Bulk
summary: Learn how to migrate data from Amazon Aurora MySQL to TiDB Cloud in bulk.
---

# AuroraからTiDB Cloudに一括で移行する {#migrate-from-amazon-aurora-mysql-to-tidb-cloud-in-bulk}

このドキュメントでは、 TiDB Cloudコンソールのインポートツールを使用して、AmazonAuroraMySQLからAuroraTiDB Cloudにデータを一括で移行する方法について説明します。

## TiDB Cloudコンソールでインポートタスクを作成する方法を学ぶ {#learn-how-to-create-an-import-task-on-the-tidb-cloud-console}

データをインポートするには、次の手順を実行します。

1.  [TiDBクラスター]ページに移動し、ターゲットクラスタの名前をクリックします。ターゲットクラスタの概要ページが表示されます。

2.  左側のクラスタ情報ペインで、[**インポート**]をクリックします。 [<strong>データインポートタスク]</strong>ページが表示されます。

3.  [Amazon S3バケットを作成し、ソースデータファイルを準備する方法を学びます](#learn-how-to-create-an-amazon-s3-bucket-and-prepare-source-data-files)に従ってソースデータを準備します。データの準備の部分で、さまざまな**データ形式**の長所と短所を確認できます。

4.  ソースデータの仕様に従って、[**データソースタイプ**]、[<strong>バケットURL</strong> ]、および<strong>[データ形式]</strong>フィールドに入力します。

5.  クラスタの接続設定に従って、**ターゲットデータベース**の<strong>[ユーザー名]</strong>フィールドと[<strong>パスワード</strong>]フィールドに入力します。

6.  [クロスアカウントアクセスを構成する方法を学ぶ](#learn-how-to-configure-cross-account-access)に従って、クロスアカウントアクセスのバケットポリシーとロールを作成します。

7.  [**インポート]**をクリックします。

    データベースリソースの消費に関する警告メッセージが表示されます。

8.  [**確認]**をクリックします。

    TiDB Cloudは、指定されたバケットURLのデータにアクセスできるかどうかの検証を開始します。検証が完了して成功すると、インポートタスクが自動的に開始されます。 `AccessDenied`エラーが発生した場合は、 [S3からのデータインポート中のアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。

> **ノート：**
>
> タスクが失敗した場合は、 [不完全なデータをクリーンアップする方法を学ぶ](#learn-how-to-clean-up-incomplete-data)を参照してください。

## Amazon S3バケットを作成し、ソースデータファイルを準備する方法を学びます {#learn-how-to-create-an-amazon-s3-bucket-and-prepare-source-data-files}

データを準備するには、次の2つのオプションから1つを選択できます。

-   [オプション1：Dumplingを使用してソースデータファイルを準備する](#option-1-prepare-source-data-files-using-dumpling)

    EC2で[Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を起動し、データをAmazonS3にエクスポートする必要があります。エクスポートするデータは、ソースデータベースの現在の最新データです。これはオンラインサービスに影響を与える可能性があります。データをエクスポートするときに、Dumplingはテーブルをロックします。

-   [オプション2： Auroraスナップショットを使用してソースデータファイルを準備する](#option-2-prepare-source-data-files-using-amazon-aurora-snapshots)

    これはオンラインサービスに影響します。 Amazon Auroraのエクスポートタスクは、データをAmazon S3にエクスポートする前に、最初にデータベースを復元してスケーリングするため、データをエクスポートするときに時間がかかる場合があります。詳細については、 [DBスナップショットデータをAmazonS3にエクスポートする](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html)を参照してください。

### 事前チェックと準備 {#prechecks-and-preparations}

> **ノート：**
>
> 現在、2TBを超えるデータをインポートすることはお勧めしません。
>
> 移行を開始する前に、次の事前チェックと準備を行う必要があります。

#### 十分な空き容量を確保する {#ensure-enough-free-space}

TiDBクラスタの空き領域がデータのサイズよりも大きいことを確認してください。各TiKVノードに600GBの空き領域を予約することをお勧めします。需要を満たすために、TiKVノードをさらに追加できます。

#### データベースの照合順序セット設定を確認してください {#check-the-database-s-collation-set-settings}

現在、TiDBは`utf8_general_ci`と`utf8mb4_general_ci`の照合順序のみをサポートしています。データベースの照合順序設定を確認するには、 Auroraに接続されているMySQLターミナルで次のコマンドを実行します。

{{< copyable "" >}}

```sql
select * from ((select table_schema, table_name, column_name, collation_name from information_schema.columns where character_set_name is not null) union all (select table_schema, table_name, null, table_collation from information_schema.tables)) x where table_schema not in ('performance_schema', 'mysql', 'information_schema') and collation_name not in ('utf8_bin', 'utf8mb4_bin', 'ascii_bin', 'latin1_bin', 'binary', 'utf8_general_ci', 'utf8mb4_general_ci');
```

結果は次のとおりです。

```output
Empty set (0.04 sec)
```

TiDBが文字セットまたは照合順序をサポートしていない場合は、それらをサポートされているタイプに変換することを検討してください。詳細については、 [文字セットと照合](https://docs.pingcap.com/tidb/stable/character-set-and-collation)を参照してください。

### オプション1：Dumplingを使用してソースデータファイルを準備する {#option-1-prepare-source-data-files-using-dumpling}

次のデータエクスポートタスクを実行するには、EC2を準備する必要があります。追加料金を回避するために、 AuroraおよびS3と同じネットワーク上で実行することをお勧めします。

1.  EC2にDumplingをインストールします。

    {{< copyable "" >}}

    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    source ~/.bash_profile
    tiup install dumpling 
    ```

    上記のコマンドでは、プロファイルファイルのパスに`~/.bash_profile`を変更する必要があります。

2.  S3を書き込むためのDumplingに書き込み権限を付与します。

    > **ノート：**
    >
    > EC2にIAMロールを割り当てている場合は、アクセスキーとセキュリティキーの設定をスキップして、このEC2で直接Dumplingを実行できます。

    環境内のAWSアカウントのアクセスキーとセキュリティキーを使用して、書き込み権限を付与できます。データを準備するための特定のキーペアを作成し、準備が完了したらすぐにアクセスキーを取り消します。

    {{< copyable "" >}}

    ```bash
    export AWS_ACCESS_KEY_ID=AccessKeyID
    export AWS_SECRET_ACCESS_KEY=SecretKey
    ```

3.  ソースデータベースをS3にバックアップします。

    Dumplingを使用して、 Auroraからデータをエクスポートします。ご使用の環境に応じて、中括弧（&gt;）で内容を置き換えてから、以下のコマンドを実行してください。データをエクスポートするときにフィルタールールを使用する場合は、 [テーブルフィルター](https://docs.pingcap.com/tidb/stable/table-filter#cli)を参照してください。

    {{< copyable "" >}}

    ```bash
    export_username="<Aurora username>"
    export_password="<Aurora password>"
    export_endpoint="<the endpoint for Amazon Aurora MySQL>"
    # You will use the s3 url when you create importing task
    backup_dir="s3://<bucket name>/<backup dir>"
    s3_bucket_region="<bueckt_region>"

    # Use `tiup -- dumpling` instead if "flag needs an argument: 'h' in -h" is prompted for TiUP versions earlier than v1.8
    tiup dumpling \
    -u "$export_username" \
    -p "$export_password" \
    -P 3306 \
    -h "$export_endpoint" \
    --filetype sql \
    --threads 8 \
    -o "$backup_dir" \
    --consistency="none" \
    --s3.region="$s3_bucket_region" \
    -r 200000 \
    -F 256MiB
    ```

4.  TiDB Cloudのデータインポートタスクパネルで、**データ形式**として<strong>Dumpling</strong>を選択します。

### オプション2： Auroraスナップショットを使用してソースデータファイルを準備する {#option-2-prepare-source-data-files-using-amazon-aurora-snapshots}

#### データベースのスキーマをバックアップし、 TiDB Cloudで復元します {#back-up-the-schema-of-the-database-and-restore-on-tidb-cloud}

Auroraからデータを移行するには、データベースのスキーマをバックアップする必要があります。

1.  MySQLクライアントをインストールします。

    {{< copyable "" >}}

    ```bash
    yum install mysql -y
    ```

2.  データベースのスキーマをバックアップします。

    {{< copyable "" >}}

    ```bash
    export_username="<Aurora username>"
    export_endpoint="<Aurora endpoint>"
    export_database="<Database to export>"

    mysqldump -h ${export_endpoint} -u ${export_username} -p --ssl-mode=DISABLED -d${export_database} >db.sql
    ```

3.  データベースのスキーマをTiDB Cloudにインポートします。

    {{< copyable "" >}}

    ```bash
    dest_endpoint="<TiDB Cloud connect endpoint>"
    dest_username="<TiDB Cloud username>"
    dest_database="<Database to restore>"

    mysql -u ${dest_username} -h ${dest_endpoint} -P ${dest_port_number} -p -D${dest_database}<db.sql
    ```

4.  TiDB Cloudのデータインポートタスクパネルで、**データ形式**として<strong>Aurora</strong>を選択します。

#### スナップショットを取り、S3にエクスポートします {#take-a-snapshot-and-export-it-to-s3}

1.  Amazon RDSコンソールから[スナップショット]を選択し、[**スナップショット**の取得]をクリックして手動スナップ<strong>ショット</strong>を作成します。

2.  [**スナップショット名]**の下に空欄を入力します。 [<strong>スナップショットを撮る]を</strong>クリックします。スナップショットの作成が完了すると、スナップショットがスナップショットテーブルの下に表示されます。

3.  作成したスナップショットを選択し、[**アクション**]をクリックします。ドロップダウンボックスで、[ <strong>AmazonS3にエクスポート]を</strong>クリックします。

4.  **エクスポート識別子**の下の空白を埋めます。

5.  エクスポートするデータの量を選択します。このガイドでは、 **[すべて]**が選択されています。部分を選択して識別子を使用し、データベースのどの部分をエクスポートする必要があるかを決定することもできます。

6.  スナップショットを保存するS3バケットを選択します。セキュリティ上の懸念からデータを保存するための新しいバケットを作成できます。 TiDBクラスタと同じリージョンでバケットを使用することをお勧めします。リージョン間でデータをダウンロードすると、追加のネットワークコストが発生する可能性があります。

7.  適切なIAMロールを選択して、S3バケットへの書き込みアクセスを許可します。後でスナップショットをTiDB Cloudにインポートするときに使用されるため、この役割をメモしてください。

8.  適切なAWSKMSキーを選択し、 IAMロールがKMSキーユーザーにすでに追加されていることを確認します。ロールを追加するには、KSMサービスを選択し、キーを選択して、[**追加**]をクリックします。

9.  [ **AmazonS3のエクスポート]**をクリックします。タスクテーブルで進行状況を確認できます。

10. タスクテーブルから、宛先バケットを記録します（たとえば、 `s3://snapshot-bucket/snapshot-samples-1` ）。

## クロスアカウントアクセスを構成する方法を学ぶ {#learn-how-to-configure-cross-account-access}

TiDB CloudクラスタとS3バケットは異なるAWSアカウントにあります。 TiDB CloudクラスタがS3バケット内のソースデータファイルにアクセスできるようにするには、AmazonS3へのクロスアカウントアクセスを設定する必要があります。詳細については、 [AmazonS3アクセスを設定する](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-amazon-s3-access)を参照してください。

完了すると、クロスアカウントのポリシーとロールが作成されます。その後、 TiDB Cloudのデータインポートタスクパネルで設定を続行できます。

## フィルタルールを設定する方法を学ぶ {#learn-how-to-set-up-filter-rules}

[テーブルフィルター](https://docs.pingcap.com/tidb/stable/table-filter#cli)ドキュメントを参照してください。現在、 TiDB Cloudは1つのテーブルフィルタールールのみをサポートしています。

## 不完全なデータをクリーンアップする方法を学ぶ {#learn-how-to-clean-up-incomplete-data}

要件を再度確認できます。すべての問題が解決したら、不完全なデータベースを削除して、インポートプロセスを再開できます。
