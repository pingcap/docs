---
title: Dumpling Overview
summary: Use the Dumpling tool to export data from TiDB.
---

# Dumpling を使用してデータをエクスポートする {#use-dumpling-to-export-data}

このドキュメントでは、データ エクスポート ツール - [Dumpling](https://github.com/pingcap/tidb/tree/master/dumpling)を紹介します。 Dumpling は、 TiDB/MySQL に保存されているデータを SQL または CSV データ ファイルとしてエクスポートし、論理的なフル バックアップまたはエクスポートの作成に使用できます。 Dumpling は、Amazon S3 へのデータのエクスポートもサポートしています。

<CustomContent platform="tidb">

`tiup install dumpling`を実行すると、 [TiUP](/tiup/tiup-overview.md)を使用してDumpling を取得できます。その後、 `tiup dumpling ...`使用してDumplingを実行できます。

Dumplingインストール パッケージはTiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDB ツールをダウンロード](/download-ecosystem-tools.md)を参照してください。

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

Dumplingの詳細な使用方法については、 `--help`オプションを使用するか、 [Dumplingのオプション一覧](#option-list-of-dumpling)を参照してください。

Dumplingを使用する場合は、実行中のクラスターで export コマンドを実行する必要があります。

<CustomContent platform="tidb">

TiDB は、必要に応じて選択して使用できる他のツールも提供します。

-   レイテンシーの影響を受けない SST ファイル (キーと値のペア) のバックアップまたは増分データのバックアップについては、 [BR](/br/backup-and-restore-overview.md)を参照してください。
-   増分データのリアルタイム バックアップについては、 [TiCDC](/ticdc/ticdc-overview.md)を参照してください。
-   エクスポートされたすべてのデータは、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用して TiDB にインポートして戻すことができます。

</CustomContent>

> **ノート：**
>
> PingCAP は以前、TiDB に固有の拡張機能を備えた[mydumper プロジェクト](https://github.com/maxbube/mydumper)のフォークを維持していました。このフォークはその後、Go で書き直された[Dumpling](/dumpling-overview.md)に置き換えられ、TiDB に固有のより多くの最適化をサポートしています。 mydumper の代わりにDumpling を使用することを強くお勧めします。
>
> Mydumper の詳細については、 [v4.0 Mydumper ドキュメント](https://docs.pingcap.com/tidb/v4.0/backup-and-restore-using-mydumper-lightning)を参照してください。

Mydumper と比較して、 Dumpling には次の改善点があります。

-   SQL や CSV など、複数の形式でのデータのエクスポートをサポートします。
-   データのフィルタリングを容易にする[テーブルフィルター](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md)機能をサポートします。
-   Amazon S3 クラウドstorageへのデータのエクスポートをサポートします。
-   TiDB に対してさらに最適化が行われます。
    -   単一のTiDB SQLステートメントのメモリ制限の構成をサポートします。
    -   Dumpling がPD に直接接続できる場合、 Dumpling はTiDB v4.0.0 以降のバージョンの TiDB GC 時間の自動調整をサポートします。
    -   TiDB の隠し列`_tidb_rowid`を使用して、単一のテーブルからの同時データ エクスポートのパフォーマンスを最適化します。
    -   TiDB の場合、値[`tidb_snapshot`](/read-historical-data.md#how-tidb-reads-data-from-history-versions)を設定して、データ バックアップの時点を指定できます。これにより、一貫性を確保するために`FLUSH TABLES WITH READ LOCK`を使用する代わりに、バックアップの一貫性が確保されます。

> **ノート：**
>
> Dumpling は、次のシナリオでは PD に接続できません。
>
> -   TiDB クラスターは Kubernetes 上で実行されています ( Dumpling自体が Kubernetes 環境内で実行されている場合を除く)。
> -   TiDB クラスターはTiDB Cloudで実行されています。
>
> このような場合、エクスポートの失敗を避けるために手動で[TiDB GC 時間を調整する](#manually-set-the-tidb-gc-time)する必要があります。

## TiDB または MySQL からデータをエクスポートする {#export-data-from-tidb-or-mysql}

### 必要な権限 {#required-privileges}

-   SELECT: テーブルをエクスポートするときに必要です。
-   RELOAD: `consistency flush`を使用する場合に必要です。この権限をサポートしているのは TiDB のみであることに注意してください。アップストリームが RDS データベースまたはマネージド サービスの場合、この権限は無視できます。
-   LOCK TABLES: `consistency lock`を使用する場合に必要です。この権限は、エクスポートするすべてのデータベースとテーブルに対して付与する必要があります。
-   REPLICATION CLIENT: メタデータをエクスポートしてデータのスナップショットを記録する場合に必要です。この権限はオプションであり、メタデータをエクスポートする必要がない場合は無視できます。

### SQL ファイルへのエクスポート {#export-to-sql-files}

このドキュメントでは、127.0.0.1:4000 ホストに TiDB インスタンスがあり、この TiDB インスタンスにはパスワードのない root ユーザーがいると想定しています。

Dumpling は、デフォルトでデータを SQL ファイルにエクスポートします。 `--filetype sql`フラグを追加して、データを SQL ファイルにエクスポートすることもできます。

{{< copyable "" >}}

```shell
dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  --filetype sql \
  -t 8 \
  -o /tmp/test \
  -r 200000 \
  -F 256MiB
```

上記のコマンドでは:

-   `-h` 、 `-P` 、および`-u`オプションは、それぞれアドレス、ポート、およびユーザーを意味します。認証にパスワードが必要な場合は、 `-p $YOUR_SECRET_PASSWORD`を使用してパスワードをDumplingに渡すことができます。

<CustomContent platform="tidb">

-   `-o` (または`--output` ) オプションは、ローカル ファイル パスまたは[外部storageURL](/br/backup-and-restore-storages.md#url-format)をサポートするstorageのエクスポート ディレクトリを指定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `-o` (または`--output` ) オプションは、ローカル ファイル パスまたは[外部storageURL](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages#url-format)をサポートするstorageのエクスポート ディレクトリを指定します。

</CustomContent>

-   `-t`オプションは、エクスポートのスレッド数を指定します。スレッドの数を増やすと、Dumplingの同時実行性とエクスポート速度が向上しますが、データベースのメモリ消費も増加します。そのため、あまり大きな数値を設定することはお勧めしません。通常は 64 未満です。
-   `-r`オプションは、1 つのファイル内の最大行数を指定します。このオプションを指定すると、 Dumpling はテーブル内の同時実行性を有効にして、エクスポートを高速化し、メモリ使用量を削減します。アップストリーム データベースが TiDB v3.0 以降のバージョンの場合、0 より大きい`-r`値は、TiDB リージョン情報が分割に使用され、特定の`-r`値が分割アルゴリズムに影響しないことを示します。アップストリーム データベースが MySQL で主キーが`int`型の場合、 `-r`指定するとテーブル内同時実行も有効になります。
-   `-F`オプションは、単一ファイルの最大サイズを指定するために使用されます (ここでの単位は`MiB`です`5GiB`や`8KB`などの入力も受け入れられます)。 TiDB Lightningを使用してこのファイルを TiDB インスタンスにロードする予定がある場合は、その値を 256 MiB 以下に保つことをお勧めします。

> **ノート：**
>
> 1 つのエクスポートされたテーブルのサイズが 10 GB を超える場合は、オプション`-r`および`-F`**を使用することを強くお勧めし**ます。

### CSV ファイルにエクスポート {#export-to-csv-files}

`--filetype csv`引数を追加することで、データを CSV ファイルにエクスポートできます。

データを CSV ファイルにエクスポートする場合、 `--sql <SQL>`を使用して SQL ステートメントでレコードをフィルタリングできます。たとえば、次のコマンドを使用して、 `id < 100` in `test.sbtest1`に一致するすべてのレコードをエクスポートできます。

{{< copyable "" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --filetype csv \
  --sql 'select * from `test`.`sbtest1` where id < 100' \
  -F 100MiB \
  --output-filename-template 'test.sbtest1.{{.Index}}'
```

上記のコマンドでは:

-   `--sql`オプションは、CSV ファイルへのエクスポートにのみ使用できます。上記のコマンドは、エクスポートするすべてのテーブルで`SELECT * FROM <table-name> WHERE id <100`ステートメントを実行します。テーブルに指定されたフィールドがない場合、エクスポートは失敗します。

<CustomContent platform="tidb">

-   `--sql`オプションを使用すると、Dumplingはエクスポートされたテーブルとスキーマの情報を取得できません。 `--output-filename-template`オプションを使用して CSV ファイルのファイル名形式を指定できます。これにより、後で[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してデータ ファイルをインポートすることが容易になります。たとえば、 `--output-filename-template='test.sbtest1.{{.Index}}'`エクスポートされた CSV ファイルの名前が`test.sbtest1.000000000`または`test.sbtest1.000000001`であることを指定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `--sql`オプションを使用すると、Dumplingはエクスポートされたテーブルとスキーマの情報を取得できません。 `--output-filename-template`オプションを使用して、CSV ファイルのファイル名形式を指定できます。たとえば、 `--output-filename-template='test.sbtest1.{{.Index}}'`エクスポートされた CSV ファイルの名前が`test.sbtest1.000000000`または`test.sbtest1.000000001`であることを指定します。

</CustomContent>

-   `--csv-separator`や`--csv-delimiter`などのオプションを使用して、CSV ファイル形式を構成できます。詳細は[Dumplingのオプション一覧](#option-list-of-dumpling)を参照してください。

> **ノート：**
>
> Dumplingでは、*文字列*と<em>キーワードは</em>区別されません。インポートされたデータがブール型の場合、値`true`は`1`に変換され、値`false`は`0`に変換されます。

### エクスポートされたデータ ファイルを圧縮する {#compress-the-exported-data-files}

`--compress <format>`オプションを使用して、 Dumplingによってエクスポートされた CSV および SQL データとテーブル構造ファイルを圧縮できます。このパラメーターは、次の圧縮アルゴリズムをサポートしています: `gzip` 、 `snappy` 、および`zstd` 。圧縮はデフォルトで無効になっています。

-   このオプションは、個々のデータおよびテーブル構造ファイルのみを圧縮します。フォルダー全体を圧縮して、単一の圧縮パッケージを生成することはできません。
-   このオプションはディスク容量を節約できますが、エクスポート速度が遅くなり、CPU 消費が増加します。エクスポート速度が重要なシナリオでは、このオプションを慎重に使用してください。
-   TiDB Lightning v6.5.0 以降のバージョンでは、追加の構成なしでDumplingによってエクスポートされた圧縮ファイルをデータ ソースとして使用できます。

### エクスポートされたファイルの形式 {#format-of-exported-files}

-   `metadata` : エクスポートされたファイルの開始時刻とマスター バイナリ ログの位置。

    {{< copyable "" >}}

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

-   `{schema}-schema-create.sql` : スキーマの作成に使用される SQL ファイル

    {{< copyable "" >}}

    ```shell
    cat test-schema-create.sql
    ```

    ```shell
    CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
    ```

-   `{schema}.{table}-schema.sql` : テーブルの作成に使用される SQL ファイル

    {{< copyable "" >}}

    ```shell
    cat test.t1-schema.sql
    ```

    ```shell
    CREATE TABLE `t1` (
      `id` int(11) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
    ```

-   `{schema}.{table}.{0001}.{sql|csv}` : 日付ソース ファイル

    {{< copyable "" >}}

    ```shell
    cat test.t1.0.sql
    ```

    ```shell
    /*!40101 SET NAMES binary*/;
    INSERT INTO `t1` VALUES
    (1);
    ```

-   `*-schema-view.sql` , `*-schema-trigger.sql` , `*-schema-post.sql` : その他のエクスポートされたファイル

### データを Amazon S3 クラウドstorageにエクスポートする {#export-data-to-amazon-s3-cloud-storage}

v4.0.8 以降、 Dumpling はクラウド ストレージへのデータのエクスポートをサポートしています。データを Amazon S3 にバックアップする必要がある場合は、 `-o`パラメータで Amazon S3storageパスを指定する必要があります。

指定されたリージョンに Amazon S3 バケットを作成する必要があります ( [Amazon ドキュメント - S3 バケットを作成する方法](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)を参照)。バケットにフォルダーも作成する必要がある場合は、 [Amazon ドキュメント - フォルダーの作成](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html)を参照してください。

Amazon S3 バックエンドstorageへのアクセス権限を持つアカウントの`SecretKey`と`AccessKey`環境変数としてDumplingノードに渡します。

{{< copyable "" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

<CustomContent platform="tidb">

Dumpling は、 `~/.aws/credentials`からの資格情報ファイルの読み取りもサポートしています。 Dumpling の構成の詳細については、 [外部ストレージ](/br/backup-and-restore-storages.md)の構成を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

Dumpling は、 `~/.aws/credentials`からの資格情報ファイルの読み取りもサポートしています。 Dumplingを使用して Amazon S3 にデータをエクスポートするためのパラメーターは、 BRで使用されるパラメーターと同じです。パラメーターの詳細については、 [外部storageURL](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages#url-format)を参照してください。

</CustomContent>

{{< copyable "" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -r 200000 \
  -o "s3://${Bucket}/${Folder}"
```

### エクスポートされたデータをフィルタリングする {#filter-the-exported-data}

#### <code>--where</code>オプションを使用してデータをフィルタリングする {#use-the-code-where-code-option-to-filter-data}

Dumpling はデフォルトで、システム データベース ( `mysql` 、 `sys` 、 `INFORMATION_SCHEMA` 、 `PERFORMANCE_SCHEMA` 、 `METRICS_SCHEMA` 、および`INSPECTION_SCHEMA`を含む) を除くすべてのデータベースをエクスポートします。 `--where <SQL where expression>`使用して、エクスポートするレコードを選択できます。

{{< copyable "" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --where "id < 100"
```

上記のコマンドは、各テーブルから`id < 100`に一致するデータをエクスポートします。 `--where`パラメータを`--sql`と一緒に使用できないことに注意してください。

#### <code>--filter</code>オプションを使用してデータをフィルタリングする {#use-the-code-filter-code-option-to-filter-data}

Dumpling は、 `--filter`オプションでテーブル フィルターを指定することにより、特定のデータベースまたはテーブルをフィルター処理できます。テーブル フィルターの構文は`.gitignore`の構文と似ています。詳細については、 [テーブル フィルター](/table-filter.md)を参照してください。

{{< copyable "" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  -r 200000 \
  --filter "employees.*" \
  --filter "*.WorkOrder"
```

上記のコマンドは、 `employees`データベース内のすべてのテーブルと、すべてのデータベース内の`WorkOrder`テーブルをエクスポートします。

#### <code>-B</code>または<code>-T</code>オプションを使用してデータをフィルタリングする {#use-the-code-b-code-or-code-t-code-option-to-filter-data}

Dumpling は、オプション`-B`を使用して特定のデータベースをエクスポートしたり、オプション`-T`を使用して特定のテーブルをエクスポートしたりすることもできます。

> **ノート：**
>
> -   オプション`--filter`とオプション`-T`を同時に使用することはできません。
> -   `-T`オプションは、 `database-name.table-name`のような完全な形式の入力のみを受け入れることができ、テーブル名のみの入力は受け入れられません。例:Dumplingは`-T WorkOrder`を認識できません。

例:

-   `-B employees` `employees`データベースをエクスポートします。
-   `-T employees.WorkOrder` `employees.WorkOrder`テーブルをエクスポートします。

### 同時実行によるエクスポート効率の向上 {#improve-export-efficiency-through-concurrency}

エクスポートされたファイルは、デフォルトで`./export-<current local time>`ディレクトリに保存されます。一般的に使用されるオプションは次のとおりです。

-   `-t`オプションは、エクスポートのスレッド数を指定します。スレッドの数を増やすと、Dumplingの同時実行性とエクスポート速度が向上しますが、データベースのメモリ消費も増加します。そのため、あまり大きな数値を設定することはお勧めしません。
-   `-r`オプションは、1 つのファイルの最大レコード数 (またはデータベース内の行数) を指定します。 Dumplingを有効にすると、テーブルの同時実行性が有効になり、大きなテーブルのエクスポート速度が向上します。アップストリーム データベースが TiDB v3.0 以降のバージョンの場合、0 より大きい`-r`値は、TiDB リージョン情報が分割に使用され、特定の`-r`値が分割アルゴリズムに影響しないことを示します。アップストリーム データベースが MySQL で主キーが`int`型の場合、 `-r`指定するとテーブル内同時実行も有効になります。
-   `--compress <format>`オプションは、ダンプの圧縮形式を指定します。次の圧縮アルゴリズムをサポートしています: `gzip` 、 `snappy` 、および`zstd` 。storageがボトルネックである場合、またはstorage容量が懸念される場合、このオプションはデータのダンプを高速化できます。欠点は、CPU 使用率の増加です。各ファイルは個別に圧縮されます。

上記のオプションを指定すると、 Dumplingのデータ エクスポート速度が向上します。

### Dumpling のデータ整合性オプションを調整する {#adjust-dumpling-s-data-consistency-options}

> **ノート：**
>
> データ整合性オプションのデフォルト値は`auto`です。ほとんどのシナリオでは、 Dumplingの既定のデータ整合性オプションを調整する必要はありません。

Dumpling は`--consistency <consistency level>`オプションを使用して、「一貫性保証」のためにデータをエクスポートする方法を制御します。一貫性のためにスナップショットを使用する場合、 `--snapshot`オプションを使用して、バックアップするタイムスタンプを指定できます。次のレベルの一貫性を使用することもできます。

-   `flush` : [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock)を使用して、レプリカ データベースの DML および DDL 操作を一時的に中断し、バックアップ接続のグローバルな一貫性を確保し、 binlog位置 (POS) 情報を記録します。すべてのバックアップ接続がトランザクションを開始した後、ロックは解放されます。オフピーク時または MySQL レプリカ データベースでフル バックアップを実行することをお勧めします。
-   `snapshot` : 指定されたタイムスタンプの一貫したスナップショットを取得してエクスポートします。
-   `lock` : エクスポートするすべてのテーブルに読み取りロックを追加します。
-   `none` : 一貫性を保証しません。
-   `auto` : MySQL には`flush` 、TiDB には`snapshot`を使用します。

すべてが完了すると、エクスポートされたファイルが`/tmp/test`に表示されます。

{{< copyable "" >}}

```shell
ls -lh /tmp/test | awk '{print $5 "\t" $9}'
```

```
140B  metadata
66B   test-schema-create.sql
300B  test.sbtest1-schema.sql
190K  test.sbtest1.0.sql
300B  test.sbtest2-schema.sql
190K  test.sbtest2.0.sql
300B  test.sbtest3-schema.sql
190K  test.sbtest3.0.sql
```

### TiDB の履歴データのスナップショットをエクスポートする {#export-historical-data-snapshots-of-tidb}

Dumpling は`--snapshot`オプション指定で特定の[tidb_snapshot](/read-historical-data.md#how-tidb-reads-data-from-history-versions)のデータをエクスポートできます。

`--snapshot`オプションは、TSO ( `SHOW MASTER STATUS`コマンドによる`Position`フィールド出力) または`datetime`データ型の有効時間 ( `YYYY-MM-DD hh:mm:ss`の形式) に設定できます。次に例を示します。

{{< copyable "" >}}

```shell
./dumpling --snapshot 417773951312461825
./dumpling --snapshot "2020-07-02 17:12:45"
```

TSO が`417773951312461825`で時刻が`2020-07-02 17:12:45`のときの TiDB ヒストリカル データ スナップショットがエクスポートされます。

### 大きなテーブルのエクスポートのメモリ使用量を制御する {#control-the-memory-usage-of-exporting-large-tables}

Dumplingが TiDB から大きな単一テーブルをエクスポートしている場合、エクスポートされたデータのサイズが大きすぎるためにメモリ不足 (OOM) が発生し、接続が中止され、エクスポートが失敗することがあります。次のパラメータを使用して、TiDB のメモリ使用量を削減できます。

-   エクスポートするデータをチャンクに分割するには、 `-r`を設定します。これにより、TiDB のデータ スキャンのメモリオーバーヘッドが削減され、同時テーブル データ ダンプが可能になり、エクスポートの効率が向上します。アップストリーム データベースが TiDB v3.0 以降のバージョンの場合、0 より大きい`-r`値は、TiDB リージョン情報が分割に使用され、特定の`-r`値が分割アルゴリズムに影響しないことを示します。
-   `--tidb-mem-quota-query`の値を`8589934592` (8 GB) 以下に減らします。 `--tidb-mem-quota-query` TiDB での単一のクエリ ステートメントのメモリ使用量を制御します。
-   `--params "tidb_distsql_scan_concurrency=5"`パラメータを調整します。 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)は、TiDB でのスキャン操作の同時実行性を制御するセッション変数です。

### TiDB GC 時間を手動で設定する {#manually-set-the-tidb-gc-time}

TiDB からデータをエクスポートする (1 TB を超える) 場合、TiDB のバージョンが v4.0.0 以降で、かつDumpling がTiDB クラスターの PD アドレスにアクセスできる場合、 Dumpling は元のクラスターに影響を与えずに GC 時間を自動的に延長します。

ただし、次のいずれかのシナリオでは、 Dumpling はGC 時間を自動的に調整できません。

-   データ サイズが非常に大きい (1 TB を超える)。
-   Dumpling は、たとえば、TiDB クラスターがTiDB Cloud上にある場合、またはDumplingから分離された Kubernetes 上にある場合、PD に直接接続することはできません。

このようなシナリオでは、事前に GC 時間を手動で延長して、エクスポート プロセス中の GC によるエクスポートの失敗を回避する必要があります。

GC 時間を手動で調整するには、次の SQL ステートメントを使用します。

```sql
SET GLOBAL tidb_gc_life_time = '720h';
```

Dumplingの終了後、エクスポートが成功したかどうかに関係なく、GC 時間を元の値に戻す必要があります (デフォルト値は`10m`です)。

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

## Dumplingのオプション一覧 {#option-list-of-dumpling}

| オプション                        | 使用法                                                                                                                                                                                                                                                | デフォルト値                                                                                                                                                                  |             |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `-V`または`--version`           | Dumplingバージョンを出力し、直接終了します                                                                                                                                                                                                                          |                                                                                                                                                                         |             |
| `-B`または`--database`          | 指定したデータベースをエクスポートする                                                                                                                                                                                                                                |                                                                                                                                                                         |             |
| `-T`または`--tables-list`       | 指定したテーブルをエクスポートする                                                                                                                                                                                                                                  |                                                                                                                                                                         |             |
| `-f`または`--filter`            | フィルター パターンに一致するテーブルをエクスポートします。フィルター構文については、 [テーブルフィルター](/table-filter.md)を参照してください。                                                                                                                                                                | `[\*.\*,!/^(mysql&#124;sys&#124;INFORMATION_SCHEMA&#124;PERFORMANCE_SCHEMA&#124;METRICS_SCHEMA&#124;INSPECTION_SCHEMA)$/.\*]` (システム スキーマを除くすべてのデータベースまたはテーブルをエクスポートします) |             |
| `--case-sensitive`           | table-filter で大文字と小文字を区別するかどうか                                                                                                                                                                                                                     | false (大文字と小文字を区別しない)                                                                                                                                                   |             |
| `-h`または`--host`              | 接続されたデータベース ホストの IP アドレス                                                                                                                                                                                                                           | 「127.0.0.1」                                                                                                                                                             |             |
| `-t`または`--threads`           | 同時バックアップ スレッドの数                                                                                                                                                                                                                                    | 4                                                                                                                                                                       |             |
| `-r`または`--rows`              | 指定された行数でテーブルを行に分割します (通常、大きなテーブルを複数のファイルに分割する同時操作に適用されます。アップストリーム データベースが TiDB v3.0 以降のバージョンである場合、0 より大きい`-r`値は、TiDB リージョンが情報は分割に使用され、特定の`-r`値は分割アルゴリズムに影響しません。                                                                                    |                                                                                                                                                                         |             |
| `-L`または`--logfile`           | ログ出力アドレス。空の場合、コンソールにログが出力されます                                                                                                                                                                                                                      | &quot;&quot;                                                                                                                                                            |             |
| `--loglevel`                 | ログレベル {debug,info,warn,error,dpanic, panic,fatal}                                                                                                                                                                                                  | &quot;情報&quot;                                                                                                                                                          |             |
| `--logfmt`                   | ログ出力形式 {text,json}                                                                                                                                                                                                                                 | &quot;文章&quot;                                                                                                                                                          |             |
| `-d`または`--no-data`           | データをエクスポートしない (スキーマのみがエクスポートされるシナリオに適しています)                                                                                                                                                                                                        |                                                                                                                                                                         |             |
| `--no-header`                | ヘッダーを生成せずにテーブルの CSV ファイルをエクスポートする                                                                                                                                                                                                                  |                                                                                                                                                                         |             |
| `-W`または`--no-views`          | ビューをエクスポートしない                                                                                                                                                                                                                                      | 真実                                                                                                                                                                      |             |
| `-m`または`--no-schemas`        | データのみがエクスポートされたスキーマをエクスポートしないでください                                                                                                                                                                                                                 |                                                                                                                                                                         |             |
| `-s`または`--statement-size`    | `INSERT`ステートメントのサイズを制御します。単位はバイトです                                                                                                                                                                                                                 |                                                                                                                                                                         |             |
| `-F`または`--filesize`          | 分割されたテーブルのファイル サイズ。単位は`128B` 、 `64KiB` 、 `32MiB` 、および`1.5GiB`のように指定する必要があります。                                                                                                                                                                      |                                                                                                                                                                         |             |
| `--filetype`                 | エクスポートされるファイルの種類 (csv/sql)                                                                                                                                                                                                                         | &quot;SQL&quot;                                                                                                                                                         |             |
| `-o`または`--output`            | エクスポートされたローカル ファイルのパスまたは[外部storageURL](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages#url-format)                                                                                                                                | &quot;./export-${time}&quot;                                                                                                                                            |             |
| `-S`または`--sql`               | 指定された SQL ステートメントに従ってデータをエクスポートします。このコマンドは、同時エクスポートをサポートしていません。                                                                                                                                                                                    |                                                                                                                                                                         |             |
| `--consistency`              | フラッシュ: ダンプの前に FTWRL を使用します<br/>スナップショット: TSO の特定のスナップショットの TiDB データをダンプします<br/>lock: ダンプするすべてのテーブルで`lock tables read`を実行します<br/>none: 一貫性を保証できないロックを追加せずにダンプします。<br/> auto: MySQL には --consistency フラッシュを使用します。 --consistency スナップショットを TiDB に使用する | 「オート」                                                                                                                                                                   |             |
| `--snapshot`                 | スナップショット TSO。 `consistency=snapshot`のときのみ有効                                                                                                                                                                                                        |                                                                                                                                                                         |             |
| `--where`                    | `where`条件でテーブル バックアップの範囲を指定します                                                                                                                                                                                                                     |                                                                                                                                                                         |             |
| `-p`または`--password`          | 接続されたデータベース ホストのパスワード                                                                                                                                                                                                                              |                                                                                                                                                                         |             |
| `-P`または`--port`              | 接続されたデータベース ホストのポート                                                                                                                                                                                                                                | 4000                                                                                                                                                                    |             |
| `-u`または`--user`              | 接続されたデータベース ホストのユーザー名                                                                                                                                                                                                                              | &quot;根&quot;                                                                                                                                                           |             |
| `--dump-empty-database`      | 空のデータベースの`CREATE DATABASE`ステートメントをエクスポートします                                                                                                                                                                                                        | 真実                                                                                                                                                                      |             |
| `--ca`                       | TLS接続用の認証局ファイルのアドレス                                                                                                                                                                                                                                |                                                                                                                                                                         |             |
| `--cert`                     | TLS接続用のクライアント証明書ファイルのアドレス                                                                                                                                                                                                                          |                                                                                                                                                                         |             |
| `--key`                      | TLS接続用のクライアント秘密鍵ファイルのアドレス                                                                                                                                                                                                                          |                                                                                                                                                                         |             |
| `--csv-delimiter`            | CSVファイルの文字型変数の区切り文字                                                                                                                                                                                                                                | &#39;&quot;&#39;                                                                                                                                                        |             |
| `--csv-separator`            | CSV ファイルの各値の区切り記号。デフォルトの「,」を使用することはお勧めしません。 「|+|」を使用することをお勧めしますまたは他の珍しい文字の組み合わせ                                                                                                                                                                    | &#39;、&#39;                                                                                                                                                             | &#39;、&#39; |
| `--csv-null-value`           | CSV ファイルでの null 値の表現                                                                                                                                                                                                                               | 「\N」                                                                                                                                                                    |             |
| `--escape-backslash`         | バックスラッシュ ( `\` ) を使用して、エクスポート ファイル内の特殊文字をエスケープします                                                                                                                                                                                                  | 真実                                                                                                                                                                      |             |
| `--output-filename-template` | [golang テンプレート](https://golang.org/pkg/text/template/#hdr-Arguments)の形式で表されるファイル名テンプレート<br/>`{{.DB}}` 、 `{{.Table}}` 、および`{{.Index}}`引数をサポート<br/>3 つの引数は、データ ファイルのデータベース名、テーブル名、およびチャンク ID を表します。                                                  | &#39;{{.DB}}.{{.Table}}.{{.Index}}&#39;                                                                                                                                 |             |
| `--status-addr`              | Dumpling のサービス アドレス (Prometheus がメトリクスをプルし、デバッグを pprof するためのアドレスを含む)                                                                                                                                                                               | &quot;:8281&quot;                                                                                                                                                       |             |
| `--tidb-mem-quota-query`     | Dumplingコマンドの 1 行で SQL ステートメントをエクスポートする際のメモリ制限で、単位はバイトです。 v4.0.10 以降のバージョンでは、このパラメータを設定しない場合、TiDB はデフォルトで`mem-quota-query`構成項目の値をメモリ制限値として使用します。 v4.0.10 より前のバージョンでは、パラメーター値のデフォルトは 32 GB です。                                                      | 34359738368                                                                                                                                                             |             |
| `--params`                   | エクスポートするデータベースの接続のセッション変数を指定します。必要な形式は`"character_set_client=latin1,character_set_connection=latin1"`です                                                                                                                                            |                                                                                                                                                                         |             |
| `-c`または`--compress`          | Dumplingによってエクスポートされた CSV および SQL データとテーブル構造ファイルを圧縮します。次の圧縮アルゴリズムがサポートされています: `gzip` 、 `snappy` 、および`zstd` 。                                                                                                                                       | &quot;&quot;                                                                                                                                                            |             |
