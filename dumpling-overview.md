---
title: Dumpling Overview
summary: TiDBからデータをエクスポートするには、Dumplingツールを使用してください。
---

# Dumplingを使用してデータをエクスポートする {#use-dumpling-to-export-data}

このドキュメントでは、データエクスポートツール「 [Dumpling](https://github.com/pingcap/tidb/tree/release-8.5/dumpling)について説明します。Dumplingは、TiDB/MySQLに保存されているデータをSQLまたはCSVデータファイルとしてエクスポートし、論理的なフルバックアップやエクスポートに使用できます。また、 DumplingはAmazon S3へのデータエクスポートもサポートしています。

<CustomContent platform="tidb">

[TiUP](/tiup/tiup-overview.md)を使用してDumplingを取得するには、 `tiup install dumpling`を実行します。その後、 `tiup dumpling ...`を使用してDumplingを実行できます。

Dumplingインストール パッケージは、 TiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロード](/download-ecosystem-tools.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

Dumplingは以下のコマンドを使用してインストールできます。

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
source ~/.bash_profile
tiup install dumpling
```

上記のコマンドでは、 `~/.bash_profile`プロファイルファイルのパスに変更する必要があります。

</CustomContent>

Dumplingの詳しい使用方法については、 `--help`オプションを使用するか、 [Dumplingのオプション一覧](#option-list-of-dumpling)を参照してください。

Dumplingを使用する場合は、実行中のクラスタ上でexportコマンドを実行する必要があります。

<CustomContent platform="tidb">

TiDBは、必要に応じて選択して使用できるその他のツールも提供しています。

-   SST ファイル (キーと値のペア) のバックアップ、またはレイテンシーに影響されない増分データのバックアップについては、 [BR](/br/backup-and-restore-overview.md)を参照してください。
-   増分データのリアルタイムバックアップについては、 [TiCDC](/ticdc/ticdc-overview.md)を参照してください。
-   エクスポートされたすべてのデータは[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用してTiDBにインポートし直すことができます。

</CustomContent>

> **注記：**
>
> PingCAP は以前、TiDB に固有の機能拡張を備えた[mydumperプロジェクト](https://github.com/maxbube/mydumper)のフォークを保守していました。 v7.5.0 以降、 [マイダンパー](https://docs-archive.pingcap.com/tidb/v4.0/mydumper-overview)は非推奨となり、その機能のほとんどが[Dumpling](/dumpling-overview.md)に置き換えられました。 mydumper の代わりにDumpling を使用することを強くお勧めします。

Dumplingには次のような利点があります。

-   SQLやCSVなど、複数の形式でのデータエクスポートをサポートします。
-   データのフィルタリングを容易にする[テーブルフィルター](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md)機能をサポートします。
-   Amazon S3クラウドstorageへのデータエクスポートをサポートします。
-   TiDB向けにさらなる最適化が行われました。
    -   TiDB SQLステートメントのメモリ制限を設定する機能をサポートします。
    -   Dumpling がTiDB クラスタの PD アドレスと[`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)テーブルにアクセスできる場合、 Dumpling はTiDB v4.0.0 以降のバージョンでブロック GC を実行するために[GC](/garbage-collection-overview.md)セーフポイント時間を自動的に調整することをサポートします。
    -   TiDBの非表示列`_tidb_rowid`を使用して、単一テーブルからの同時データエクスポートのパフォーマンスを最適化します。
    -   TiDB の場合、 [`tidb_snapshot`](/read-historical-data.md#how-tidb-reads-data-from-history-versions)の値を設定することで、データバックアップの時点を指定できます。これにより、 `FLUSH TABLES WITH READ LOCK`を使用して一貫性を確保する代わりに、バックアップの一貫性が確保されます。

> **注記：**
>
> Dumplingは、以下のシナリオではPDに接続できません。
>
> -   TiDBクラスタはKubernetes上で動作します（ただし、 Dumpling自体がKubernetes環境内で動作している場合は除きます）。
> -   TiDBクラスターはTiDB Cloud上で稼働しています。
>
> このような場合、エクスポートの失敗を避けるために手動で[TiDBのGC時間を調整する](#manually-set-the-tidb-gc-time)必要があります。

## TiDBまたはMySQLからデータをエクスポートする {#export-data-from-tidb-or-mysql}

### 必要な権限 {#required-privileges}

-   プロセス：クラスタ情報を照会してPDアドレスを取得し、PDを介してGCを制御する必要があります。
-   SELECT: テーブルをエクスポートする際に必須です。
-   RELOAD: `consistency`のレベルが`flush`の場合に必要です。アップストリームが RDS データベースまたはマネージド サービスの場合は、この権限を無視できます。
-   テーブルのロック: `consistency`のレベルが`lock`の場合に必要です。この権限は、エクスポートするすべてのデータベースとテーブルに対して付与する必要があります。
-   レプリケーションクライアント：データスナップショットを記録するためにメタデータをエクスポートする場合に必要です。この権限はオプションであり、メタデータをエクスポートする必要がない場合は無視できます。
-   ビューの表示：エクスポート用のビューメタデータを収集するために必要です。

### SQLファイルへのエクスポート {#export-to-sql-files}

このドキュメントは、127.0.0.1:4000 ホスト上に TiDB インスタンスが存在し、その TiDB インスタンスにパスワードのない root ユーザーが存在することを前提としています。

DumplingはデフォルトでデータをSQLファイルにエクスポートします。 `--filetype sql`フラグを追加することでも、データをSQLファイルにエクスポートできます。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 --filetype sql -t 8 -o /tmp/test -r 200000 -F 256MiB
```

上記のコマンドでは：

-   `-h` 、 `-P` 、および`-u`オプションは、それぞれアドレス、ポート、およびユーザーを意味します。認証にパスワードが必要な場合は、 `-p $YOUR_SECRET_PASSWORD`を使用してパスワードをDumplingに渡すことができます。

-   `-o` (または`--output` ) オプションは、storageのエクスポート ディレクトリを指定します。これは、絶対ローカル ファイル パスまたは[外部storageURI](/external-storage-uri.md)をサポートします。

-   `-t`オプションは、エクスポートに使用するスレッド数を指定します。スレッド数を増やすと、Dumplingの並列処理能力とエクスポート速度が向上しますが、データベースのメモリ使用量も増加します。そのため、スレッド数をあまり大きく設定することは推奨されません。通常は 64 未満に設定します。

-   `-r`オプションは、テーブル内同時実行を有効にしてエクスポートを高速化します。デフォルトでは無効になっています (値`0` )。 `0`より大きい値で有効にした場合、動作はソース データベースによって異なります。

    -   TiDBの場合、 Dumplingは領域情報を使用して分割を行うため、メモリ使用量も削減されます。指定された`-r`の値は、分割アルゴリズムには影響しません。
    -   MySQLの場合、このオプションは、主キー（または複合主キーの最初の列）が`INT`または`STRING`型である場合にサポートされます。

-   `-F`オプションは、単一ファイルの最大サイズを指定するために使用されます（単位は`MiB`です。 `5GiB`や`8KB`のような入力も許容されます）。このファイルを TiDB インスタンスにロードするためにTiDB Lightning を使用する場合は、その値を 256 MiB 以下に保つことをお勧めします。

> **注記：**
>
> エクスポートされた単一のテーブルのサイズが 10 GB を超える場合は、 `-r`および`-F`オプション**を使用することを**強くお勧めします。

#### storageサービスのURI形式 {#uri-formats-of-the-storage-services}

このセクションでは、Amazon S3、GCS、Azure Blob StorageなどのstorageサービスのURI形式について説明します。URI形式は以下のとおりです。

```shell
[scheme]://[host]/[path]?[parameters]
```

詳細については、[外部ストレージサービスのURI形式](/external-storage-uri.md)を参照してください。

### CSVファイルにエクスポート {#export-to-csv-files}

`--filetype csv`引数を追加することで、データをCSVファイルにエクスポートできます。

データをCSVファイルにエクスポートする際に、 `--sql <SQL>`を使用してSQLステートメントでレコードをフィルタリングできます。たとえば、次のコマンドを使用して`id < 100`内の`test.sbtest1`に一致するすべてのレコードをエクスポートできます。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test --filetype csv --sql 'select * from `test`.`sbtest1` where id < 100' -F 100MiB --output-filename-template 'test.sbtest1.{{.Index}}'
```

上記のコマンドでは：

-   `--sql`オプションは、CSV ファイルへのエクスポートにのみ使用できます。上記のコマンドは、エクスポート対象のすべてのテーブルに対して`SELECT * FROM <table-name> WHERE id <100`ステートメントを実行します。テーブルに指定されたフィールドがない場合、エクスポートは失敗します。

<CustomContent platform="tidb">

-   `--sql`オプションを使用すると、 Dumpling はエクスポートされたテーブルとスキーマ情報を取得できません。 `--output-filename-template`オプションを使用すると、CSV ファイルのファイル名形式を指定できます。これにより、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してデータ ファイルをインポートする際に便利です。たとえば、 `--output-filename-template='test.sbtest1.{{.Index}}'`は、エクスポートされた CSV ファイルの名前が`test.sbtest1.000000000`または`test.sbtest1.000000001`となることを指定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `--sql`オプションを使用すると、 Dumpling はエクスポートされたテーブルとスキーマ情報を取得できません。 `--output-filename-template`オプションを使用して、CSV ファイルのファイル名の形式を指定できます。たとえば、 `--output-filename-template='test.sbtest1.{{.Index}}'` 、エクスポートされた CSV ファイルの名前が`test.sbtest1.000000000`または`test.sbtest1.000000001`であることを指定します。

</CustomContent>

-   `--csv-separator`や`--csv-delimiter`などのオプションを使用して、CSV ファイル形式を構成できます。詳細については、 [Dumplingのオプション一覧](#option-list-of-dumpling)をご覧ください。

> **注記：**
>
> Dumplingでは*文字列*と*キーワードは*区別されません。インポートされたデータがブール型の場合、 `true`の値は`1`に変換され、 `false`の値は`0`に変換されます。

### エクスポートされたデータファイルを圧縮する {#compress-the-exported-data-files}

`--compress <format>`オプションを使用すると、 Dumplingによってエクスポートされた CSV および SQL データとテーブル構造ファイルを圧縮できます。このパラメーターは、 `gzip` 、 `snappy` 、および`zstd`アルゴリズムをサポートしています。圧縮はデフォルトでは無効になっています。

-   このオプションは、個々のデータファイルとテーブル構造ファイルのみを圧縮します。フォルダ全体を圧縮して単一の圧縮パッケージを生成することはできません。
-   このオプションはディスク容量を節約できますが、エクスポート速度が低下し、CPU使用率も増加します。エクスポート速度が非常に重要な場面では、このオプションの使用には注意が必要です。
-   TiDB Lightning v6.5.0以降のバージョンでは、 Dumplingによってエクスポートされた圧縮ファイルを、追加の設定なしでデータソースとして使用できます。

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。

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

-   `{schema}-schema-create.sql` : スキーマの作成に使用された SQL ファイル

    ```shell
    cat test-schema-create.sql
    ```

    ```shell
    CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
    ```

-   `{schema}.{table}-schema.sql` : テーブルを作成するために使用された SQL ファイル

    ```shell
    cat test.t1-schema.sql
    ```

    ```shell
    CREATE TABLE `t1` (
      `id` int DEFAULT NULL
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

-   `*-schema-view.sql` 、 `*-schema-trigger.sql` 、 `*-schema-post.sql` : その他のエクスポートされたファイル

### データをAmazon S3クラウドstorageにエクスポートする {#export-data-to-amazon-s3-cloud-storage}

バージョン4.0.8以降、 Dumplingはクラウドストレージへのデータエクスポートをサポートしています。Amazon S3にデータをバックアップする必要がある場合は、 `-o`パラメータでAmazon S3storageパスを指定する必要があります。

指定されたリージョンに Amazon S3 バケットを作成する必要があります ( [Amazonドキュメント - S3バケットの作成方法](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)参照)。バケット内にフォルダーを作成する必要がある場合は、 [Amazonドキュメント - フォルダの作成](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html)参照してください。

Amazon S3バックエンドstorageへのアクセス権限を持つアカウントの`SecretKey`と`AccessKey`を環境変数としてDumplingノードに渡します。

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

Dumpling は、 `~/.aws/credentials`からの認証情報ファイルの読み取りもサポートしています。 URI パラメーターの説明の詳細については、[外部ストレージサービスのURI形式](/external-storage-uri.md)を参照してください。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -r 200000 -o "s3://${Bucket}/${Folder}"
```

### エクスポートされたデータをフィルタリングする {#filter-the-exported-data}

#### <code>--where</code>オプションを使用してデータをフィルタリングします {#use-the-code-where-code-option-to-filter-data}

デフォルトでは、 Dumpling はシステム データベース ( `mysql` 、 `sys` 、 `INFORMATION_SCHEMA` 、 `PERFORMANCE_SCHEMA` 、 `METRICS_SCHEMA` 、および`INSPECTION_SCHEMA` ) を除くすべてのデータベースをエクスポートします。 `--where <SQL where expression>`を使用して、エクスポートするレコードを選択できます。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test --where "id < 100"
```

上記のコマンドは、各テーブルから`id < 100`に一致するデータをエクスポートします。 `--where`パラメータと`--sql`パラメータを同時に使用することはできませんのでご注意ください。

#### <code>--filter</code>オプションを使用してデータをフィルタリングします。 {#use-the-code-filter-code-option-to-filter-data}

Dumpling`--filter`オプションでテーブルフィルタを指定することで、特定のデータベースまたはテーブルをフィルタリングできます。テーブルフィルタの構文は`.gitignore`と同様です。詳細は、[テーブルフィルター](/table-filter.md)参照してください。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test -r 200000 --filter "employees.*" --filter "*.WorkOrder"
```

上記のコマンドは`employees`データベース内のすべてのテーブルと、すべてのデータベース内の`WorkOrder`テーブルをエクスポートします。

#### <code>-B</code>または<code>-T</code>オプションを使用してデータをフィルタリングします。 {#use-the-code-b-code-or-code-t-code-option-to-filter-data}

Dumpling、 `-B`オプションを使用して特定のデータベースをエクスポートしたり、 `-T`オプションを使用して特定のテーブルをエクスポートすることもできます。

> **注記：**
>
> -   `--filter`オプションと`-T`オプションは同時に使用できません。
> -   `-T`オプションは`database-name.table-name`のような完全な形式の入力のみを受け付け、テーブル名のみの入力は受け付けられません。例: Dumpling は`-T WorkOrder`を認識できません。

例：

-   `-B employees` `employees`データベースをエクスポートします。
-   `-T employees.WorkOrder` `employees.WorkOrder`テーブルをエクスポートします。

### 同時実行による輸出効率の向上 {#improve-export-efficiency-through-concurrency}

エクスポートされたファイルは、デフォルトでは`./export-<current local time>`ディレクトリに保存されます。よく使用されるオプションは以下のとおりです。

-   `-t`オプションは、エクスポートに使用するスレッド数を指定します。スレッド数を増やすと、Dumplingの並列処理能力とエクスポート速度が向上しますが、データベースのメモリ使用量も増加します。そのため、スレッド数をあまり大きく設定することはお勧めしません。
-   `-r`オプションは、テーブル内同時実行を有効にしてエクスポートを高速化します。デフォルト値は`0`で、無効を意味します。0 より大きい値は有効を意味し、値は`INT`型です。ソース データベースが TiDB の場合、0 より大きい`-r`値は、TiDB リージョン情報が分割に使用され、メモリ使用量が削減されることを示します。特定の`-r`値は、分割アルゴリズムに影響しません。ソースデータベースがMySQLで、主キーまたは複合主キーの最初の列が`INT`型の場合、 `-r`を指定することで、テーブル内同時実行を有効にすることもできます。
-   `--compress <format>`オプションは、ダンプの圧縮形式を指定します。このオプションは、 `gzip` 、 `snappy` 、および`zstd`の圧縮アルゴリズムをサポートしています。storageがボトルネックになっている場合や、storage容量が懸念される場合は、このオプションを使用するとデータのダンプを高速化できます。ただし、CPU 使用率が増加するという欠点があります。各ファイルは個別に圧縮されます。

上記のオプションを指定することで、 Dumplingはより高速なデータエクスポートを実現できます。

### Dumplingのデータ整合性オプションを調整する {#adjust-dumpling-s-data-consistency-options}

> **注記：**
>
> データ整合性オプションのデフォルト値は`auto`です。ほとんどの場合、 Dumplingのデフォルトのデータ整合性オプションを調整する必要はありません。

Dumpling は`--consistency <consistency level>`オプションを使用して、「一貫性の保証」のためにデータをエクスポートする方法を制御します。スナップショットを使用して一貫性を確保する場合、 `--snapshot`オプションを使用してバックアップするタイムスタンプを指定できます。また、次のレベルの一貫性も使用できます。

-   `flush` : [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock)を使用すると、レプリカ データベースの DML および DDL 操作を一時的に中断し、バックアップ 接続のグローバルな一貫性を確保し、binlog位置 (POS) 情報を記録できます。ロックは、すべてのバックアップ 接続がトランザクションを開始すると解放されます。フル バックアップは、ピーク時以外の時間帯、または MySQL レプリカ データベースで実行することをお勧めします。TiDB はこの値をサポートしていないことに注意してください。
-   `snapshot` : 指定されたタイムスタンプの一貫性のあるスナップショットを取得し、エクスポートします。
-   `lock` : エクスポートするすべてのテーブルに読み取りロックを追加します。
-   `none` : 一貫性は保証されません。
-   `auto` : MySQL には`flush`を、TiDB には`snapshot`を使用してください。

すべて完了したら、 `/tmp/test`にエクスポートされたファイルが表示されます。

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

### TiDBの履歴データスナップショットをエクスポート {#export-historical-data-snapshots-of-tidb}

Dumpling は`--snapshot`オプションを指定して、特定の[tidb_snapshot](/read-historical-data.md#how-tidb-reads-data-from-history-versions)のデータをエクスポートできます。

`--snapshot`オプションは、TSO ( `Position`コマンドによって出力される`SHOW MASTER STATUS`フィールド) または`datetime`データ タイプの有効時間 ( `YYYY-MM-DD hh:mm:ss`の形式) に設定できます。例:

```shell
tiup dumpling --snapshot 417773951312461825
tiup dumpling --snapshot "2020-07-02 17:12:45"
```

TSOが`417773951312461825`で時刻が`2020-07-02 17:12:45`のときのTiDB履歴データスナップショットがエクスポートされます。

### 大規模テーブルのエクスポート時のメモリ使用量を制御する {#control-the-memory-usage-of-exporting-large-tables}

DumplingがTiDBから大きな単一テーブルをエクスポートする際、エクスポートされるデータサイズが大きすぎるためにメモリ不足（OOM）が発生し、接続が中断されてエクスポートが失敗する場合があります。TiDBのメモリ使用量を削減するには、以下のパラメータを使用してください。

-   `-r`を設定すると、エクスポートするデータがチャンクに分割されます。これにより、TiDB のデータ スキャンのメモリオーバーヘッドが削減され、同時テーブル データ ダンプが可能になり、エクスポート効率が向上します。アップストリーム データベースが TiDB v3.0 以降のバージョンの場合、 `-r`の値が 0 より大きい場合は、TiDB リージョン情報が分割に使用され、特定の`-r`の値は分割アルゴリズムに影響しません。
-   `--tidb-mem-quota-query`の値を`8589934592` (8 GB) 以下まで減らしてください。 `--tidb-mem-quota-query` TiDB の単一クエリ ステートメントのメモリ使用量を制御します。
-   `--params "tidb_distsql_scan_concurrency=5"`パラメータを調整します。tidb_distsql_scan_concurrency [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 、TiDB でのスキャン操作の同時実行性を制御するセッション変数です。

### TiDBのGC時間を手動で設定する {#manually-set-the-tidb-gc-time}

TiDBからデータをエクスポートする場合（1TB未満）、TiDBのバージョンがv4.0.0以降で、 DumplingがTiDBクラスタのPDアドレスと[`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)テーブルにアクセスできる場合、 DumplingはGCセーフポイントを自動的に調整し、元のクラスタに影響を与えることなくGCをブロックします。

ただし、以下のいずれかのシナリオでは、 DumplingはGC時間を自動的に調整できません。

-   データサイズが非常に大きい（1TB以上）。
-   TiDBクラスタがTiDB Cloud上、またはDumplingとは別のKubernetes上にある場合、 DumplingはPDに直接接続できません。

このような場合、エクスポート処理中にガベージコレクション（GC）が原因でエクスポートが失敗しないように、事前にGC時間を手動で延長する必要があります。

GC時間を手動で調整するには、次のSQL文を使用します。

```sql
SET GLOBAL tidb_gc_life_time = '720h';
```

Dumpling が終了した後、エクスポートが成功したかどうかに関わらず、GC 時間を元の値に戻す必要があります (デフォルト値は`10m`です)。

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

## Dumplingのオプション一覧 {#option-list-of-dumpling}

| オプション                        | 使用法                                                                                                                                                                                                                                                                                                                                                                                 | デフォルト値                                                                                                                                                              |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-V`または`--version`           | Dumplingバージョンを出力して直接終了します。                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                     |
| `-B`または`--database`          | 指定したデータベースをエクスポートする                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                     |
| `-T`または`--tables-list`       | 指定したテーブルをエクスポートします                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                     |
| `-f`または`--filter`            | フィルター パターンに一致するテーブルをエクスポートします。フィルターの構文については、[テーブルフィルター](/table-filter.md)を参照してください。                                                                                                                                                                                                                                                                                                 | `[\*.\*,!/^(mysql&#124;sys&#124;INFORMATION_SCHEMA&#124;PERFORMANCE_SCHEMA&#124;METRICS_SCHEMA&#124;INSPECTION_SCHEMA)$/.\*]` （システムスキーマを除くすべてのデータベースまたはテーブルをエクスポート） |
| `--case-sensitive`           | テーブルフィルターが大文字と小文字を区別するかどうか                                                                                                                                                                                                                                                                                                                                                          | 偽（大文字小文字を区別しない）                                                                                                                                                     |
| `-h`または`--host`              | 接続されたデータベースホストのIPアドレス                                                                                                                                                                                                                                                                                                                                                               | 「127.0.0.1」                                                                                                                                                         |
| `-t`または`--threads`           | 同時バックアップスレッド数                                                                                                                                                                                                                                                                                                                                                                       | 4                                                                                                                                                                   |
| `-r`または`--rows`              | テーブル内同時実行を有効にすると、エクスポートが高速化されます。デフォルト値は`0`で、無効を意味します。0 より大きい値は有効を意味し、値は`INT`型です。ソース データベースが TiDB の場合、0 より大きい`-r`値は、TiDB リージョン情報が分割に使用され、メモリ使用量が削減されることを示します。特定の`-r`値は、分割アルゴリズムに影響しません。ソース データベースが MySQL で、主キーまたは複合主キーの最初の列が`INT`型の場合、 `-r`を指定することで、テーブル内同時実行を有効にすることもできます。                                                                                                          |                                                                                                                                                                     |
| `-L`または`--logfile`           | ログ出力アドレス。空欄の場合は、ログはコンソールに出力されます。                                                                                                                                                                                                                                                                                                                                                    | 「」                                                                                                                                                                  |
| `--loglevel`                 | ログレベル {debug,info,warn,error,dpanic, panic,fatal}                                                                                                                                                                                                                                                                                                                                   | &quot;情報&quot;                                                                                                                                                      |
| `--logfmt`                   | ログ出力形式：{text,json}                                                                                                                                                                                                                                                                                                                                                                  | &quot;文章&quot;                                                                                                                                                      |
| `-d`または`--no-data`           | データのエクスポートを行わない（スキーマのみをエクスポートする場合に適しています）                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                     |
| `--no-header`                | ヘッダーを生成せずにテーブルのCSVファイルをエクスポートする                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                     |
| `-W`または`--no-views`          | ビューをエクスポートしないでください                                                                                                                                                                                                                                                                                                                                                                  | 真実                                                                                                                                                                  |
| `-m`または`--no-schemas`        | データのみをエクスポートしてスキーマをエクスポートしないでください。                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                     |
| `-s`または`--statement-size`    | `INSERT`ステートメントのサイズを制御します。単位はバイトです。                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                     |
| `-F`または`--filesize`          | 分割されたテーブルのファイルサイズ。単位は`128B` 、 `64KiB` 、 `32MiB` 、 `1.5GiB`のように指定する必要があります。                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                     |
| `--filetype`                 | エクスポートされたファイル形式（csv/sql）                                                                                                                                                                                                                                                                                                                                                            | 「sql」                                                                                                                                                               |
| `-o`または`--output`            | データのエクスポートに使用する絶対ローカルファイルパス、または[外部storageURI](/external-storage-uri.md)を指定してください。                                                                                                                                                                                                                                                                                                   | &quot;./export-${time}&quot;                                                                                                                                        |
| `-S`または`--sql`               | 指定されたSQL文に従ってデータをエクスポートします。このコマンドは同時エクスポートをサポートしていません。                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                     |
| `--consistency`              | フラッシュ: ダンプの前にFTWRLを使用してください<br/>スナップショット: TSO の特定のスナップショットの TiDB データをダンプします<br/>ロック: ダンプ対象のすべてのテーブルに対して`lock tables read`を実行します<br/>none: ロックを追加せずにダンプします。これは一貫性を保証できません。<br/> auto: MySQL の場合は --consistency flush を使用し、TiDB の場合は --consistency snapshot を使用します。                                                                                                                   | 「自動」                                                                                                                                                                |
| `--snapshot`                 | スナップショットTSO。 `consistency=snapshot`の場合のみ有効。                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                     |
| `--where`                    | `where`条件を使用して、テーブルバックアップの範囲を指定します。                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                     |
| `-p`または`--password`          | 接続先のデータベースホストのパスワード                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                     |
| `-P`または`--port`              | 接続されたデータベースホストのポート                                                                                                                                                                                                                                                                                                                                                                  | 4000                                                                                                                                                                |
| `-u`または`--user`              | 接続されたデータベースホストのユーザー名                                                                                                                                                                                                                                                                                                                                                                | &quot;根&quot;                                                                                                                                                       |
| `--dump-empty-database`      | 空のデータベースの`CREATE DATABASE`ステートメントをエクスポートします。                                                                                                                                                                                                                                                                                                                                        | 真実                                                                                                                                                                  |
| `--ca`                       | TLS接続用の認証局ファイルのアドレス                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                     |
| `--cert`                     | TLS接続用のクライアント証明書ファイルのアドレス                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                     |
| `--key`                      | TLS接続用のクライアント秘密鍵ファイルのアドレス                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                     |
| `--csv-delimiter`            | CSVファイル内の文字型変数の区切り文字                                                                                                                                                                                                                                                                                                                                                                | &#39;&quot;&#39;                                                                                                                                                    |
| `--csv-separator`            | CSV ファイル内の各値の区切り文字。データにカンマが含まれている場合は、区切り文字として特殊な文字の組み合わせを使用することをお勧めします。非表示の文字もサポートされています。例: `--csv-separator $'\001'` 。                                                                                                                                                                                                                                                             | &#39;,&#39;                                                                                                                                                         |
| `--csv-null-value`           | CSVファイルにおけるnull値の表現                                                                                                                                                                                                                                                                                                                                                                 | &quot;\N&quot;                                                                                                                                                      |
| `--csv-line-terminator`      | CSV ファイルの行末の終端文字。データを CSV ファイルにエクスポートする際に、このオプションを使用して目的の終端文字を指定できます。このオプションは &quot;\r\n&quot; と &quot;\n&quot; をサポートしています。デフォルト値は &quot;\r\n&quot; で、以前のバージョンと互換性があります。bash の引用符はエスケープ規則が異なるため、LF (改行) を終端文字として指定する場合は、 `--csv-line-terminator $'\n'`に似た構文を使用できます。                                                                                                                 | &quot;\r\n&quot;                                                                                                                                                    |
| `--csv-output-dialect`       | ソースデータをデータベースで指定された形式の CSV ファイルにエクスポートできることを示します。オプションの値は`""` 、 `"snowflake"` 、 `"redshift"` 、 `"bigquery"`のいずれかです。デフォルト値は`""`で、ソースデータを UTF-8 でエンコードしてエクスポートすることを意味します。オプションを`"snowflake"`または`"redshift"`に設定すると、ソースデータのバイナリデータ型は 16 進数に変換されますが、 `0x`の接頭辞は削除されます。例えば、 `0x61` `61`と表示されます。オプションを`"bigquery"`に設定すると、バイナリデータ型は base64 を使用してエンコードされます。場合によっては、バイナリ文字列に文字化けが発生する可能性があります。 | `""`                                                                                                                                                                |
| `--escape-backslash`         | エクスポートファイル内の特殊文字をエスケープするには、バックスラッシュ（ `\` ）を使用します。                                                                                                                                                                                                                                                                                                                                   | 真実                                                                                                                                                                  |
| `--output-filename-template` | [Go言語テンプレート](https://golang.org/pkg/text/template/#hdr-Arguments)の形式で表されるファイル名テンプレート<br/>`{{.DB}}` 、 `{{.Table}}` 、および`{{.Index}}`引数をサポートします。<br/> 3つの引数は、データベース名、テーブル名、およびデータファイルのチャンクIDを表します。                                                                                                                                                                                     | `{{.DB}}.{{.Table}}.{{.Index}}`                                                                                                                                     |
| `--status-addr`              | Dumplingのサービスアドレス（Prometheusがメトリクスを取得するアドレスとpprofデバッグ用アドレスを含む）                                                                                                                                                                                                                                                                                                                      | &quot;:8281&quot;                                                                                                                                                   |
| `--tidb-mem-quota-query`     | Dumplingコマンドの1行でエクスポートするSQLステートメントのメモリ制限値で、単位はバイトです。v4.0.10以降のバージョンでは、このパラメータを設定しない場合、TiDBはデフォルトで`mem-quota-query`構成項目の値をメモリ制限値として使用します。v4.0.10より前のバージョンでは、パラメータ値のデフォルト値は32GBです。                                                                                                                                                                                                    | 34359738368                                                                                                                                                         |
| `--params`                   | エクスポートするデータベースへの接続に使用するセッション変数を指定します。必須の形式は`"character_set_client=latin1,character_set_connection=latin1"`です。                                                                                                                                                                                                                                                                       |                                                                                                                                                                     |
| `-c`または`--compress`          | Dumplingによってエクスポートされた CSV および SQL データとテーブル構造ファイルを圧縮します。次の圧縮アルゴリズムをサポートしています: `gzip` 、 `snappy` 、および`zstd` 。                                                                                                                                                                                                                                                                         | 「」                                                                                                                                                                  |

## 出力ファイル名テンプレート {#output-filename-template}

`--output-filename-template`引数は、ファイル拡張子を除いた出力ファイルの命名規則を定義します。Go[Go `text/template`構文](https://golang.org/pkg/text/template/)内の文字列を受け入れます。 。

テンプレートには以下のフィールドが利用可能です。

-   `.DB` : データベース名
-   `.Table` : テーブル名またはオブジェクト名
-   `.Index` : テーブルが複数のファイルに分割されている場合の、ファイルの0から始まるシーケンス番号。どの部分がダンプされるかを示します。たとえば、 `{{printf "%09d" .Index}}`は、 `.Index`先頭にゼロが付いた9桁の数値としてフォーマットすることを意味します。

データベース名やテーブル名には、ファイルシステムでは使用できない特殊文字（例： `/` ）が含まれている場合があります。この問題を解決するために、 Dumpling はこれらの特殊文字をパーセントエンコードする`fn`関数を提供しています。

-   U+0000～U+001F（制御文字）
-   `/` 、 `\` 、 `<` 、 `>` 、 `:` 、 `"` 、 `*` 、 `?` (無効な Windows パス文字)
-   `.` （データベース名またはテーブル名の区切り文字）
-   `-` 、 `-schema`の一部として使用される場合

例えば、 `--output-filename-template '{{fn .Table}}.{{printf "%09d" .Index}}'`を使用すると、 Dumplingはテーブル`db.tbl:normal`を`tbl%3Anormal.000000000.sql` 、 `tbl%3Anormal.000000001.sql`などという名前のファイルに書き込みます。

出力データファイルに加えて、 `--output-filename-template`を定義することで、スキーマファイルのファイル名を置き換えることができます。以下の表に、デフォルトの設定を示します。

| 名前   | コンテンツ                                      |
| ---- | ------------------------------------------ |
| データ  | `{{fn .DB}}.{{fn .Table}}.{{.Index}}`      |
| スキーマ | `{{fn .DB}}-schema-create`                 |
| テーブル | `{{fn .DB}}.{{fn .Table}}-schema`          |
| イベント | `{{fn .DB}}.{{fn .Table}}-schema-post`     |
| 関数   | `{{fn .DB}}.{{fn .Table}}-schema-post`     |
| 手順   | `{{fn .DB}}.{{fn .Table}}-schema-post`     |
| 順序   | `{{fn .DB}}.{{fn .Table}}-schema-sequence` |
| トリガー | `{{fn .DB}}.{{fn .Table}}-schema-triggers` |
| ビュー  | `{{fn .DB}}.{{fn .Table}}-schema-view`     |

例えば、 `--output-filename-template '{{define "table"}}{{fn .Table}}.$schema{{end}}{{define "data"}}{{fn .Table}}.{{printf "%09d" .Index}}{{end}}'`を使用すると、 Dumpling はテーブル`db.tbl:normal`のスキーマを`tbl%3Anormal.$schema.sql`という名前のファイルに書き込み、データを`tbl%3Anormal.000000000.sql` 、 `tbl%3Anormal.000000001.sql`などのファイルに書き込みます。

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="TiDB Admin Lab 7: Exporting Data Using Dumpling" type="lab" link="https://labs.tidb.io/labs/dba_303_lab_ff6" imgSrc="https://lab-static.pingcap.com/quick-demo/dba_303_ch08_en.png" duration="60 mins" />
</RelatedResources>
