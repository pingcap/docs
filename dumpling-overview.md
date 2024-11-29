---
title: Dumpling Overview
summary: Dumplingツールを使用して TiDB からデータをエクスポートします。
---

# Dumpling を使用してデータをエクスポートする {#use-dumpling-to-export-data}

このドキュメントでは、データ エクスポート ツール - [Dumpling](https://github.com/pingcap/tidb/tree/release-8.1/dumpling)を紹介します。Dumplingは、 TiDB/MySQL に保存されているデータを SQL または CSV データ ファイルとしてエクスポートし、論理的な完全バックアップやエクスポートに使用できます。Dumplingは、 Amazon S3 へのデータのエクスポートもサポートしています。

<CustomContent platform="tidb">

[TiUP](/tiup/tiup-overview.md)使用して`tiup install dumpling`実行するとDumpling を取得できます。その後、 `tiup dumpling ...`使用してDumpling を実行できます。

Dumplingインストール パッケージはTiDB Toolkitに含まれています。TiDB TiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロード](/download-ecosystem-tools.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

次のコマンドを使用してDumpling をインストールできます。

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
source ~/.bash_profile
tiup install dumpling
```

上記のコマンドでは、 `~/.bash_profile`プロファイル ファイルのパスに変更する必要があります。

</CustomContent>

Dumplingの詳細な使用方法については、 `--help`オプションを使用するか、 [Dumplingのオプションリスト](#option-list-of-dumpling)を参照してください。

Dumpling を使用する場合は、実行中のクラスターでエクスポート コマンドを実行する必要があります。

<CustomContent platform="tidb">

TiDB には、必要に応じて選択できるその他のツールも用意されています。

-   SST ファイル (キーと値のペア) のバックアップ、またはレイテンシーの影響を受けない増分データのバックアップについては、 [BR](/br/backup-and-restore-overview.md)を参照してください。
-   増分データのリアルタイムバックアップについては、 [ティCDC](/ticdc/ticdc-overview.md)を参照してください。
-   エクスポートされたすべてのデータは、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用して TiDB に再度インポートできます。

</CustomContent>

> **注記：**
>
> PingCAP は以前、TiDB 固有の機能強化を加えた[mydumper プロジェクト](https://github.com/maxbube/mydumper)のフォークを維持していました。v7.5.0 以降、 [マイダンパー](https://docs.pingcap.com/tidb/v4.0/mydumper-overview)非推奨となり、その機能のほとんどが[Dumpling](/dumpling-overview.md)に置き換えられました。mydumper ではなくDumpling を使用することを強くお勧めします。

Dumplingには次のような利点があります。

-   SQL や CSV を含む複数の形式でのデータのエクスポートをサポートします。
-   データのフィルタリングを容易にする[テーブルフィルター](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md)機能をサポートします。
-   Amazon S3 クラウドstorageへのデータのエクスポートをサポートします。
-   TiDB に対してさらなる最適化が行われました:
    -   単一のTiDB SQLステートメントのメモリ制限の構成をサポートします。
    -   Dumpling がTiDB クラスターの PD アドレスと[`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)テーブルにアクセスできる場合、 Dumpling はTiDB v4.0.0 以降のバージョンで[GC](/garbage-collection-overview.md)セーフ ポイント時間をブロック GC に自動的に調整することをサポートします。
    -   TiDB の隠し列`_tidb_rowid`を使用して、単一のテーブルからの同時データ エクスポートのパフォーマンスを最適化します。
    -   TiDB の場合、データ バックアップの時点を指定するために値[`tidb_snapshot`](/read-historical-data.md#how-tidb-reads-data-from-history-versions)を設定できます。これにより、一貫性を確保するために`FLUSH TABLES WITH READ LOCK`使用する代わりに、バックアップの一貫性が確保されます。

> **注記：**
>
> 次のシナリオでは、 Dumpling はPD に接続できません。
>
> -   TiDB クラスターは Kubernetes 上で実行されています ( Dumpling自体が Kubernetes 環境内で実行されている場合を除く)。
> -   TiDB クラスターはTiDB Cloud上で実行されています。
>
> このような場合、エクスポートの失敗を回避するために手動で[TiDB GC時間を調整する](#manually-set-the-tidb-gc-time)実行する必要があります。

## TiDBまたはMySQLからデータをエクスポートする {#export-data-from-tidb-or-mysql}

### 必要な権限 {#required-privileges}

-   プロセス: クラスター情報を照会して PD アドレスを取得し、PD 経由で GC を制御するために必要です。
-   SELECT: テーブルをエクスポートするときに必要です。
-   RELOAD: `consistency flush`使用する場合に必須です。この権限をサポートするのは TiDB のみであることに注意してください。アップストリームが RDS データベースまたはマネージド サービスである場合は、この権限を無視できます。
-   LOCK TABLES: `consistency lock`使用する場合に必要です。この権限は、エクスポートするすべてのデータベースとテーブルに付与する必要があります。
-   レプリケーション クライアント: データのスナップショットを記録するためにメタデータをエクスポートするときに必要です。この権限はオプションであり、メタデータをエクスポートする必要がない場合は無視できます。

### SQLファイルへのエクスポート {#export-to-sql-files}

このドキュメントでは、127.0.0.1:4000 ホストに TiDB インスタンスがあり、この TiDB インスタンスにパスワードのない root ユーザーが存在することを前提としています。

Dumpling はデフォルトでデータを SQL ファイルにエクスポートします。1 `--filetype sql`を追加してデータを SQL ファイルにエクスポートすることもできます。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 --filetype sql -t 8 -o /tmp/test -r 200000 -F 256MiB
```

上記のコマンドでは:

-   `-h` 、 `-P` 、 `-u`オプションはそれぞれ、アドレス、ポート、ユーザーを意味します。認証にパスワードが必要な場合は、 `-p $YOUR_SECRET_PASSWORD`使用してDumplingにパスワードを渡すことができます。
-   `-o` (または`--output` ) オプションは、storageのエクスポート ディレクトリを指定します。これは、絶対ローカル ファイル パスまたは[外部storageURI](/external-storage-uri.md)サポートします。
-   `-t`オプションは、エクスポートのスレッド数を指定します。スレッド数を増やすと、 Dumplingの同時実行性とエクスポート速度が向上しますが、データベースのメモリ消費も増加します。したがって、数値を大きくしすぎることはお勧めしません。通常は 64 未満です。
-   `-r`オプションは、テーブル内同時実行を有効にしてエクスポートを高速化します。デフォルト値は`0`で、無効を意味します。0 より大きい値は有効であることを意味し、値は`INT`タイプです。ソース データベースが TiDB の場合、0 より大きい値`-r`は、TiDB 領域情報が分割に使用され、メモリ使用量が削減されることを示します。特定の`-r`値は分割アルゴリズムに影響しません。ソース データベースが MySQL で、主キーが`INT`タイプの場合、 `-r`指定してもテーブル内同時実行を有効にできます。
-   `-F`オプションは、単一ファイルの最大サイズを指定するために使用されます (ここでの単位は`MiB`ですが、 `5GiB`や`8KB`などの入力も許容されます)。TiDB TiDB Lightning を使用してこのファイルを TiDB インスタンスにロードする予定の場合は、値を 256 MiB 以下に維持することをお勧めします。

> **注記：**
>
> エクスポートされた単一のテーブルのサイズが 10 GB を超える場合は、オプション`-r`および`-F`**を使用することを強くお勧めします**。

#### storageサービスのURI形式 {#uri-formats-of-the-storage-services}

このセクションでは、Amazon S3、GCS、Azure Blob Storage などのstorageサービスの URI 形式について説明します。URI 形式は次のとおりです。

```shell
[scheme]://[host]/[path]?[parameters]
```

詳細については[外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

### CSVファイルにエクスポート {#export-to-csv-files}

`--filetype csv`引数を追加することで、データを CSV ファイルにエクスポートできます。

データを CSV ファイルにエクスポートする場合、 `--sql <SQL>`使用して SQL ステートメントでレコードをフィルター処理できます。たとえば、次のコマンドを使用して、 `test.sbtest1`のうち`id < 100`に一致するすべてのレコードをエクスポートできます。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test --filetype csv --sql 'select * from `test`.`sbtest1` where id < 100' -F 100MiB --output-filename-template 'test.sbtest1.{{.Index}}'
```

上記のコマンドでは:

-   `--sql`オプションは、CSV ファイルへのエクスポートにのみ使用できます。上記のコマンドは、エクスポートするすべてのテーブルに対して`SELECT * FROM <table-name> WHERE id <100`ステートメントを実行します。テーブルに指定されたフィールドがない場合、エクスポートは失敗します。

<CustomContent platform="tidb">

-   `--sql`オプションを使用すると、 Dumpling はエクスポートされたテーブルとスキーマの情報を取得できません。 `--output-filename-template`オプションを使用して CSV ファイルのファイル名形式を指定できます。これにより、後で[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してデータ ファイルをインポートしやすくなります。 たとえば、 `--output-filename-template='test.sbtest1.{{.Index}}'`エクスポートされた CSV ファイルの名前が`test.sbtest1.000000000`または`test.sbtest1.000000001`になるように指定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `--sql`オプションを使用すると、 Dumpling はエクスポートされたテーブルとスキーマの情報を取得できません。 `--output-filename-template`オプションを使用して、CSV ファイルのファイル名の形式を指定できます。 たとえば、 `--output-filename-template='test.sbtest1.{{.Index}}'` 、エクスポートされた CSV ファイルの名前が`test.sbtest1.000000000`または`test.sbtest1.000000001`になるように指定します。

</CustomContent>

-   `--csv-separator`や`--csv-delimiter`などのオプションを使用して、CSV ファイル形式を設定できます。詳細については、 [Dumplingオプションリスト](#option-list-of-dumpling)を参照してください。

> **注記：**
>
> Dumplingでは*文字列*と*キーワードは*区別されません。インポートされたデータがブール型の場合、 `true`の値は`1`に変換され、 `false`の値は`0`に変換されます。

### エクスポートしたデータファイルを圧縮する {#compress-the-exported-data-files}

`--compress <format>`オプションを使用すると、 Dumplingによってエクスポートされた CSV および SQL データとテーブル構造ファイルを圧縮できます。このパラメータは、 `gzip` 、 `snappy` 、および`zstd`の圧縮アルゴリズムをサポートしています。デフォルトでは、圧縮は無効になっています。

-   このオプションは、個々のデータとテーブル構造ファイルのみを圧縮します。フォルダー全体を圧縮して単一の圧縮パッケージを生成することはできません。
-   このオプションを使用するとディスク容量を節約できますが、エクスポート速度が低下し、CPU 消費量が増加します。エクスポート速度が重要なシナリオでは、このオプションを慎重に使用してください。
-   TiDB Lightning v6.5.0 以降のバージョンでは、追加の構成なしで、 Dumplingによってエクスポートされた圧縮ファイルをデータ ソースとして使用できます。

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。Snappy 圧縮の他のバリエーションはサポートされていません。

### エクスポートされたファイルの形式 {#format-of-exported-files}

-   `metadata` : エクスポートされたファイルの開始時刻とマスターバイナリログの位置。

    ```shell
    cat metadata
    ```

    ```shell
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ```

-   `{schema}-schema-create.sql` : スキーマの作成に使用されたSQLファイル

    ```shell
    cat test-schema-create.sql
    ```

    ```shell
    CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
    ```

-   `{schema}.{table}-schema.sql` : テーブルの作成に使用されたSQLファイル

    ```shell
    cat test.t1-schema.sql
    ```

    ```shell
    CREATE TABLE `t1` (
      `id` int(11) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
    ```

-   `{schema}.{table}.{0001}.{sql|csv}` : 日付ソースファイル

    ```shell
    cat test.t1.0.sql
    ```

    ```shell
    /*!40101 SET NAMES binary*/;
    INSERT INTO `t1` VALUES
    (1);
    ```

-   `*-schema-view.sql` : その他`*-schema-post.sql` `*-schema-trigger.sql`ファイル

### Amazon S3クラウドstorageにデータをエクスポートする {#export-data-to-amazon-s3-cloud-storage}

バージョン 4.0.8 以降、 Dumpling はクラウド ストレージへのデータのエクスポートをサポートしています。データを Amazon S3 にバックアップする必要がある場合は、 `-o`パラメータで Amazon S3storageパスを指定する必要があります。

指定されたリージョンに Amazon S3 バケットを作成する必要があります ( [Amazon ドキュメント - S3 バケットを作成するには](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)を参照)。バケット内にフォルダも作成する必要がある場合は、 [Amazon ドキュメント - フォルダーの作成](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html)を参照してください。

Amazon S3 バックエンドstorageにアクセスする権限を持つアカウントの`SecretKey`と`AccessKey`環境変数としてDumplingノードに渡します。

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

Dumpling は`~/.aws/credentials`からの資格情報ファイルの読み取りもサポートしています。URI パラメータの説明の詳細については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -r 200000 -o "s3://${Bucket}/${Folder}"
```

### エクスポートしたデータをフィルタリングする {#filter-the-exported-data}

#### <code>--where</code>オプションを使用してデータをフィルタリングします {#use-the-code-where-code-option-to-filter-data}

デフォルトでは、 Dumpling はシステム データベース ( `mysql` 、 `sys` 、 `INFORMATION_SCHEMA` 、 `PERFORMANCE_SCHEMA` 、 `METRICS_SCHEMA` 、および`INSPECTION_SCHEMA`を含む) を除くすべてのデータベースをエクスポートします。 `--where <SQL where expression>`使用して、エクスポートするレコードを選択できます。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test --where "id < 100"
```

上記のコマンドは、各テーブルから`id < 100`に一致するデータをエクスポートします。 `--where`パラメータを`--sql`と一緒に使用できないことに注意してください。

#### <code>--filter</code>オプションを使用してデータをフィルタリングします {#use-the-code-filter-code-option-to-filter-data}

Dumpling は、 `--filter`オプションでテーブル フィルターを指定することにより、特定のデータベースまたはテーブルをフィルターできます。テーブル フィルターの構文は`.gitignore`の構文と似ています。詳細については、 [テーブルフィルター](/table-filter.md)参照してください。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test -r 200000 --filter "employees.*" --filter "*.WorkOrder"
```

上記のコマンドは、 `employees`データベース内のすべてのテーブルと、すべてのデータベース内の`WorkOrder`テーブルをエクスポートします。

#### <code>-B</code>または<code>-T</code>オプションを使用してデータをフィルタリングします {#use-the-code-b-code-or-code-t-code-option-to-filter-data}

Dumpling、 `-B`オプションを使用して特定のデータベースをエクスポートしたり、 `-T`オプションを使用して特定のテーブルをエクスポートすることもできます。

> **注記：**
>
> -   オプション`--filter`とオプション`-T`を同時に使用することはできません。
> -   `-T`オプションは、 `database-name.table-name`ような完全な形式の入力のみを受け入れることができ、テーブル名のみの入力は受け入れられません。例: Dumpling は`-T WorkOrder`認識できません。

例:

-   `-B employees` `employees`データベースをエクスポートします。
-   `-T employees.WorkOrder` `employees.WorkOrder`テーブルをエクスポートします。

### 同時実行による輸出効率の向上 {#improve-export-efficiency-through-concurrency}

エクスポートされたファイルは、デフォルトで`./export-<current local time>`ディレクトリに保存されます。よく使用されるオプションは次のとおりです。

-   `-t`オプションは、エクスポートのスレッド数を指定します。スレッド数を増やすと、 Dumplingの同時実行性とエクスポート速度が向上しますが、データベースのメモリ消費も増加します。したがって、数値を大きくしすぎることはお勧めしません。
-   `-r`オプションは、テーブル内同時実行を有効にしてエクスポートを高速化します。デフォルト値は`0`で、無効を意味します。0 より大きい値は有効であることを意味し、値は`INT`タイプです。ソース データベースが TiDB の場合、0 より大きい値`-r`は、TiDB 領域情報が分割に使用され、メモリ使用量が削減されることを示します。特定の`-r`値は分割アルゴリズムに影響しません。ソース データベースが MySQL で、主キーが`INT`タイプの場合、 `-r`指定してもテーブル内同時実行を有効にできます。
-   `--compress <format>`オプションは、ダンプの圧縮形式を指定します。 `gzip` 、 `snappy` 、および`zstd`の圧縮アルゴリズムをサポートしています。 このオプションを使用すると、storageがボトルネックになっている場合やstorage容量が問題になっている場合に、データのダンプを高速化できます。 欠点は、CPU 使用率が増加することです。 各ファイルは個別に圧縮されます。

上記のオプションを指定すると、 Dumpling はデータのエクスポート速度を速めることができます。

### Dumplingのデータ一貫性オプションを調整する {#adjust-dumpling-s-data-consistency-options}

> **注記：**
>
> データ一貫性オプションのデフォルト値は`auto`です。ほとんどのシナリオでは、 Dumplingのデフォルトのデータ一貫性オプションを調整する必要はありません。

Dumpling は、 `--consistency <consistency level>`オプションを使用して、「一貫性の保証」のためにデータをエクスポートする方法を制御します。一貫性のためにスナップショットを使用する場合は、 `--snapshot`オプションを使用して、バックアップするタイムスタンプを指定できます。次の一貫性レベルも使用できます。

-   `flush` : レプリカ データベースの DML および DDL 操作を一時的に中断し、バックアップ接続のグローバルな一貫性を確保し、binlog位置 (POS) 情報を記録するために[`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock)使用します。すべてのバックアップ接続がトランザクションを開始した後、ロックは解除されます。オフピーク時間または MySQL レプリカ データベースで完全バックアップを実行することをお勧めします。
-   `snapshot` : 指定されたタイムスタンプの一貫したスナップショットを取得してエクスポートします。
-   `lock` : エクスポートするすべてのテーブルに読み取りロックを追加します。
-   `none` : 一貫性は保証されません。
-   `auto` : MySQL の場合は`flush` 、TiDB の場合は`snapshot`使用します。

すべてが完了したら、エクスポートされたファイルを`/tmp/test`で確認できます。

```shell
ls -lh /tmp/test | awk '{print $5 "\t" $9}'
```

    140B  metadata
    66B   test-schema-create.sql
    300B  test.sbtest1-schema.sql
    190K  test.sbtest1.0.sql
    300B  test.sbtest2-schema.sql
    190K  test.sbtest2.0.sql
    300B  test.sbtest3-schema.sql
    190K  test.sbtest3.0.sql

### TiDBの履歴データスナップショットをエクスポートする {#export-historical-data-snapshots-of-tidb}

Dumpling は、 `--snapshot`オプションを指定して特定の[スナップショット](/read-historical-data.md#how-tidb-reads-data-from-history-versions)のデータをエクスポートできます。

`--snapshot`オプションは、TSO ( `SHOW MASTER STATUS`コマンドによって出力される`Position`フィールド) または`datetime`データ型の有効時間 ( `YYYY-MM-DD hh:mm:ss`の形式) に設定できます。次に例を示します。

```shell
tiup dumpling --snapshot 417773951312461825
tiup dumpling --snapshot "2020-07-02 17:12:45"
```

TSO が`417773951312461825` 、時間が`2020-07-02 17:12:45`ときの TiDB 履歴データ スナップショットがエクスポートされます。

### 大きなテーブルをエクスポートする際のメモリ使用量を制御する {#control-the-memory-usage-of-exporting-large-tables}

Dumpling がTiDB から大きな単一テーブルをエクスポートする場合、エクスポートされたデータのサイズが大きすぎるためにメモリ不足 (OOM) が発生し、接続が中断され、エクスポートが失敗する可能性があります。次のパラメータを使用して、TiDB のメモリ使用量を削減できます。

-   `-r`に設定すると、エクスポートするデータがチャンクに分割されます。これにより、TiDB のデータ スキャンのメモリオーバーヘッドが削減され、同時テーブル データ ダンプが可能になり、エクスポートの効率が向上します。アップストリーム データベースが TiDB v3.0 以降のバージョンの場合、0 より大きい`-r`値は、分割に TiDB リージョン情報が使用され、特定の`-r`値は分割アルゴリズムに影響しないことを示します。
-   `--tidb-mem-quota-query`の値を`8589934592` (8 GB) 以下に減らします。5 `--tidb-mem-quota-query` TiDB 内の単一のクエリ ステートメントのメモリ使用量を制御します。
-   `--params "tidb_distsql_scan_concurrency=5"`パラメータを調整します。3 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) TiDB でのスキャン操作の同時実行を制御するセッション変数です。

### TiDB GC時間を手動で設定する {#manually-set-the-tidb-gc-time}

TiDB (1 TB 未満) からデータをエクスポートする場合、TiDB バージョンが v4.0.0 以降で、 Dumpling がTiDB クラスターの PD アドレスと[`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)テーブルにアクセスできる場合、 Dumpling はGC セーフ ポイントを自動的に調整し、元のクラスターに影響を与えずに GC をブロックします。

ただし、次のいずれかのシナリオでは、 Dumpling はGC 時間を自動的に調整できません。

-   データサイズが非常に大きい（1TB以上）。
-   たとえば、TiDB クラスターがTiDB Cloud上にある場合や、 Dumplingから分離された Kubernetes 上にある場合、 Dumpling はPD に直接接続できません。

このようなシナリオでは、エクスポート プロセス中の GC によるエクスポートの失敗を回避するために、事前に GC 時間を手動で延長する必要があります。

GC 時間を手動で調整するには、次の SQL ステートメントを使用します。

```sql
SET GLOBAL tidb_gc_life_time = '720h';
```

Dumpling が終了したら、エクスポートが成功したかどうかに関係なく、GC 時間を元の値に戻す必要があります (デフォルト値は`10m`です)。

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

## Dumplingのオプションリスト {#option-list-of-dumpling}

| オプション                        | 使用法                                                                                                                                                                                                                                                                                                                                                                                             | デフォルト値                                                                                                                                                               |             |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `-V`または`--version`           | Dumplingバージョンを出力して直接終了する                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                      |             |
| `-B`または`--database`          | 指定されたデータベースをエクスポートする                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                      |             |
| `-T`または`--tables-list`       | 指定されたテーブルをエクスポートする                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                      |             |
| `-f`または`--filter`            | フィルタ パターンに一致するテーブルをエクスポートします。フィルタ構文については、 [テーブルフィルター](/table-filter.md)参照してください。                                                                                                                                                                                                                                                                                                                | `[\*.\*,!/^(mysql&#124;sys&#124;INFORMATION_SCHEMA&#124;PERFORMANCE_SCHEMA&#124;METRICS_SCHEMA&#124;INSPECTION_SCHEMA)$/.\*]` (システム スキーマを除くすべてのデータベースまたはテーブルをエクスポート) |             |
| `--case-sensitive`           | テーブルフィルタが大文字と小文字を区別するかどうか                                                                                                                                                                                                                                                                                                                                                                       | 偽（大文字と小文字を区別しない）                                                                                                                                                     |             |
| `-h`または`--host`              | 接続されたデータベースホストのIPアドレス                                                                                                                                                                                                                                                                                                                                                                           | 「127.0.0.1」                                                                                                                                                          |             |
| `-t`または`--threads`           | 同時バックアップスレッドの数                                                                                                                                                                                                                                                                                                                                                                                  | 4                                                                                                                                                                    |             |
| `-r`または`--rows`              | テーブル内同時実行を有効にして、エクスポートを高速化します。デフォルト値は`0`で、無効を意味します。0 より大きい値は有効であることを意味し、値は`INT`タイプです。ソース データベースが TiDB の場合、0 より大きい値`-r`は、分割に TiDB リージョン情報が使用され、メモリ使用量が削減されることを示します。特定の`-r`値は分割アルゴリズムに影響しません。ソース データベースが MySQL で、主キーが`INT`タイプの場合、 `-r`指定してもテーブル内同時実行を有効にできます。                                                                                                                                     |                                                                                                                                                                      |             |
| `-L`または`--logfile`           | ログ出力アドレス。空の場合、ログはコンソールに出力されます。                                                                                                                                                                                                                                                                                                                                                                  | 「」                                                                                                                                                                   |             |
| `--loglevel`                 | ログレベル {debug、info、warn、error、dpanic、 panic、fatal}                                                                                                                                                                                                                                                                                                                                               | &quot;情報&quot;                                                                                                                                                       |             |
| `--logfmt`                   | ログ出力形式 {text,json}                                                                                                                                                                                                                                                                                                                                                                              | &quot;文章&quot;                                                                                                                                                       |             |
| `-d`または`--no-data`           | データをエクスポートしない (スキーマのみがエクスポートされるシナリオに適しています)                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                      |             |
| `--no-header`                | ヘッダーを生成せずにテーブルのCSVファイルをエクスポートする                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                      |             |
| `-W`または`--no-views`          | ビューをエクスポートしない                                                                                                                                                                                                                                                                                                                                                                                   | 真実                                                                                                                                                                   |             |
| `-m`または`--no-schemas`        | データのみをエクスポートしてスキーマをエクスポートしないでください                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                      |             |
| `-s`または`--statement-size`    | `INSERT`ステートメントのサイズを制御します。単位はバイトです。                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                      |             |
| `-F`または`--filesize`          | 分割されたテーブルのファイルサイズ。 `128B` 、 `64KiB` 、 `32MiB` 、 `1.5GiB`などの単位を指定する必要があります。                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                                      |             |
| `--filetype`                 | エクスポートされたファイルの種類 (csv/sql)                                                                                                                                                                                                                                                                                                                                                                      | 「SQL」                                                                                                                                                                |             |
| `-o`または`--output`            | データをエクスポートするには、絶対ローカル ファイル パスまたは[外部storageURI](/external-storage-uri.md)指定します。                                                                                                                                                                                                                                                                                                                  | 「./export-${time}」                                                                                                                                                   |             |
| `-S`または`--sql`               | 指定された SQL ステートメントに従ってデータをエクスポートします。このコマンドは同時エクスポートをサポートしていません。                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                      |             |
| `--consistency`              | フラッシュ: ダンプの前にFTWRLを使用する<br/>スナップショット: TSO の特定のスナップショットの TiDB データをダンプします<br/>ロック: ダンプするすべてのテーブルに対して`lock tables read`を実行します<br/>none: ロックを追加せずにダンプします。一貫性は保証されません。<br/>自動: MySQL の場合は --consistency flush を使用し、TiDB の場合は --consistency snapshot を使用します。                                                                                                                                          | 「自動」                                                                                                                                                                 |             |
| `--snapshot`                 | スナップショットTSO; `consistency=snapshot`場合にのみ有効                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                                      |             |
| `--where`                    | `where`条件でテーブルバックアップの範囲を指定します                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                      |             |
| `-p`または`--password`          | 接続されたデータベースホストのパスワード                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                      |             |
| `-P`または`--port`              | 接続されたデータベースホストのポート                                                                                                                                                                                                                                                                                                                                                                              | 4000                                                                                                                                                                 |             |
| `-u`または`--user`              | 接続されたデータベースホストのユーザー名                                                                                                                                                                                                                                                                                                                                                                            | &quot;根&quot;                                                                                                                                                        |             |
| `--dump-empty-database`      | 空のデータベースの`CREATE DATABASE`ステートメントをエクスポートします                                                                                                                                                                                                                                                                                                                                                     | 真実                                                                                                                                                                   |             |
| `--ca`                       | TLS接続用の証明機関ファイルのアドレス                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                      |             |
| `--cert`                     | TLS接続用のクライアント証明書ファイルのアドレス                                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                      |             |
| `--key`                      | TLS接続用のクライアント秘密鍵ファイルのアドレス                                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                      |             |
| `--csv-delimiter`            | CSV ファイル内の文字型変数の区切り文字                                                                                                                                                                                                                                                                                                                                                                           | &#39;&quot;&#39;                                                                                                                                                     |             |
| `--csv-separator`            | CSV ファイル内の各値の区切り文字。デフォルトの &#39;,&#39; の使用は推奨されません。&#39;|+|&#39; またはその他の一般的でない文字の組み合わせを使用することをお勧めします。                                                                                                                                                                                                                                                                                            | &#39;,&#39;                                                                                                                                                          | &#39;,&#39; |
| `--csv-null-value`           | CSV ファイルにおける null 値の表現                                                                                                                                                                                                                                                                                                                                                                          | 「\N」                                                                                                                                                                 |             |
| `--csv-line-terminator`      | CSV ファイルの行末のターミネータ。データを CSV ファイルにエクスポートするときに、このオプションを使用して目的のターミネータを指定できます。このオプションは、&quot;\r\n&quot; と &quot;\n&quot; をサポートします。デフォルト値は &quot;\r\n&quot; で、以前のバージョンと一致しています。bash の引用符には異なるエスケープ規則があるため、ターミネータとして LF (改行) を指定する場合は、 `--csv-line-terminator $'\n'`のような構文を使用できます。                                                                                                                    | &quot;\r\n&quot;                                                                                                                                                     |             |
| `--csv-output-dialect`       | ソース データを、データベースに必要な特定の形式で CSV ファイルにエクスポートできることを示します。オプションの値は`""` 、 `"snowflake"` 、 `"redshift"` 、または`"bigquery"`です。既定値は`""`で、ソース データを UTF-8 に従ってエンコードしてエクスポートすることを意味します。オプションを`"snowflake"`または`"redshift"`に設定すると、ソース データのバイナリ データ型は 16 進数に変換されますが、 `0x`プレフィックスは削除されます。たとえば、 `0x61` `61`として表されます。オプションを`"bigquery"`に設定すると、バイナリ データ型は base64 を使用してエンコードされます。場合によっては、バイナリ文字列に文字化けした文字が含まれることがあります。 | `""`                                                                                                                                                                 |             |
| `--escape-backslash`         | エクスポートファイル内の特殊文字をエスケープするには、バックスラッシュ（ `\` ）を使用します。                                                                                                                                                                                                                                                                                                                                               | 真実                                                                                                                                                                   |             |
| `--output-filename-template` | [Golang テンプレート](https://golang.org/pkg/text/template/#hdr-Arguments)の形式で表されたファイル名テンプレート<br/>`{{.DB}}` `{{.Table}}`引数`{{.Index}}`サポートする<br/>3つの引数は、データベース名、テーブル名、データファイルのチャンクIDを表します。                                                                                                                                                                                                            | `{{.DB}}.{{.Table}}.{{.Index}}`                                                                                                                                      |             |
| `--status-addr`              | Dumpling のサービス アドレス (Prometheus がメトリクスを取得して pprof デバッグを行うためのアドレスを含む)                                                                                                                                                                                                                                                                                                                            | 「:8281」                                                                                                                                                              |             |
| `--tidb-mem-quota-query`     | Dumplingコマンドの 1 行でエクスポートする SQL ステートメントのメモリ制限。単位はバイトです。v4.0.10 以降のバージョンでは、このパラメータを設定しないと、TiDB はデフォルトで`mem-quota-query`構成項目の値をメモリ制限値として使用します。v4.0.10 より前のバージョンでは、パラメータ値はデフォルトで 32 GB になります。                                                                                                                                                                                                       | 34359738368                                                                                                                                                          |             |
| `--params`                   | エクスポートするデータベースの接続のセッション変数を指定します。必要な形式は`"character_set_client=latin1,character_set_connection=latin1"`です。                                                                                                                                                                                                                                                                                        |                                                                                                                                                                      |             |
| `-c`または`--compress`          | Dumplingによってエクスポートされた CSV および SQL データとテーブル構造ファイルを圧縮します。次の`zstd`アルゴリズムをサポートしています: `gzip` 、および`snappy` 。                                                                                                                                                                                                                                                                                          | 「」                                                                                                                                                                   |             |
