---
title: Dumpling Overview
summary: Dumplingツールを使用して TiDB からデータをエクスポートします。
---

# Dumplingを使用してデータをエクスポートする {#use-dumpling-to-export-data}

このドキュメントでは、データエクスポートツール - [Dumpling](https://github.com/pingcap/tidb/tree/release-8.5/dumpling)を紹介します。Dumplingは、TiDB/MySQL に保存されているデータを SQL または CSV データファイルとしてエクスポートし、論理的な完全バックアップやエクスポートに使用できます。DumplingはAmazon S3 へのデータエクスポートもサポートしています。

<CustomContent platform="tidb">

[TiUP](/tiup/tiup-overview.md)使って`tiup install dumpling`実行するとDumplingが手に入ります。その後、 `tiup dumpling ...`使ってDumpling を実行できます。

DumplingインストールパッケージはTiDB Toolkitに含まれています。TiDBTiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロード](/download-ecosystem-tools.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

次のコマンドを使用してDumplingをインストールできます。

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
source ~/.bash_profile
tiup install dumpling
```

上記のコマンドでは、 `~/.bash_profile`プロファイル ファイルのパスに変更する必要があります。

</CustomContent>

Dumplingの詳細な使用方法については、 `--help`オプションを使用するか、 [Dumplingのオプションリスト](#option-list-of-dumpling)を参照してください。

Dumplingを使用する場合は、実行中のクラスターでエクスポート コマンドを実行する必要があります。

<CustomContent platform="tidb">

TiDB には、必要に応じて使用できる他のツールも用意されています。

-   SST ファイル (キーと値のペア) のバックアップ、またはレイテンシーの影響を受けない増分データのバックアップについては、 [BR](/br/backup-and-restore-overview.md)を参照してください。
-   増分データのリアルタイムバックアップについては、 [TiCDC](/ticdc/ticdc-overview.md)を参照してください。
-   エクスポートされたすべてのデータは、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用して TiDB に再度インポートできます。

</CustomContent>

> **注記：**
>
> PingCAPは以前、TiDBに特化した機能強化を加えたバージョン[mydumperプロジェクト](https://github.com/maxbube/mydumper)のフォークを保守していました。バージョン7.5.0以降、 [マイダンパー](https://docs-archive.pingcap.com/tidb/v4.0/mydumper-overview)非推奨となり、その機能の大部分は[Dumpling](/dumpling-overview.md)に置き換えられました。mydumperではなくDumplingを使用することを強くお勧めします。

Dumplingには次のような利点があります。

-   SQL や CSV など複数の形式でのデータのエクスポートをサポートします。
-   データのフィルタリングを容易にする[テーブルフィルター](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md)機能をサポートします。
-   Amazon S3 クラウドstorageへのデータのエクスポートをサポートします。
-   TiDB に対してさらなる最適化が行われました:
    -   単一のTiDB SQLステートメントのメモリ制限の構成をサポートします。
    -   Dumpling がTiDB クラスターの PD アドレスと[`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)テーブルにアクセスできる場合、 Dumpling はTiDB v4.0.0 以降のバージョンで[GC](/garbage-collection-overview.md)セーフ ポイント時間をブロック GC に自動的に調整することをサポートします。
    -   TiDB の隠し列`_tidb_rowid`を使用して、単一のテーブルからの同時データ エクスポートのパフォーマンスを最適化します。
    -   TiDBの場合、データのバックアップ時点を指定するために値[`tidb_snapshot`](/read-historical-data.md#how-tidb-reads-data-from-history-versions)を設定できます。これにより、整合性を確保するために`FLUSH TABLES WITH READ LOCK`使用する代わりに、バックアップの整合性が確保されます。

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
-   RELOAD: `consistency`のレベルが`flush`場合に必須です。アップストリームが RDS データベースまたはマネージドサービスの場合は、この権限は無視できます。
-   LOCK TABLES: レベル`consistency`が`lock`場合に必要です。この権限は、エクスポートするすべてのデータベースとテーブルに付与する必要があります。
-   レプリケーションクライアント: データのスナップショットを記録するためにメタデータをエクスポートする場合に必要です。この権限はオプションであり、メタデータをエクスポートする必要がない場合は無視できます。

### SQLファイルへのエクスポート {#export-to-sql-files}

このドキュメントでは、127.0.0.1:4000 ホストに TiDB インスタンスがあり、この TiDB インスタンスにパスワードのない root ユーザーが存在することを前提としています。

DumplingはデフォルトでSQLファイルにデータをエクスポートします。1フラグ`--filetype sql`追加することで、SQLファイルにデータをエクスポートすることもできます。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 --filetype sql -t 8 -o /tmp/test -r 200000 -F 256MiB
```

上記のコマンドでは、

-   `-h` 、 `-P` 、 `-u`オプションはそれぞれ、アドレス、ポート、ユーザーを意味します。認証にパスワードが必要な場合は、 `-p $YOUR_SECRET_PASSWORD`使用してDumplingにパスワードを渡すことができます。

-   `-o` (または`--output` ) オプションは、storageのエクスポート ディレクトリを指定します。これは、絶対ローカル ファイル パスまたは[外部storageURI](/external-storage-uri.md)サポートします。

-   `-t`オプションは、エクスポートのスレッド数を指定します。スレッド数を増やすと、 Dumplingの同時実行性とエクスポート速度が向上しますが、データベースのメモリ消費量も増加します。そのため、スレッド数を大きくしすぎることは推奨されません。通常は 64 未満です。

-   オプション`-r`は、テーブル内同時実行を有効にしてエクスポートを高速化します。デフォルトでは無効（値`0` ）です。有効にした場合、 `0`より大きい値で動作はソースデータベースによって異なります。

    -   TiDBの場合、 Dumplingは分割にリージョン情報を使用するため、メモリ使用量も削減されます。指定された値`-r`分割アルゴリズムに影響を与えません。
    -   MySQL の場合、このオプションは、主キー (または複合主キーの最初の列) が`INT`または`STRING`タイプの場合にサポートされます。

-   `-F`オプションは、単一ファイルの最大サイズを指定するために使用されます（単位は`MiB`ですが、 `5GiB`や`8KB`の入力も許容されます）。TiDB TiDB Lightningを使用してこのファイルを TiDB インスタンスにロードする場合は、この値を 256 MiB 以下に抑えることをお勧めします。

> **注記：**
>
> エクスポートされた単一のテーブルのサイズが 10 GB を超える場合は、オプション`-r`と`-F`**使用することを強くお勧めします**。

#### storageサービスのURI形式 {#uri-formats-of-the-storage-services}

このセクションでは、Amazon S3、GCS、Azure Blob StorageなどのstorageサービスのURI形式について説明します。URI形式は次のとおりです。

```shell
[scheme]://[host]/[path]?[parameters]
```

詳細については[外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

### CSVファイルへのエクスポート {#export-to-csv-files}

`--filetype csv`引数を追加することで、データを CSV ファイルにエクスポートできます。

データをCSVファイルにエクスポートする際、SQL文を使って`--sql <SQL>`をフィルタリングできます。例えば、以下のコマンドを使うと、 `id < 100`行中`test.sbtest1`行に一致するすべてのレコードをエクスポートできます。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test --filetype csv --sql 'select * from `test`.`sbtest1` where id < 100' -F 100MiB --output-filename-template 'test.sbtest1.{{.Index}}'
```

上記のコマンドでは、

-   `--sql`オプションはCSVファイルへのエクスポートにのみ使用できます。上記のコマンドは、エクスポート対象となるすべてのテーブルに対して`SELECT * FROM <table-name> WHERE id <100`ステートメントを実行します。指定されたフィールドがテーブルに存在しない場合、エクスポートは失敗します。

<CustomContent platform="tidb">

-   オプション`--sql`使用すると、 Dumplingはエクスポートされたテーブルとスキーマ情報を取得できません。オプション`--output-filename-template`を使用してCSVファイルのファイル名形式を指定できます。これにより、後でオプション[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してデータファイルをインポートしやすくなります。例えば、オプション`--output-filename-template='test.sbtest1.{{.Index}}'`を指定すると、エクスポートされたCSVファイルは`test.sbtest1.000000000`または`test.sbtest1.000000001`という名前になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   オプション`--sql`使用すると、 Dumplingはエクスポートされたテーブルとスキーマ情報を取得できません。オプション`--output-filename-template`使用すると、CSVファイルのファイル名の形式を指定できます。例えば、オプション`--output-filename-template='test.sbtest1.{{.Index}}'`を指定すると、エクスポートされたCSVファイルは`test.sbtest1.000000000`または`test.sbtest1.000000001`名前になります。

</CustomContent>

-   `--csv-separator`や`--csv-delimiter`などのオプションを使用してCSVファイル形式を設定できます。詳細については、 [Dumplingのオプションリスト](#option-list-of-dumpling)を参照してください。

> **注記：**
>
> Dumplingでは*文字列*と*キーワード*は区別されません。インポートされたデータがブール型の場合、値`true`は`1`に、値`false`は`0`に変換されます。

### エクスポートしたデータファイルを圧縮する {#compress-the-exported-data-files}

`--compress <format>`オプションを使用すると、 Dumplingによってエクスポートされる CSV および SQL データファイルとテーブル構造ファイルを圧縮できます。このパラメータは、 `gzip` 、 `snappy` 、 `zstd`の圧縮アルゴリズムをサポートしています。圧縮はデフォルトで無効になっています。

-   このオプションは、個々のデータファイルとテーブル構造ファイルのみを圧縮します。フォルダ全体を圧縮して単一の圧縮パッケージを生成することはできません。
-   このオプションはディスク容量を節約できますが、エクスポート速度が低下し、CPU消費量が増加します。エクスポート速度が重要なシナリオでは、このオプションの使用には注意が必要です。
-   TiDB Lightning v6.5.0 以降のバージョンでは、追加の構成なしで、 Dumplingによってエクスポートされた圧縮ファイルをデータ ソースとして使用できます。

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。

### エクスポートファイルの形式 {#format-of-exported-files}

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

-   `*-schema-view.sql` ：その他`*-schema-trigger.sql` `*-schema-post.sql`ファイル

### Amazon S3クラウドstorageにデータをエクスポートする {#export-data-to-amazon-s3-cloud-storage}

バージョン4.0.8以降、 Dumplingはクラウドストレージへのデータのエクスポートをサポートしています。Amazon S3にデータをバックアップする必要がある場合は、 `-o`のパラメータでAmazon S3storageのパスを指定する必要があります。

指定されたリージョンにAmazon S3バケットを作成する必要があります（ [Amazonドキュメント - S3バケットを作成する方法](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)を参照）。バケット内にフォルダも作成する必要がある場合は、 [Amazonドキュメント - フォルダの作成](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html)参照してください。

Amazon S3 バックエンドstorageへのアクセス権を持つアカウントの`SecretKey`と`AccessKey`環境変数としてDumplingノードに渡します。

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

Dumplingは`~/.aws/credentials`からの認証情報ファイルの読み取りもサポートしています。URIパラメータの説明の詳細については、 [外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -r 200000 -o "s3://${Bucket}/${Folder}"
```

### エクスポートしたデータをフィルタリングする {#filter-the-exported-data}

#### <code>--where</code>オプションを使用してデータをフィルタリングします {#use-the-code-where-code-option-to-filter-data}

デフォルトでは、 Dumplingは`INSPECTION_SCHEMA`データベース（ `mysql`を含む`INFORMATION_SCHEMA`を除くすべて`sys`データベースをエクスポートします`--where <SQL where expression>` `PERFORMANCE_SCHEMA`使用して、エクスポートするレコード`METRICS_SCHEMA`選択できます。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test --where "id < 100"
```

上記のコマンドは、各テーブルから`id < 100`一致するデータをエクスポートします。3 パラメータと`--where` `--sql`を同時に使用できないことに注意してください。

#### <code>--filter</code>オプションを使用してデータをフィルタリングします {#use-the-code-filter-code-option-to-filter-data}

Dumplingは、 `--filter`オプションでテーブルフィルターを指定することで、特定のデータベースまたはテーブルをフィルタリングできます。テーブルフィルターの構文は`.gitignore`と同様です。詳細は[テーブルフィルター](/table-filter.md)参照してください。

```shell
tiup dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test -r 200000 --filter "employees.*" --filter "*.WorkOrder"
```

上記のコマンドは、 `employees`データベース内のすべてのテーブルと、すべてのデータベース内の`WorkOrder`テーブルをエクスポートします。

#### <code>-B</code>または<code>-T</code>オプションを使用してデータをフィルタリングします {#use-the-code-b-code-or-code-t-code-option-to-filter-data}

Dumpling は、 `-B`オプションを使用して特定のデータベースをエクスポートしたり、 `-T`オプションを使用して特定のテーブルをエクスポートすることもできます。

> **注記：**
>
> -   オプション`--filter`とオプション`-T`を同時に使用することはできません。
> -   `-T`オプションは`database-name.table-name`ような完全な形式の入力のみを受け入れます。テーブル名のみの入力は受け入れられません。例： Dumpling は`-T WorkOrder`認識できません。

例:

-   `-B employees` `employees`データベースをエクスポートします。
-   `-T employees.WorkOrder` `employees.WorkOrder`テーブルをエクスポートします。

### 同時実行による輸出効率の向上 {#improve-export-efficiency-through-concurrency}

エクスポートされたファイルはデフォルトで`./export-<current local time>`ディレクトリに保存されます。よく使用されるオプションは次のとおりです。

-   `-t`オプションはエクスポートのスレッド数を指定します。スレッド数を増やすと、 Dumplingの同時実行性が向上し、エクスポート速度も向上しますが、データベースのメモリ消費量も増加します。そのため、スレッド数を大きくしすぎることは推奨されません。
-   `-r`オプションは、テーブル内同時実行を有効にしてエクスポートを高速化します。デフォルト値は`0`で、無効を意味します。0 より大きい値は有効を意味し、値は`INT`型です。ソースデータベースが TiDB の場合、0 より大きい値`-r` 、TiDB リージョン情報が分割に使用され、メモリ使用量が削減されることを示します。特定の値`-r`は分割アルゴリズムに影響を与えません。ソースデータベースが MySQL で、主キーまたは複合主キーの最初の列が`INT`型の場合、 `-r`指定するとテーブル内同時実行が有効になります。
-   `--compress <format>`オプションはダンプの圧縮形式を指定します。3、5、7 `gzip`圧縮アルゴリズムをサポートしています。storageがボトルネックになっている場合やstorage容量が懸念される場合、このオプションを使用するとデータのダンプ`zstd`高速化できます。ただし、CPU使用率が増加するという欠点があります。各ファイル`snappy`個別に圧縮されます。

上記のオプションを指定すると、 Dumpling はデータのエクスポート速度を速めることができます。

### Dumplingのデータ一貫性オプションを調整する {#adjust-dumpling-s-data-consistency-options}

> **注記：**
>
> データ整合性オプションのデフォルト値は`auto`です。ほとんどのシナリオでは、 Dumplingのデフォルトのデータ整合性オプションを調整する必要はありません。

Dumplingは、 `--consistency <consistency level>`オプションを使用して、「整合性保証」のためにデータのエクスポート方法を制御します。整合性のためにスナップショットを使用する場合は、 `--snapshot`オプションを使用してバックアップするタイムスタンプを指定できます。また、以下の整合性レベルも使用できます。

-   `flush` : レプリカデータベースのDMLおよびDDL操作を一時的に中断し、バックアップ接続のグローバルな一貫性を確保し、binlog位置（POS）情報を記録するために、 [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock)使用します。ロックは、すべてのバックアップ接続がトランザクションを開始した後に解除されます。フルバックアップは、オフピーク時間帯またはMySQLレプリカデータベースで実行することをお勧めします。TiDBはこの値をサポートしていないことに注意してください。
-   `snapshot` : 指定されたタイムスタンプの一貫性のあるスナップショットを取得してエクスポートします。
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

Dumplingは`--snapshot`オプションを指定して特定の[tidb_スナップショット](/read-historical-data.md#how-tidb-reads-data-from-history-versions)のデータをエクスポートすることができます。

`--snapshot`オプションは、TSO ( `SHOW MASTER STATUS`コマンドによって出力される`Position`フィールド) または`datetime`データ型の有効な時刻 ( `YYYY-MM-DD hh:mm:ss`の形式) に設定できます。次に例を示します。

```shell
tiup dumpling --snapshot 417773951312461825
tiup dumpling --snapshot "2020-07-02 17:12:45"
```

TSO が`417773951312461825`で時間が`2020-07-02 17:12:45`ときの TiDB 履歴データ スナップショットがエクスポートされます。

### 大きなテーブルのエクスポート時のメモリ使用量を制御する {#control-the-memory-usage-of-exporting-large-tables}

DumplingがTiDBから大きな単一テーブルをエクスポートする際、エクスポートデータのサイズが大きすぎるためにメモリ不足（OOM）が発生することがあります。これにより、接続が中断され、エクスポートが失敗します。以下のパラメータを使用することで、TiDBのメモリ使用量を削減できます。

-   `-r`設定すると、エクスポートするデータがチャンクに分割されます。これにより、TiDB のデータスキャンのメモリオーバーヘッドが削減され、テーブルデータの同時ダンプが可能になり、エクスポート効率が向上します。上流データベースが TiDB v3.0 以降の場合、 `-r`が 0 より大きい場合、分割には TiDB のリージョン情報が使用され、 `-r`値は分割アルゴリズムに影響を与えません。
-   `--tidb-mem-quota-query`の値を`8589934592` (8 GB) 以下に減らします。5 `--tidb-mem-quota-query` 、TiDB 内の単一のクエリ ステートメントのメモリ使用量を制御します。
-   `--params "tidb_distsql_scan_concurrency=5"`パラメータを調整します。3 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 、TiDB でのスキャン操作の同時実行を制御するセッション変数です。

### TiDB GC時間を手動で設定する {#manually-set-the-tidb-gc-time}

TiDB (1 TB 未満) からデータをエクスポートする場合、TiDB のバージョンが v4.0.0 以降で、 Dumplingが TiDB クラスターの PD アドレスと[`INFORMATION_SCHEMA.CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)テーブルにアクセスできる場合、 Dumpling はGC セーフ ポイントを自動的に調整し、元のクラスターに影響を与えずに GC をブロックします。

ただし、次のいずれかのシナリオでは、 Dumpling はGC 時間を自動的に調整できません。

-   データサイズが非常に大きい（1TB以上）。
-   たとえば、TiDB クラスターがTiDB Cloud上にある場合や、 Dumplingから分離された Kubernetes 上にある場合、 Dumpling はPD に直接接続できません。

このようなシナリオでは、エクスポート プロセス中の GC によるエクスポートの失敗を回避するために、事前に GC 時間を手動で延長する必要があります。

GC 時間を手動で調整するには、次の SQL ステートメントを使用します。

```sql
SET GLOBAL tidb_gc_life_time = '720h';
```

Dumplingが終了したら、エクスポートが成功したかどうかに関係なく、GC 時間を元の値に戻す必要があります (デフォルト値は`10m`です)。

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

## Dumplingのオプションリスト {#option-list-of-dumpling}

| オプション                        | 使用法                                                                                                                                                                                                                                                                                                                                                                                | デフォルト値                                                                                                                                                               |             |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `-V`または`--version`           | Dumplingバージョンを出力して直接終了する                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                      |             |
| `-B`または`--database`          | 指定されたデータベースをエクスポートする                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                      |             |
| `-T`または`--tables-list`       | 指定されたテーブルをエクスポートする                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                      |             |
| `-f`または`--filter`            | フィルタパターンに一致するテーブルをエクスポートします。フィルタ構文については[テーブルフィルター](/table-filter.md)参照してください。                                                                                                                                                                                                                                                                                                      | `[\*.\*,!/^(mysql&#124;sys&#124;INFORMATION_SCHEMA&#124;PERFORMANCE_SCHEMA&#124;METRICS_SCHEMA&#124;INSPECTION_SCHEMA)$/.\*]` (システム スキーマを除くすべてのデータベースまたはテーブルをエクスポート) |             |
| `--case-sensitive`           | テーブルフィルタが大文字と小文字を区別するかどうか                                                                                                                                                                                                                                                                                                                                                          | 偽（大文字と小文字を区別しない）                                                                                                                                                     |             |
| `-h`または`--host`              | 接続されたデータベースホストのIPアドレス                                                                                                                                                                                                                                                                                                                                                              | 「127.0.0.1」                                                                                                                                                          |             |
| `-t`または`--threads`           | 同時バックアップスレッドの数                                                                                                                                                                                                                                                                                                                                                                     | 4                                                                                                                                                                    |             |
| `-r`または`--rows`              | エクスポートを高速化するために、テーブル内同時実行を有効にします。デフォルト値は`0`で、無効を意味します。0 より大きい値は有効を意味し、値は`INT`型です。ソースデータベースが TiDB の場合、0 より大きい値`-r`は、TiDB リージョン情報を使用して分割し、メモリ使用量を削減することを示します。特定の値`-r`は分割アルゴリズムに影響を与えません。ソースデータベースが MySQL で、主キーまたは複合主キーの最初の列が`INT`型の場合、 `-r`指定することでもテーブル内同時実行を有効にできます。                                                                                                                |                                                                                                                                                                      |             |
| `-L`または`--logfile`           | ログ出力アドレス。空の場合、ログはコンソールに出力されます。                                                                                                                                                                                                                                                                                                                                                     | 「」                                                                                                                                                                   |             |
| `--loglevel`                 | ログレベル {debug、info、warn、error、dpanic、 panic、fatal}                                                                                                                                                                                                                                                                                                                                  | &quot;情報&quot;                                                                                                                                                       |             |
| `--logfmt`                   | ログ出力形式 {text,json}                                                                                                                                                                                                                                                                                                                                                                 | &quot;文章&quot;                                                                                                                                                       |             |
| `-d`または`--no-data`           | データをエクスポートしない (スキーマのみをエクスポートするシナリオに適しています)                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                      |             |
| `--no-header`                | ヘッダーを生成せずにテーブルのCSVファイルをエクスポートする                                                                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                      |             |
| `-W`または`--no-views`          | ビューをエクスポートしない                                                                                                                                                                                                                                                                                                                                                                      | 真実                                                                                                                                                                   |             |
| `-m`または`--no-schemas`        | データのみをエクスポートしてスキーマをエクスポートしないでください                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                      |             |
| `-s`または`--statement-size`    | `INSERT`文のサイズを制御します。単位はバイトです。                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                                      |             |
| `-F`または`--filesize`          | 分割されたテーブルのファイルサイズ。1、3、5、7などの`128B` `32MiB`指定する必要があり`1.5GiB` `64KiB`                                                                                                                                                                                                                                                                                                                |                                                                                                                                                                      |             |
| `--filetype`                 | エクスポートされたファイルの種類 (csv/sql)                                                                                                                                                                                                                                                                                                                                                         | 「SQL」                                                                                                                                                                |             |
| `-o`または`--output`            | データをエクスポートするには、絶対ローカル ファイル パスまたは[外部storageURI](/external-storage-uri.md)指定します。                                                                                                                                                                                                                                                                                                     | 「./export-${time}」                                                                                                                                                   |             |
| `-S`または`--sql`               | 指定されたSQL文に従ってデータをエクスポートします。このコマンドは同時エクスポートをサポートしていません。                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                      |             |
| `--consistency`              | フラッシュ: ダンプの前に FTWRL を使用する<br/>スナップショット: TSO の特定のスナップショットの TiDB データをダンプします。<br/>ロック: ダンプするすべてのテーブルに対して`lock tables read`実行する<br/>なし: ロックを追加せずにダンプします。一貫性は保証されません。<br/>自動: MySQL の場合は --consistency フラッシュを使用します。TiDB の場合は --consistency スナップショットを使用します。                                                                                                                              | 「自動」                                                                                                                                                                 |             |
| `--snapshot`                 | スナップショットTSO; `consistency=snapshot`場合にのみ有効                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                      |             |
| `--where`                    | `where`条件でテーブルバックアップの範囲を指定します                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                                      |             |
| `-p`または`--password`          | 接続されたデータベースホストのパスワード                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                      |             |
| `-P`または`--port`              | 接続されたデータベースホストのポート                                                                                                                                                                                                                                                                                                                                                                 | 4000                                                                                                                                                                 |             |
| `-u`または`--user`              | 接続されたデータベースホストのユーザー名                                                                                                                                                                                                                                                                                                                                                               | &quot;根&quot;                                                                                                                                                        |             |
| `--dump-empty-database`      | 空のデータベースの`CREATE DATABASE`ステートメントをエクスポートします                                                                                                                                                                                                                                                                                                                                        | 真実                                                                                                                                                                   |             |
| `--ca`                       | TLS接続用の証明機関ファイルのアドレス                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                      |             |
| `--cert`                     | TLS接続用のクライアント証明書ファイルのアドレス                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                      |             |
| `--key`                      | TLS接続用のクライアント秘密鍵ファイルのアドレス                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                      |             |
| `--csv-delimiter`            | CSVファイル内の文字型変数の区切り文字                                                                                                                                                                                                                                                                                                                                                               | &#39;&quot;&#39;                                                                                                                                                     |             |
| `--csv-separator`            | CSVファイル内の各値の区切り文字。デフォルトの「,」の使用は推奨されません。「|+|」などの一般的ではない文字の組み合わせを使用することをお勧めします。                                                                                                                                                                                                                                                                                                      | &#39;,&#39;                                                                                                                                                          | &#39;,&#39; |
| `--csv-null-value`           | CSVファイルにおけるnull値の表現                                                                                                                                                                                                                                                                                                                                                                | 「\N」                                                                                                                                                                 |             |
| `--csv-line-terminator`      | CSVファイルの行末の終端文字です。データをCSVファイルにエクスポートする際に、このオプションを使用して任意の終端文字を指定できます。このオプションは「\r\n」と「\n」をサポートしています。デフォルト値は「\r\n」で、これは以前のバージョンと同じです。bashの引用符には異なるエスケープ規則があるため、LF（改行）を終端文字として指定する場合は、 `--csv-line-terminator $'\n'`のような構文を使用できます。                                                                                                                                                     | &quot;\r\n&quot;                                                                                                                                                     |             |
| `--csv-output-dialect`       | ソースデータを、データベースに必要な特定の形式でCSVファイルにエクスポートできることを示します。オプションの値は、 `""` 、 `"snowflake"` 、 `"redshift"` 、または`"bigquery"`です。デフォルト値は`""`で、ソースデータをUTF-8でエンコードしてエクスポートすることを意味します。オプションを`"snowflake"`または`"redshift"`に設定すると、ソースデータ内のバイナリデータ型は16進数に変換されますが、プレフィックスの`0x`削除されます。たとえば、 `0x61` `61`と表されます。オプションを`"bigquery"`に設定すると、バイナリデータ型はbase64を使用してエンコードされます。場合によっては、バイナリ文字列に文字化けした文字が含まれることがあります。 | `""`                                                                                                                                                                 |             |
| `--escape-backslash`         | エクスポートファイル内の特殊文字をエスケープするには、バックスラッシュ（ `\` ）を使用します。                                                                                                                                                                                                                                                                                                                                  | 真実                                                                                                                                                                   |             |
| `--output-filename-template` | [Golangテンプレート](https://golang.org/pkg/text/template/#hdr-Arguments)の形式で表されるファイル名テンプレート<br/>`{{.DB}}` `{{.Table}}`引数`{{.Index}}`サポートする<br/>3つの引数は、データベース名、テーブル名、およびデータファイルのチャンクIDを表します。                                                                                                                                                                                             | `{{.DB}}.{{.Table}}.{{.Index}}`                                                                                                                                      |             |
| `--status-addr`              | Dumpling のサービス アドレス (Prometheus がメトリクスを取得して pprof デバッグを行うためのアドレスを含む)                                                                                                                                                                                                                                                                                                               | 「:8281」                                                                                                                                                              |             |
| `--tidb-mem-quota-query`     | Dumplingコマンドの1行でエクスポートするSQL文のメモリ制限。単位はバイトです。v4.0.10以降のバージョンでは、このパラメータを設定しない場合、TiDBはデフォルトで設定項目`mem-quota-query`の値をメモリ制限値として使用します。v4.0.10より前のバージョンでは、このパラメータ値はデフォルトで32 GBになります。                                                                                                                                                                                                      | 34359738368                                                                                                                                                          |             |
| `--params`                   | エクスポートするデータベース接続のセッション変数を指定します。必要な形式は`"character_set_client=latin1,character_set_connection=latin1"`です。                                                                                                                                                                                                                                                                            |                                                                                                                                                                      |             |
| `-c`または`--compress`          | DumplingによってエクスポートされたCSVおよびSQLデータとテーブル構造ファイルを圧縮します。以下`zstd`圧縮アルゴリズムをサポートしています： `gzip` `snappy`                                                                                                                                                                                                                                                                                     | 「」                                                                                                                                                                   |             |

## 出力ファイル名テンプレート {#output-filename-template}

`--output-filename-template`引数は、ファイル拡張子を除く出力ファイルの命名規則を定義します。3 の[Go `text/template`構文](https://golang.org/pkg/text/template/)列を受け入れます。

テンプレートでは次のフィールドを使用できます。

-   `.DB` : データベース名
-   `.Table` : テーブル名またはオブジェクト名
-   `.Index` : テーブルが複数のファイルに分割されている場合、ファイルの0から始まるシーケンス番号。ダンプされる部分を示します。例えば、 `{{printf "%09d" .Index}}` `.Index`先頭に0が付いた9桁の数字としてフォーマットすることを意味します。

データベース名やテーブル名には、ファイルシステムでは許可されていない特殊文字（ `/`など）が含まれている場合があります。この問題に対処するため、 Dumplingはこれらの特殊文字をパーセントエンコードする`fn`関数を提供しています。

-   U+0000からU+001F（制御文字）
-   `/` `*` `<` `"` `>` `:` `\` `?`
-   `.` (データベース名またはテーブル名の区切り文字)
-   `-` `-schema`の一部として使用される場合）

たとえば、 `--output-filename-template '{{fn .Table}}.{{printf "%09d" .Index}}'`使用すると、 Dumpling はテーブル`db.tbl:normal` `tbl%3Anormal.000000000.sql` 、 `tbl%3Anormal.000000001.sql`などの名前のファイルに書き込みます。

出力データファイルに加えて、スキーマファイルのファイル名を置き換えるために`--output-filename-template`定義できます。次の表はデフォルトの設定を示しています。

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

たとえば、 `--output-filename-template '{{define "table"}}{{fn .Table}}.$schema{{end}}{{define "data"}}{{fn .Table}}.{{printf "%09d" .Index}}{{end}}'`使用すると、 Dumpling はテーブル`db.tbl:normal`のスキーマを`tbl%3Anormal.$schema.sql`という名前のファイルに書き込み、データを`tbl%3Anormal.000000000.sql` 、 `tbl%3Anormal.000000001.sql`などのファイルに書き込みます。
