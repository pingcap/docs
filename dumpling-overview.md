---
title: Dumpling Overview
summary: Use the Dumpling tool to export data from TiDB.
---

# Dumpling を使用してデータをエクスポートする {#use-dumpling-to-export-data}

このドキュメントでは、データ エクスポート ツール[<a href="https://github.com/pingcap/dumpling">Dumpling</a>](https://github.com/pingcap/dumpling)について紹介します。 Dumpling は、 TiDB/MySQL に保存されているデータを SQL または CSV データ ファイルとしてエクスポートし、論理完全バックアップまたはエクスポートの作成に使用できます。 Dumpling は、Amazon S3 へのデータのエクスポートもサポートしています。

<CustomContent platform="tidb">

`tiup install dumpling`を実行すると、 [<a href="/tiup/tiup-overview.md">TiUP</a>](/tiup/tiup-overview.md)使用してDumplingを入手できます。その後、 `tiup dumpling ...`使用してDumplingを実行できます。

Dumplingインストール パッケージは、 TiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [<a href="/download-ecosystem-tools.md">TiDB ツールをダウンロード</a>](/download-ecosystem-tools.md)を参照してください。

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

Dumplingの詳細な使用方法については、 `--help`オプションを使用するか、 [<a href="#option-list-of-dumpling">Dumplingのオプション一覧</a>](#option-list-of-dumpling)を参照してください。

Dumplingを使用する場合は、実行中のクラスターでエクスポート コマンドを実行する必要があります。

<CustomContent platform="tidb">

TiDB は、必要に応じて使用できる他のツールも提供します。

-   SST ファイル (キーと値のペア) のバックアップ、またはレイテンシーの影響を受けない増分データのバックアップについては、 [<a href="/br/backup-and-restore-tool.md">BR</a>](/br/backup-and-restore-tool.md)を参照してください。
-   増分データのリアルタイム バックアップについては、 [<a href="/ticdc/ticdc-overview.md">TiCDC</a>](/ticdc/ticdc-overview.md)を参照してください。
-   エクスポートされたすべてのデータは、 [<a href="/tidb-lightning/tidb-lightning-overview.md">TiDB Lightning</a>](/tidb-lightning/tidb-lightning-overview.md)使用して TiDB にインポートして戻すことができます。

</CustomContent>

> **ノート：**
>
> PingCAP は以前、TiDB に固有の拡張機能を備えた[<a href="https://github.com/maxbube/mydumper">マイダンパープロジェクト</a>](https://github.com/maxbube/mydumper)のフォークを維持していました。その後、このフォークは Go で書き直された[<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md)に置き換えられ、TiDB に固有のさらなる最適化をサポートしています。 mydumper の代わりにDumpling を使用することを強くお勧めします。
>
> Mydumper の詳細については、 [<a href="https://docs.pingcap.com/tidb/v4.0/backup-and-restore-using-mydumper-lightning">v4.0 Mydumper ドキュメント</a>](https://docs.pingcap.com/tidb/v4.0/backup-and-restore-using-mydumper-lightning)を参照してください。

Mydumper と比較して、 Dumplingには次の改良点があります。

-   SQL や CSV などの複数の形式でのデータのエクスポートをサポートします。
-   データのフィルタリングを容易にする[<a href="https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md">テーブルフィルター</a>](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md)機能をサポートします。
-   Amazon S3 クラウドstorageへのデータのエクスポートをサポートします。
-   TiDB に対してさらに最適化が行われています。
    -   単一のTiDB SQLステートメントのメモリ制限の構成をサポートします。
    -   TiDB v4.0.0 以降のバージョンの TiDB GC 時間の自動調整をサポートします。
    -   TiDB の非表示列`_tidb_rowid`を使用して、単一テーブルからの同時データ エクスポートのパフォーマンスを最適化します。
    -   TiDB の場合、値[<a href="/read-historical-data.md#how-tidb-reads-data-from-history-versions">`tidb_snapshot`</a>](/read-historical-data.md#how-tidb-reads-data-from-history-versions)を設定してデータ バックアップの時点を指定できます。一貫性を確保するために`FLUSH TABLES WITH READ LOCK`を使用するのではなく、これによりバックアップの一貫性が確保されます。

## TiDB または MySQL からデータをエクスポートする {#export-data-from-tidb-or-mysql}

### 必要な権限 {#required-privileges}

-   選択する
-   リロード
-   ロックテーブル
-   レプリケーションクライアント
-   プロセス

### SQL ファイルにエクスポート {#export-to-sql-files}

このドキュメントでは、127.0.0.1:4000 ホスト上に TiDB インスタンスが存在し、この TiDB インスタンスにはパスワードのない root ユーザーがいることを前提としています。

Dumpling は、デフォルトでデータを SQL ファイルにエクスポートします。 `--filetype sql`フラグを追加して、データを SQL ファイルにエクスポートすることもできます。

{{< copyable "" >}}

```shell
dumpling -u root -P 4000 -h 127.0.0.1 --filetype sql -t 8 -o /tmp/test -r 200000 -F 256MiB
```

上記のコマンドでは次のようになります。

-   `-h` 、 `-p` 、および`-u`オプションは、それぞれアドレス、ポート、およびユーザーを意味します。認証にパスワードが必要な場合は、 `-p $YOUR_SECRET_PASSWORD`を使用してパスワードをDumplingに渡すことができます。
-   `-o`オプションは、ローカル ファイル パスまたは[<a href="/br/backup-and-restore-storages.md">外部storageのURL</a>](/br/backup-and-restore-storages.md)をサポートするstorageのエクスポート ディレクトリを指定します。
-   `-t`オプションは、エクスポートのスレッド数を指定します。スレッドの数を増やすと、 Dumplingの同時実行性とエクスポート速度が向上し、データベースのメモリ消費量も増加します。したがって、あまり大きな数値を設定することはお勧めできません。通常は 64 未満です。
-   `-r`オプションは、単一ファイル内の最大行数を指定します。このオプションを指定すると、 Dumplingによりテーブル内の同時実行が有効になり、エクスポートが高速化され、メモリ使用量が削減されます。アップストリーム データベースが TiDB v3.0 以降のバージョンの場合、このパラメータの値が 0 より大きい場合、TiDB リージョン情報が分割に使用され、ここで指定した値が有効でなくなることを示します。
-   `-F`オプションは、単一ファイルの最大サイズを指定するために使用されます (ここでの単位は`MiB`です`5GiB`や`8KB`などの入力も受け入れられます)。 TiDB Lightningを使用してこのファイルを TiDB インスタンスにロードする予定がある場合は、その値を 256 MiB 以下に保つことをお勧めします。

> **ノート：**
>
> エクスポートされる 1 つのテーブルのサイズが 10 GB を超える場合は、 `-r`および`-F`オプション**を使用することを強くお勧めし**ます。

### CSV ファイルにエクスポート {#export-to-csv-files}

引数`--filetype csv`を追加すると、データを CSV ファイルにエクスポートできます。

データを CSV ファイルにエクスポートする場合、 `--sql <SQL>`を使用して SQL ステートメントでレコードをフィルターできます。たとえば、次のコマンドを使用して、 `test.sbtest1`中`id < 100`に一致するすべてのレコードをエクスポートできます。

{{< copyable "" >}}

```shell
./dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test --filetype csv --sql 'select * from `test`.`sbtest1` where id < 100' -F 100MiB --output-filename-template 'test.sbtest1.{{.Index}}'
```

上記のコマンドでは次のようになります。

-   `--sql`オプションは、CSV ファイルへのエクスポートにのみ使用できます。上記のコマンドは、エクスポートされるすべてのテーブルに対して`SELECT * FROM <table-name> WHERE id <100`ステートメントを実行します。テーブルに指定されたフィールドがない場合、エクスポートは失敗します。
-   `--sql`オプションを使用すると、 Dumpling はエクスポートされたテーブルとスキーマの情報を取得できません。 `--output-filename-template`オプションを使用して CSV ファイルのファイル名形式を指定できます。これにより、その後[<a href="/tidb-lightning/tidb-lightning-overview.md">TiDB Lightning</a>](/tidb-lightning/tidb-lightning-overview.md)を使用してデータ ファイルをインポートすることが容易になります。たとえば、 `--output-filename-template='test.sbtest1.{{.Index}}'`エクスポートされた CSV ファイルの名前が`test.sbtest1.000000000`または`test.sbtest1.000000001`であることを指定します。
-   `--csv-separator`や`--csv-delimiter`のようなオプションを使用して、CSV ファイル形式を構成できます。詳細は[<a href="#option-list-of-dumpling">Dumplingオプション一覧</a>](#option-list-of-dumpling)を参照してください。

> **ノート：**
>
> Dumplingでは*文字列*と*キーワードは*区別されません。インポートされたデータが Boolean 型の場合、値`true`は`1`に変換され、値`false`は`0`に変換されます。

### エクスポートされるファイルの形式 {#format-of-exported-files}

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

-   `{schema}.{table}.{0001}.{sql|csv` }: 日付ソース ファイル

    {{< copyable "" >}}

    ```shell
    cat test.t1.0.sql
    ```

    ```shell
    /*!40101 SET NAMES binary*/;
    INSERT INTO `t1` VALUES
    (1);
    ```

-   `*-schema-view.sql` 、 `*-schema-trigger.sql` 、 `*-schema-post.sql` : その他のエクスポートされたファイル

### データを Amazon S3 クラウドstorageにエクスポートする {#export-data-to-amazon-s3-cloud-storage}

v4.0.8 以降、 Dumpling はクラウド ストレージへのデータのエクスポートをサポートします。データを Amazon S3 にバックアップする必要がある場合は、 `-o`パラメータで Amazon S3storageパスを指定する必要があります。

指定されたリージョンに Amazon S3 バケットを作成する必要があります ( [<a href="https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html">Amazon ドキュメント - S3 バケットの作成方法</a>](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)を参照)。バケット内にフォルダーを作成する必要がある場合は、 [<a href="https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html">Amazon ドキュメント - フォルダーの作成</a>](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html)を参照してください。

Amazon S3 バックエンドstorageにアクセスする権限を持つアカウントの`SecretKey`と`AccessKey`環境変数としてDumplingノードに渡します。

{{< copyable "" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

Dumpling は、資格情報ファイルの`~/.aws/credentials`からの読み取りもサポートしています。 Dumpling の構成の詳細については、 [<a href="/br/backup-and-restore-storages.md">外部ストレージ</a>](/br/backup-and-restore-storages.md)の構成を参照してください。

Dumplingを使用してデータをバックアップする場合は、S3storageの領域 (たとえば、 `ap-northeast-1` ) を意味する`--s3.region`パラメータを明示的に指定します。

{{< copyable "" >}}

```shell
./dumpling -u root -P 4000 -h 127.0.0.1 -r 200000 -o "s3://${Bucket}/${Folder}" --s3.region "${region}"
```

### エクスポートされたデータをフィルタリングする {#filter-the-exported-data}

#### <code>--where</code>オプションを使用してデータをフィルタリングします {#use-the-code-where-code-option-to-filter-data}

デフォルトでは、 Dumpling はシステム データベース ( `mysql` 、 `sys` 、 `INFORMATION_SCHEMA` 、 `PERFORMANCE_SCHEMA` 、 `METRICS_SCHEMA` 、および`INSPECTION_SCHEMA`を含む) を除くすべてのデータベースをエクスポートします。 `--where <SQL where expression>`使用して、エクスポートするレコードを選択できます。

{{< copyable "" >}}

```shell
./dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test --where "id < 100"
```

上記のコマンドは、各テーブルから`id < 100`に一致するデータをエクスポートします。 `--where`パラメータを`--sql`と一緒に使用することはできないことに注意してください。

#### <code>--filter</code>オプションを使用してデータをフィルタリングします。 {#use-the-code-filter-code-option-to-filter-data}

Dumpling は、 `--filter`オプションでテーブル フィルターを指定することで、特定のデータベースまたはテーブルをフィルターできます。テーブル フィルターの構文は`.gitignore`の構文と似ています。詳細は[<a href="/table-filter.md">テーブルフィルター</a>](/table-filter.md)を参照してください。

{{< copyable "" >}}

```shell
./dumpling -u root -P 4000 -h 127.0.0.1 -o /tmp/test -r 200000 --filter "employees.*" --filter "*.WorkOrder"
```

上記のコマンドは、 `employees`データベースのすべてのテーブルと、すべてのデータベースの`WorkOrder`テーブルをエクスポートします。

#### <code>-B</code>または<code>-T</code>オプションを使用してデータをフィルタリングします。 {#use-the-code-b-code-or-code-t-code-option-to-filter-data}

Dumpling は、 `-B`オプションを使用して特定のデータベースをエクスポートしたり、 `-T`オプションを使用して特定のテーブルをエクスポートしたりすることもできます。

> **ノート：**
>
> -   `--filter`オプションと`-T`オプションを同時に使用することはできません。
> -   `-T`オプションは`database-name.table-name`のような完全な形式の入力のみを受け入れることができ、テーブル名のみの入力は受け入れられません。例:Dumplingは`-T WorkOrder`を認識できません。

例:

-   `-B employees` `employees`データベースをエクスポートします。
-   `-T employees.WorkOrder` `employees.WorkOrder`テーブルをエクスポートします。

### 同時実行によるエクスポート効率の向上 {#improve-export-efficiency-through-concurrency}

エクスポートされたファイルは、デフォルトでは`./export-<current local time>`ディレクトリに保存されます。一般的に使用されるオプションは次のとおりです。

-   `-t`オプションは、エクスポートのスレッド数を指定します。スレッドの数を増やすと、 Dumplingの同時実行性とエクスポート速度が向上し、データベースのメモリ消費量も増加します。したがって、あまり大きな数値を設定することはお勧めできません。
-   `-r`オプションは、1 つのファイルの最大レコード数 (またはデータベース内の行数) を指定します。 Dumplingを有効にすると、テーブルの同時実行が有効になり、大きなテーブルのエクスポート速度が向上します。アップストリーム データベースが TiDB v3.0 以降のバージョンの場合、このパラメータの値が 0 より大きい場合、TiDB リージョン情報が分割に使用され、ここで指定した値が有効でなくなることを示します。
-   `--compress gzip`オプションを使用すると、ダンプを圧縮できます。これは、storageがボトルネックになっている場合、またはstorage容量が懸念される場合に、データのダンプを高速化するのに役立ちます。この欠点は、CPU 使用率が増加することです。各ファイルは個別に圧縮されます。

上記のオプションを指定すると、 Dumpling のデータ エクスポートの速度が速くなります。

### Dumpling のデータ整合性オプションを調整する {#adjust-dumpling-s-data-consistency-options}

> **ノート：**
>
> データ整合性オプションのデフォルト値は`auto`です。ほとんどのシナリオでは、 Dumplingのデフォルトのデータ整合性オプションを調整する必要はありません。

Dumpling は`--consistency <consistency level>`オプションを使用して、「一貫性保証」のためにデータをエクスポートする方法を制御します。整合性のためにスナップショットを使用する場合、 `--snapshot`オプションを使用して、バックアップするタイムスタンプを指定できます。次のレベルの一貫性を使用することもできます。

-   `flush` : レプリカ データベースの DML および DDL 操作を一時的に中断し、バックアップ接続のグローバルな一貫性を確保し、binlog位置 (POS) 情報を記録するには、 [<a href="https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock">`FLUSH TABLES WITH READ LOCK`</a>](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock)を使用します。すべてのバックアップ接続がトランザクションを開始すると、ロックが解放されます。完全バックアップはオフピーク時間帯に実行するか、MySQL レプリカ データベースで実行することをお勧めします。
-   `snapshot` : 指定されたタイムスタンプの一貫したスナップショットを取得し、エクスポートします。
-   `lock` : エクスポートするすべてのテーブルに読み取りロックを追加します。
-   `none` : 一貫性の保証はありません。
-   `auto` : MySQL には`flush` 、TiDB には`snapshot`を使用します。

すべてが完了すると、エクスポートされたファイルが`/tmp/test`で表示されます。

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

Dumpling は、 `--snapshot`オプションを指定して、ある[<a href="/read-historical-data.md#how-tidb-reads-data-from-history-versions">tidb_スナップショット</a>](/read-historical-data.md#how-tidb-reads-data-from-history-versions)のデータをエクスポートできます。

`--snapshot`オプションは、TSO ( `SHOW MASTER STATUS`コマンドによって出力される`Position`フィールド) または`datetime`データ型の有効時間 ( `YYYY-MM-DD hh:mm:ss`の形式) に設定できます。次に例を示します。

{{< copyable "" >}}

```shell
./dumpling --snapshot 417773951312461825
./dumpling --snapshot "2020-07-02 17:12:45"
```

TSO が`417773951312461825` 、時刻が`2020-07-02 17:12:45`のときの TiDB 履歴データのスナップショットがエクスポートされます。

### 大きなテーブルのエクスポート時のメモリ使用量を制御する {#control-the-memory-usage-of-exporting-large-tables}

Dumplingが TiDB から大きな単一テーブルをエクスポートしている場合、エクスポートされたデータのサイズが大きすぎるため、メモリ不足 (OOM) が発生し、接続が中止され、エクスポートが失敗する可能性があります。次のパラメータを使用すると、TiDB のメモリ使用量を削減できます。

-   エクスポートするデータをチャンクに分割するには`-r`を設定します。これにより、TiDB のデータ スキャンのメモリオーバーヘッドが軽減され、テーブル データの同時ダンプが可能になり、エクスポート効率が向上します。アップストリーム データベースが TiDB v3.0 以降のバージョンの場合、このパラメータの値が 0 より大きい場合、TiDB リージョン情報が分割に使用され、ここで指定した値が有効でなくなることを示します。
-   `--tidb-mem-quota-query`の値を`8589934592` (8 GB) 以下に減らしてください。 `--tidb-mem-quota-query` TiDB 内の単一のクエリ ステートメントのメモリ使用量を制御します。
-   `--params "tidb_distsql_scan_concurrency=5"`パラメータを調整します。 [<a href="/system-variables.md#tidb_distsql_scan_concurrency">`tidb_distsql_scan_concurrency`</a>](/system-variables.md#tidb_distsql_scan_concurrency)は、TiDB でのスキャン操作の同時実行性を制御するセッション変数です。

### 大量のデータ (1 TB を超える) をエクスポートする場合は TiDB GC を設定します {#set-tidb-gc-when-exporting-a-large-volume-of-data-more-than-1-tb}

TiDB (1 TB を超える) からデータをエクスポートする場合、TiDB バージョンが v4.0.0 以降で、 Dumpling がTiDB クラスターの PD アドレスにアクセスできる場合、 Dumpling は元のクラスターに影響を与えることなく GC 時間を自動的に延長します。

他のシナリオでは、データ サイズが非常に大きい場合、エクスポート プロセス中の GC によるエクスポートの失敗を避けるために、事前に GC 時間を延長できます。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_gc_life_time = '720h';
```

操作が完了したら、GC 時間を元に戻します (デフォルト値は`10m` )。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

## Dumplingのオプション一覧 {#option-list-of-dumpling}

| オプション                        | 使用法                                                                                                                                                                                                                                                                 | デフォルト値                                                                                                                                                              |     |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| `-V`または`--version`           | Dumplingバージョンを出力して直接終了します                                                                                                                                                                                                                                           |                                                                                                                                                                     |     |
| `-B`または`--database`          | 指定したデータベースをエクスポートする                                                                                                                                                                                                                                                 |                                                                                                                                                                     |     |
| `-T`または`--tables-list`       | 指定したテーブルをエクスポートする                                                                                                                                                                                                                                                   |                                                                                                                                                                     |     |
| `-f`または`--filter`            | フィルター パターンに一致するテーブルをエクスポートします。フィルターの構文については、 [<a href="/table-filter.md">テーブルフィルター</a>](/table-filter.md)を参照してください。                                                                                                                                                 | `[\*.\*,!/^(mysql&#124;sys&#124;INFORMATION_SCHEMA&#124;PERFORMANCE_SCHEMA&#124;METRICS_SCHEMA&#124;INSPECTION_SCHEMA)$/.\*]` (システムスキーマを除くすべてのデータベースまたはテーブルをエクスポート) |     |
| `--case-sensitive`           | テーブルフィルターで大文字と小文字が区別されるかどうか                                                                                                                                                                                                                                         | false (大文字と小文字を区別しない)                                                                                                                                               |     |
| `-h`または`--host`              | 接続されているデータベースホストのIPアドレス                                                                                                                                                                                                                                             | 「127.0.0.1」                                                                                                                                                         |     |
| `-t`または`--threads`           | 同時バックアップスレッドの数                                                                                                                                                                                                                                                      | 4                                                                                                                                                                   |     |
| `-r`または`--rows`              | テーブルを指定した行数の行に分割します (通常、大きなテーブルを複数のファイルに分割する同時操作に適用されます。アップストリーム データベースが TiDB v3.0 以降のバージョンの場合、このパラメータの値が 0 より大きい場合、 TiDB リージョン情報は分割に使用されるため、ここで指定した値は有効になりません。                                                                                                     |                                                                                                                                                                     |     |
| `-L`または`--logfile`           | ログ出力アドレス。空の場合、ログがコンソールに出力されます。                                                                                                                                                                                                                                      | 「」                                                                                                                                                                  |     |
| `--loglevel`                 | ログレベル {デバッグ、情報、警告、エラー、パニック、panic、致命的}                                                                                                                                                                                                                               | &quot;情報&quot;                                                                                                                                                      |     |
| `--logfmt`                   | ログ出力形式 {text,json}                                                                                                                                                                                                                                                  | &quot;文章&quot;                                                                                                                                                      |     |
| `-d`または`--no-data`           | データをエクスポートしない (スキーマのみがエクスポートされるシナリオに適しています)                                                                                                                                                                                                                         |                                                                                                                                                                     |     |
| `--no-header`                | ヘッダーを生成せずにテーブルの CSV ファイルをエクスポートします                                                                                                                                                                                                                                  |                                                                                                                                                                     |     |
| `-W`または`--no-views`          | ビューをエクスポートしないでください                                                                                                                                                                                                                                                  | 真実                                                                                                                                                                  |     |
| `-m`または`--no-schemas`        | データのみをエクスポートしたスキーマをエクスポートしないでください。                                                                                                                                                                                                                                  |                                                                                                                                                                     |     |
| `-s`または`--statement-size`    | `INSERT`ステートメントのサイズを制御します。単位はバイトです                                                                                                                                                                                                                                  |                                                                                                                                                                     |     |
| `-F`または`--filesize`          | 分割されたテーブルのファイルサイズ。単位は`128B` 、 `64KiB` 、 `32MiB` 、 `1.5GiB`などで指定する必要があります。                                                                                                                                                                                           |                                                                                                                                                                     |     |
| `--filetype`                 | エクスポートされるファイルの種類 (csv/sql)                                                                                                                                                                                                                                          | 「SQL」                                                                                                                                                               |     |
| `-o`または`--output`            | エクスポートされたローカル ファイルのパス、または[<a href="/br/backup-and-restore-storages.md">外部storageのURL</a>](/br/backup-and-restore-storages.md)                                                                                                                                       | 「./export-${time}」                                                                                                                                                  |     |
| `-S`または`--sql`               | 指定されたSQL文に従ってデータをエクスポートします。このコマンドは同時エクスポートをサポートしていません。                                                                                                                                                                                                              |                                                                                                                                                                     |     |
| `--consistency`              | フラッシュ: ダンプの前に FTWRL を使用します。<br/>スナップショット: TSO の特定のスナップショットの TiDB データをダンプします。<br/> lock: ダンプされるすべてのテーブルに対して`lock tables read`を実行します。<br/> none: ロックを追加せずにダンプします。一貫性は保証できません。<br/> auto: MySQL の場合は --consistency flash を使用します。 TiDB の --consistency スナップショットを使用する    | 「自動」                                                                                                                                                                |     |
| `--snapshot`                 | スナップショット TSO。 `consistency=snapshot`の場合のみ有効                                                                                                                                                                                                                         |                                                                                                                                                                     |     |
| `--where`                    | `where`条件を通じてテーブル バックアップの範囲を指定します                                                                                                                                                                                                                                   |                                                                                                                                                                     |     |
| `-p`または`--password`          | 接続されたデータベースホストのパスワード                                                                                                                                                                                                                                                |                                                                                                                                                                     |     |
| `-P`または`--port`              | 接続されているデータベースホストのポート                                                                                                                                                                                                                                                | 4000                                                                                                                                                                |     |
| `-u`または`--user`              | 接続されているデータベースホストのユーザー名                                                                                                                                                                                                                                              | &quot;根&quot;                                                                                                                                                       |     |
| `--dump-empty-database`      | 空のデータベースの`CREATE DATABASE`ステートメントをエクスポートします。                                                                                                                                                                                                                        | 真実                                                                                                                                                                  |     |
| `--ca`                       | TLS接続用の認証局ファイルのアドレス                                                                                                                                                                                                                                                 |                                                                                                                                                                     |     |
| `--cert`                     | TLS接続用のクライアント証明書ファイルのアドレス                                                                                                                                                                                                                                           |                                                                                                                                                                     |     |
| `--key`                      | TLS接続用のクライアント秘密鍵ファイルのアドレス                                                                                                                                                                                                                                           |                                                                                                                                                                     |     |
| `--csv-delimiter`            | CSVファイルの文字型変数の区切り文字                                                                                                                                                                                                                                                 | 「」                                                                                                                                                                  |     |
| `--csv-separator`            | CSV ファイル内の各値の区切り文字。デフォルトの「,」を使用することはお勧めできません。 「|+|」を使用することをお勧めします。またはその他の珍しい文字の組み合わせ                                                                                                                                                                                | 「、」                                                                                                                                                                 | 「、」 |
| `--csv-null-value`           | CSV ファイル内の null 値の表現                                                                                                                                                                                                                                                | 「\N」                                                                                                                                                                |     |
| `--escape-backslash`         | エクスポート ファイル内の特殊文字をエスケープするには、バックスラッシュ ( `\` ) を使用します。                                                                                                                                                                                                                | 真実                                                                                                                                                                  |     |
| `--output-filename-template` | [<a href="https://golang.org/pkg/text/template/#hdr-Arguments">golang テンプレート</a>](https://golang.org/pkg/text/template/#hdr-Arguments)の形式で表されるファイル名テンプレート<br/>`{{.DB}}` 、 `{{.Table}}` 、および`{{.Index}}`引数をサポートします<br/>3 つの引数は、データ ファイルのデータベース名、テーブル名、チャンク ID を表します。 | &#39;{{.DB}}.{{.Table}}.{{.Index}}&#39;                                                                                                                             |     |
| `--status-addr`              | Dumpling のサービス アドレス (Prometheus がメトリクスと pprof デバッグを取得するためのアドレスを含む)                                                                                                                                                                                                  | &quot;:8281&quot;                                                                                                                                                   |     |
| `--tidb-mem-quota-query`     | Dumplingコマンドの 1 行で SQL ステートメントをエクスポートする際のメモリ制限。単位はバイトです。 v4.0.10 以降のバージョンでは、このパラメーターを設定しない場合、TiDB はデフォルトで`mem-quota-query`構成項目の値をメモリ制限値として使用します。 v4.0.10 より前のバージョンの場合、パラメータ値のデフォルトは 32 GB です。                                                                       | 34359738368                                                                                                                                                         |     |
| `--params`                   | エクスポートするデータベースの接続のセッション変数を指定します。必要な形式は`"character_set_client=latin1,character_set_connection=latin1"`です                                                                                                                                                             |                                                                                                                                                                     |     |
