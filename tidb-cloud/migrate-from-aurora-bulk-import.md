---
title: Migrate from Amazon Aurora MySQL to TiDB Cloud in Bulk
summary: Learn how to migrate data from Amazon Aurora MySQL to TiDB Cloud in bulk.
---

# Amazon Aurora MySQL からTiDB Cloudへ一括移行 {#migrate-from-amazon-aurora-mysql-to-tidb-cloud-in-bulk}

このドキュメントでは、 TiDB Cloudコンソールのインポート ツールを使用して、Amazon Aurora MySQL からTiDB Cloudにデータを一括移行する方法について説明します。

## TiDB Cloudコンソールでインポート タスクを作成する方法を学習します。 {#learn-how-to-create-an-import-task-in-the-tidb-cloud-console}

データをインポートするには、次の手順を実行します。

1.  ターゲットクラスターの**インポート**ページを開きます。

    1.  [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)にログインし、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅にある ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **[インポート]**ページで、右上隅の**[データのインポート]**をクリックし、 **[S3 から]**を選択します。

3.  [<a href="#learn-how-to-create-an-amazon-s3-bucket-and-prepare-source-data-files">Amazon S3 バケットを作成し、ソース データ ファイルを準備する方法を学習します。</a>](#learn-how-to-create-an-amazon-s3-bucket-and-prepare-source-data-files)に従ってソースデータを準備します。ソース データ ファイルの準備の部分で、さまざまなデータ形式の長所と短所を確認できます。

4.  ソース データの仕様に従って、 **[データ形式]** 、 **[バケット URI]** 、および**[ロール ARN]**フィールドを選択または入力します。クロスアカウント アクセス用のバケット ポリシーとロールを作成する方法の詳細については、 [<a href="/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access">Amazon S3 アクセスを設定する</a>](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

5.  **ターゲット データベース**のクラスター名とリージョン名を確認します。 **「次へ」**をクリックします。

    TiDB Cloudは、指定されたバケット URI 内のデータにアクセスできるかどうかの検証を開始します。検証後、 TiDB Cloudはデフォルトのファイル命名パターンを使用してデータ ソース内のすべてのファイルのスキャンを試行し、次のページの左側にスキャンの概要結果を返します。 `AccessDenied`エラーが発生した場合は、 [<a href="/tidb-cloud/troubleshoot-import-access-denied-error.md">S3 からのデータインポート中のアクセス拒否エラーのトラブルシューティング</a>](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。

6.  必要に応じて、テーブル フィルター ルールを追加します。 **「次へ」**をクリックします。

    -   **テーブル フィルター**: インポートするテーブルをフィルターする場合は、この領域でテーブル フィルター ルールを指定できます。

        例えば：

        -   `db01.*` : `db01`データベース内のすべてのテーブルがインポートされます。
        -   `!db02.*` : `db02`データベース内のテーブルを除き、他のすべてのテーブルがインポートされます。 `!`は、インポートする必要のないテーブルを除外するために使用されます。
        -   `*.*` : すべてのテーブルがインポートされます。

        詳細については、 [<a href="/table-filter.md#syntax">テーブルフィルターの構文</a>](/table-filter.md#syntax)を参照してください。

7.  **[プレビュー]**ページで、インポートするデータを確認し、 **[インポートの開始]**をクリックします。

> **ノート：**
>
> タスクが失敗した場合は、 [<a href="#learn-how-to-clean-up-incomplete-data">不完全なデータをクリーンアップする方法を学ぶ</a>](#learn-how-to-clean-up-incomplete-data)を参照してください。

## Amazon S3 バケットを作成し、ソース データ ファイルを準備する方法を学習します。 {#learn-how-to-create-an-amazon-s3-bucket-and-prepare-source-data-files}

データを準備するには、次の 2 つのオプションから 1 つを選択できます。

-   [<a href="#option-1-prepare-source-data-files-using-dumpling">オプション 1: Dumplingを使用してソース データ ファイルを準備する</a>](#option-1-prepare-source-data-files-using-dumpling)

    EC2 で[<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md)起動し、データを Amazon S3 にエクスポートする必要があります。エクスポートするデータは、ソース データベースの現在の最新データです。これはオンライン サービスに影響を与える可能性があります。 Dumpling は、データをエクスポートするときにテーブルをロックします。

-   [<a href="#option-2-prepare-source-data-files-using-amazon-aurora-snapshots">オプション 2: Amazon Auroraスナップショットを使用してソース データ ファイルを準備する</a>](#option-2-prepare-source-data-files-using-amazon-aurora-snapshots)

    これはオンライン サービスに影響します。 Amazon Auroraのエクスポート タスクは、データを Amazon S3 にエクスポートする前に、まずデータベースを復元してスケーリングするため、データのエクスポートには時間がかかる場合があります。詳細については、 [<a href="https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html">DB スナップショット データを Amazon S3 にエクスポートする</a>](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html)を参照してください。

### 事前チェックと準備 {#prechecks-and-preparations}

> **ノート：**
>
> 現時点では、2 TB を超えるデータをインポートすることはお勧めできません。
>
> 移行を開始する前に、次の事前チェックと準備を行う必要があります。

#### 十分な空き容量を確保する {#ensure-enough-free-space}

TiDB クラスターの空きスペースがデータのサイズよりも大きいことを確認してください。各 TiKV ノードに 600 GB の空き領域を予約することをお勧めします。要求を満たすために、さらに TiKV ノードを追加できます。

#### データベースの照合順序セット設定を確認してください {#check-the-database-s-collation-set-settings}

現在、TiDB は`utf8_general_ci`および`utf8mb4_general_ci`照合順序のみをサポートしています。データベースの照合順序設定を確認するには、 Auroraに接続されている MySQL ターミナルで次のコマンドを実行します。

{{< copyable "" >}}

```sql
select * from ((select table_schema, table_name, column_name, collation_name from information_schema.columns where character_set_name is not null) union all (select table_schema, table_name, null, table_collation from information_schema.tables)) x where table_schema not in ('performance_schema', 'mysql', 'information_schema') and collation_name not in ('utf8_bin', 'utf8mb4_bin', 'ascii_bin', 'latin1_bin', 'binary', 'utf8_general_ci', 'utf8mb4_general_ci');
```

結果は次のとおりです。

```output
Empty set (0.04 sec)
```

TiDB が文字セットまたは照合順序をサポートしていない場合は、サポートされているタイプに変換することを検討してください。詳細については、 [<a href="https://docs.pingcap.com/tidb/stable/character-set-and-collation">文字セットと照合順序</a>](https://docs.pingcap.com/tidb/stable/character-set-and-collation)を参照してください。

### オプション 1: Dumplingを使用してソース データ ファイルを準備する {#option-1-prepare-source-data-files-using-dumpling}

次のデータ エクスポート タスクを実行するには、EC2 を準備する必要があります。追加料金を避けるために、 Auroraと S3 を同じネットワーク上で実行することをお勧めします。

1.  EC2 にDumplingをインストールします。

    {{< copyable "" >}}

    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    source ~/.bash_profile
    tiup install dumpling
    ```

    上記のコマンドでは、 `~/.bash_profile`プロファイル ファイルのパスに変更する必要があります。

2.  S3 を書き込むための書き込み権限をDumplingに付与します。

    > **ノート：**
    >
    > IAMロールを EC2 に割り当てている場合は、アクセス キーとセキュリティ キーの構成をスキップして、この EC2 上でDumplingを直接実行できます。

    環境内の AWS アカウントのアクセス キーとセキュリティ キーを使用して、書き込み権限を付与できます。データを準備するための特定のキー ペアを作成し、準備が完了したらすぐにアクセス キーを取り消します。

    {{< copyable "" >}}

    ```bash
    export AWS_ACCESS_KEY_ID=AccessKeyID
    export AWS_SECRET_ACCESS_KEY=SecretKey
    ```

3.  ソース データベースを S3 にバックアップします。

    Dumpling を使用して Amazon Auroraからデータをエクスポートします。環境に応じて山括弧 (&gt;) 内の内容を置き換えて、次のコマンドを実行します。データのエクスポート時にフィルター ルールを使用する場合は、 [<a href="/table-filter.md#syntax">テーブルフィルター</a>](/table-filter.md#syntax)を参照してください。

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

4.  クラスターの [**インポート]**ページで、右上隅にある**[データのインポート]**をクリックし、 **[S3 から]**を選択して、データ形式として**SQL ファイル**を選択します。

### オプション 2: Amazon Auroraスナップショットを使用してソース データ ファイルを準備する {#option-2-prepare-source-data-files-using-amazon-aurora-snapshots}

#### データベースのスキーマをバックアップし、 TiDB Cloud上で復元します {#back-up-the-schema-of-the-database-and-restore-on-tidb-cloud}

Auroraからデータを移行するには、データベースのスキーマをバックアップする必要があります。

1.  MySQL クライアントをインストールします。

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

4.  クラスターの [**インポート]**ページで、右上隅の**[データのインポート]**をクリックし、 **[From S3]**を選択して、データ形式として**[Aurora Snapshot]**を選択します。

#### スナップショットを取得して S3 にエクスポートする {#take-a-snapshot-and-export-it-to-s3}

1.  Amazon RDS コンソールから、 **[スナップショット]**を選択し、 **[スナップショットの作成]**をクリックして手動スナップショットを作成します。

2.  **[スナップショット名]**の下に空白を入力します。 **「スナップショットを撮る」**をクリックします。スナップショットの作成が完了すると、スナップショットがスナップショット テーブルの下に表示されます。

3.  作成したスナップショットを選択し、 **「アクション」を**クリックします。ドロップダウン ボックスで、 **[Amazon S3 にエクスポート] を**クリックします。

4.  **[エクスポート識別子]**の下に空白を入力します。

5.  エクスポートするデータの量を選択します。このガイドでは、 **「すべて」**が選択されています。また、「部分」を選択して、識別子を使用してデータベースのどの部分をエクスポートする必要があるかを決定することもできます。

6.  スナップショットを保存する S3 バケットを選択します。セキュリティ上の懸念がある場合は、新しいバケットを作成してデータを保存できます。 TiDB クラスターと同じリージョンのバケットを使用することをお勧めします。リージョン間でデータをダウンロードすると、追加のネットワーク コストが発生する可能性があります。

7.  S3 バケットへの書き込みアクセスを許可するには、適切なIAMロールを選択します。このロールは、後でスナップショットをTiDB Cloudにインポートするときに使用するため、メモしておきます。

8.  適切な AWS KMS キーを選択し、 IAMロールが KMS キー ユーザーにすでに追加されていることを確認してください。ロールを追加するには、KSM サービスを選択し、キーを選択して、 **[追加]**をクリックします。

9.  **[Amazon S3 をエクスポート] を**クリックします。タスクテーブルで進行状況を確認できます。

10. タスク テーブルから、宛先バケット (たとえば、 `s3://snapshot-bucket/snapshot-samples-1` ) を記録します。

## Amazon S3 へのアクセスを設定する方法を学ぶ {#learn-how-to-configure-access-to-amazon-s3}

TiDB Cloudクラスターと S3 バケットは別の AWS アカウントにあります。 TiDB Cloudクラスターが S3 バケット内のソース データ ファイルにアクセスできるようにするには、Amazon S3 へのクロスアカウント アクセスを設定する必要があります。詳細については、 [<a href="/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access">Amazon S3 アクセスを構成する</a>](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

完了すると、クロスアカウントのポリシーとロールが作成されます。その後、 TiDB Cloudのデータ インポート タスク パネルで構成を続行できます。

> **ノート：**
>
> データの一貫性を確保するために、 TiDB Cloud空のテーブルにのみ CSV ファイルをインポートできます。すでにデータが含まれている既存のテーブルにデータをインポートするには、このドキュメントに従ってTiDB Cloudを使用して一時的な空のテーブルにデータをインポートし、その後`INSERT SELECT`ステートメントを使用してデータをターゲットの既存のテーブルにコピーします。

## フィルタールールの設定方法を学ぶ {#learn-how-to-set-up-filter-rules}

資料[<a href="/table-filter.md#syntax">テーブルフィルター</a>](/table-filter.md#syntax)をご参照ください。

## 不完全なデータをクリーンアップする方法を学ぶ {#learn-how-to-clean-up-incomplete-data}

要件を再度確認できます。すべての問題が解決したら、不完全なデータベースを削除し、インポート プロセスを再開できます。
