---
title: Dumpling Overview
summary: Use the Dumpling tool to export data from TiDB.
---

# Dumplingの概要 {#dumpling-overview}

このドキュメントでは、データエクスポートツール[Dumpling](https://github.com/pingcap/dumpling)を紹介します。Dumplingは、TiDB / MySQLに保存されているデータをSQLまたはCSVデータファイルとしてエクスポートし、論理的な完全バックアップまたはエクスポートを行うために使用できます。

SSTファイル（キーと値のペア）のバックアップ、または遅延の影響を受けない増分データのバックアップについては、 [BR](/br/backup-and-restore-overview.md)を参照してください。インクリメンタルデータのリアルタイムバックアップについては、 [TiCDC](/ticdc/ticdc-overview.md)を参照してください。

> **ノート：**
>
> PingCAPは、以前はTiDBに固有の拡張機能を備えた[mydumperプロジェクト](https://github.com/maxbube/mydumper)のフォークを維持していました。その後、このフォークは[Dumpling](/dumpling-overview.md)に置き換えられました。これは、Goで書き直され、TiDBに固有のより多くの最適化をサポートします。 mydumperの代わりにDumplingを使用することを強くお勧めします。
>
> Mydumperの概要については、 [v4.0Mydumperのドキュメント](https://docs.pingcap.com/tidb/v4.0/backup-and-restore-using-mydumper-lightning)を参照してください。

## Mydumperと比較したDumplingの改善 {#improvements-of-dumpling-compared-with-mydumper}

1.  SQLやCSVを含む複数の形式でのデータのエクスポートをサポート
2.  データのフィルタリングを容易にする[テーブルフィルター](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md)つの機能をサポートします
3.  AmazonS3クラウドストレージへのデータのエクスポートをサポートします。
4.  TiDBに対してさらに最適化が行われます。
    -   単一のTiDB SQLステートメントのメモリ制限の構成をサポート
    -   TiDBv4.0.0以降のTiDBGC時間の自動調整をサポート
    -   TiDBの非表示の列`_tidb_rowid`を使用して、単一のテーブルからの同時データエクスポートのパフォーマンスを最適化します
    -   TiDBの場合、値[`tidb_snapshot`](/read-historical-data.md#how-tidb-reads-data-from-history-versions)を設定して、データバックアップの時点を指定できます。これにより、一貫性を確保するために`FLUSH TABLES WITH READ LOCK`を使用する代わりに、バックアップの一貫性が保証されます。

## Dumpling紹介 {#dumpling-introduction}

Dumplingは囲碁で書かれています。 Githubプロジェクトは[pingcap/餃子](https://github.com/pingcap/dumpling)です。

Dumplingの詳細な使用法については、 `--help`オプションを使用するか、 [Dumplingのオプションリスト](#option-list-of-dumpling)を参照してください。

Dumplingを使用する場合は、実行中のクラスタでexportコマンドを実行する必要があります。このドキュメントでは、 `127.0.0.1:4000`のホストにTiDBインスタンスがあり、このTiDBインスタンスにパスワードのないrootユーザーがいることを前提としています。

`tiup install dumpling`を実行すると、 [TiUP](/tiup/tiup-overview.md)を使用してDumplingを取得できます。その後、 `tiup dumpling ...`を使用してDumplingを実行できます。

DumplingインストールパッケージはTiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロードする](/download-ecosystem-tools.md)を参照してください。

## TiDB/MySQLからデータをエクスポートする {#export-data-from-tidb-mysql}

### 必要な特権 {#required-privileges}

-   選択する
-   リロード
-   ロックテーブル
-   レプリケーションクライアント
-   処理する

### SQLファイルにエクスポート {#export-to-sql-files}

DumplingはデフォルトでデータをSQLファイルにエクスポートします。 `--filetype sql`フラグを追加して、データをSQLファイルにエクスポートすることもできます。

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

上記のコマンドでは：

-   `-h` 、および`-p`オプションは、それぞれアドレス、ポート、およびユーザーを意味し`-u` 。認証にパスワードが必要な場合は、 `-p $YOUR_SECRET_PASSWORD`を使用してパスワードをDumplingに渡すことができます。
-   `-o`オプションは、ローカルファイルパスまたは[外部ストレージのURL](/br/backup-and-restore-storages.md)をサポートするストレージのエクスポートディレクトリを指定します。
-   `-t`オプションは、エクスポートするスレッドの数を指定します。スレッドの数を増やすと、Dumplingの同時実行性とエクスポート速度が向上し、データベースのメモリ消費量も増加します。したがって、数値を大きく設定しすぎることはお勧めしません。通常、64未満です。
-   `-r`オプションは、1つのファイルの最大行数を指定します。このオプションを指定すると、 Dumplingにより、テーブル内の同時実行がエクスポートを高速化し、メモリ使用量を削減できます。アップストリームデータベースがTiDBv3.0以降のバージョンの場合、このパラメーターの値が0より大きい場合は、TiDB領域情報が分割に使用され、ここで指定された値は無効になることを示します。
-   `-F`オプションは、単一ファイルの最大サイズを指定するために使用されます（ここでの単位は`MiB`です`5GiB`や`8KB`などの入力も受け入れられます）。 TiDB Lightningを使用してこのファイルをTiDBインスタンスにロードする場合は、その値を256MiB以下に保つことをお勧めします。

> **ノート：**
>
> エクスポートされた単一のテーブルのサイズが10GBを超える場合は、 `-r`および`-F`オプション**を使用することを強くお勧めし**ます。

### CSVファイルにエクスポート {#export-to-csv-files}

`--filetype csv`引数を追加すると、データをCSVファイルにエクスポートできます。

データをCSVファイルにエクスポートする場合、 `--sql <SQL>`を使用してSQLステートメントでレコードをフィルタリングできます。たとえば、次のコマンドを使用して、 `test.sbtest1`分の`id < 100`に一致するすべてのレコードをエクスポートできます。

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

上記のコマンドでは：

-   `--sql`オプションは、CSVファイルへのエクスポートにのみ使用できます。上記のコマンドは、エクスポートされるすべてのテーブルに対して`SELECT * FROM <table-name> WHERE id <100`ステートメントを実行します。テーブルに指定されたフィールドがない場合、エクスポートは失敗します。
-   `--sql`オプションを使用すると、 Dumplingはエクスポートされたテーブルおよびスキーマ情報を取得できません。 `--output-filename-template`オプションを使用してCSVファイルのファイル名形式を指定できます。これにより、後で[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してデータファイルをインポートしやすくなります。たとえば、 `--output-filename-template='test.sbtest1.{{.Index}}'`は、エクスポートされたCSVファイルの名前が`test.sbtest1.000000000`または`test.sbtest1.000000001`であることを指定します。
-   `--csv-separator`や`--csv-delimiter`などのオプションを使用して、CSVファイル形式を構成できます。詳しくは[Dumplingオプションリスト](#option-list-of-dumpling)をご覧ください。

> **ノート：**
>
> *文字列*と<em>キーワード</em>はDumplingによって区別されません。インポートされたデータがブール型の場合、 `true`の値は`1`に変換され、 `false`の値は`0`に変換されます。

### エクスポートされたファイルの形式 {#format-of-exported-files}

-   `metadata` ：エクスポートされたファイルの開始時刻とマスターバイナリログの位置。

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

-   `{schema}-schema-create.sql` ：スキーマの作成に使用されるSQLファイル

    {{< copyable "" >}}

    ```shell
    cat test-schema-create.sql
    ```

    ```shell
    CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
    ```

-   `{schema}.{table}-schema.sql` ：テーブルの作成に使用されるSQLファイル

    {{< copyable "" >}}

    ```shell
    cat test.t1-schema.sql
    ```

    ```shell
    CREATE TABLE `t1` (
      `id` int(11) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
    ```

-   `{schema}.{table}.{0001}.{sql|csv` }：日付ソースファイル

    {{< copyable "" >}}

    ```shell
    cat test.t1.0.sql
    ```

    ```shell
    /*!40101 SET NAMES binary*/;
    INSERT INTO `t1` VALUES
    (1);
    ```

-   `*-schema-view.sql` ： `*-schema-post.sql`の`*-schema-trigger.sql`されたファイル

### AmazonS3クラウドストレージにデータをエクスポートする {#export-data-to-amazon-s3-cloud-storage}

v4.0.8以降、 Dumplingはクラウドストレージへのデータのエクスポートをサポートしています。 AmazonのS3バックエンドストレージにデータをバックアップする必要がある場合は、 `-o`パラメーターでS3ストレージパスを指定する必要があります。

指定したリージョンにS3バケットを作成する必要があります（ [Amazonドキュメント-S3バケットを作成するにはどうすればよいですか](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)を参照）。バケット内にフォルダも作成する必要がある場合は、 [Amazonドキュメント-フォルダの作成](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html)を参照してください。

S3バックエンドストレージにアクセスする権限を持つアカウントの`SecretKey`と`AccessKey`を、環境変数としてDumplingノードに渡します。

{{< copyable "" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

Dumplingは、 `~/.aws/credentials`からのクレデンシャルファイルの読み取りもサポートします。Dumplingの構成の詳細については、 [外部ストレージ](/br/backup-and-restore-storages.md)の構成を参照してください。

Dumplingを使用してデータをバックアップする場合は、 `--s3.region`パラメーターを明示的に指定します。これは、S3ストレージの領域（たとえば、 `ap-northeast-1` ）を意味します。

{{< copyable "" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -r 200000 \
  -o "s3://${Bucket}/${Folder}" \
  --s3.region "${region}"
```

### エクスポートされたデータをフィルタリングする {#filter-the-exported-data}

#### <code>--where</code>オプションを使用して、データをフィルタリングします {#use-the-code-where-code-option-to-filter-data}

デフォルトでは、 Dumplingはシステム`PERFORMANCE_SCHEMA` （ `mysql` 、 `METRICS_SCHEMA` `sys`を`INSPECTION_SCHEMA` ）を除くすべてのデータベースをエクスポートし`INFORMATION_SCHEMA` 。 `--where <SQL where expression>`を使用して、エクスポートするレコードを選択できます。

{{< copyable "" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --where "id < 100"
```

上記のコマンドは、各テーブルから`id < 100`に一致するデータをエクスポートします。 `--where`パラメータを`--sql`と一緒に使用することはできないことに注意してください。

#### <code>--filter</code>オプションを使用して、データをフィルタリングします {#use-the-code-filter-code-option-to-filter-data}

Dumplingは、 `--filter`オプションでテーブルフィルターを指定することにより、特定のデータベースまたはテーブルをフィルター処理できます。テーブルフィルターの構文は`.gitignore`の構文と似ています。詳細については、 [テーブルフィルター](/table-filter.md)を参照してください。

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

上記のコマンドは、 `employees`のデータベースのすべてのテーブルとすべてのデータベースの`WorkOrder`のテーブルをエクスポートします。

#### <code>-B</code>または<code>-T</code>オプションを使用して、データをフィルタリングします {#use-the-code-b-code-or-code-t-code-option-to-filter-data}

Dumplingは、 `-B`オプションの特定のデータベースまたは`-T`オプションの特定のテーブルをエクスポートすることもできます。

> **ノート：**
>
> -   `--filter`オプションと`-T`オプションを同時に使用することはできません。
> -   `-T`オプションは、 `database-name.table-name`のような完全な形式の入力のみを受け入れることができ、テーブル名のみの入力は受け入れられません。例：Dumplingは`-T WorkOrder`を認識できません。

例：

-   `-B employees`は`employees`のデータベースをエクスポートします。
-   `-T employees.WorkOrder`は`employees.WorkOrder`のテーブルをエクスポートします。

### 同時実行によるエクスポート効率の向上 {#improve-export-efficiency-through-concurrency}

エクスポートされたファイルは、デフォルトで`./export-<current local time>`ディレクトリに保存されます。一般的に使用されるオプションは次のとおりです。

-   `-t`オプションは、エクスポートするスレッドの数を指定します。スレッドの数を増やすと、Dumplingの同時実行性とエクスポート速度が向上し、データベースのメモリ消費量も増加します。したがって、数値を大きく設定しすぎることはお勧めしません。
-   `-r`オプションは、単一ファイルのレコードの最大数（またはデータベース内の行数）を指定します。有効にすると、Dumplingによってテーブルの同時実行が有効になり、大きなテーブルのエクスポート速度が向上します。アップストリームデータベースがTiDBv3.0以降のバージョンの場合、このパラメーターの値が0より大きい場合は、TiDB領域情報が分割に使用され、ここで指定された値は無効になることを示します。
-   `--compress gzip`オプションを使用して、ダンプを圧縮できます。これは、ストレージがボトルネックである場合、またはストレージ容量が懸念される場合に、データのダンプを高速化するのに役立ちます。これの欠点は、CPU使用率の増加です。各ファイルは個別に圧縮されます。

上記のオプションを指定すると、Dumplingのデータエクスポート速度が速くなります。

### Dumplingのデータ整合性オプションを調整する {#adjust-dumpling-s-data-consistency-options}

> **ノート：**
>
> ほとんどのシナリオでは、 Dumplingのデフォルトのデータ整合性オプションを調整する必要はありません（デフォルト値は`auto`です）。

Dumplingは`--consistency <consistency level>`オプションを使用して、「整合性保証」のためにデータをエクスポートする方法を制御します。一貫性を保つためにスナップショットを使用する場合は、 `--snapshot`オプションを使用して、バックアップするタイムスタンプを指定できます。次のレベルの整合性を使用することもできます。

-   `flush` ： [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock)を使用して、レプリカデータベースのDMLおよびDDL操作を一時的に中断し、バックアップ接続のグローバル整合性を確保し、binlog位置（POS）情報を記録します。すべてのバックアップ接続がトランザクションを開始すると、ロックが解除されます。オフピーク時またはMySQLレプリカデータベースで完全バックアップを実行することをお勧めします。
-   `snapshot` ：指定されたタイムスタンプの一貫したスナップショットを取得してエクスポートします。
-   `lock` ：エクスポートするすべてのテーブルに読み取りロックを追加します。
-   `none` ：一貫性の保証はありません。
-   `auto` ：MySQLには`flush`を使用し、TiDBには`snapshot`を使用します。

すべてが完了すると、エクスポートされたファイルを`/tmp/test`で確認できます。

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

### TiDBの履歴データスナップショットをエクスポートする {#export-historical-data-snapshot-of-tidb}

Dumplingは、 `--snapshot`オプションを指定して特定の[tidb_snapshot](/read-historical-data.md#how-tidb-reads-data-from-history-versions)のデータをエクスポートできます。

`--snapshot`オプションは、TSO（ `SHOW MASTER STATUS`コマンドによって出力される`Position`フィールド）または`datetime`データ型の有効時間（ `YYYY-MM-DD hh:mm:ss`の形式）に設定できます。次に例を示します。

{{< copyable "" >}}

```shell
./dumpling --snapshot 417773951312461825
./dumpling --snapshot "2020-07-02 17:12:45"
```

TSOが`417773951312461825`で時刻が`2020-07-02 17:12:45`の場合のTiDB履歴データスナップショットがエクスポートされます。

### 大きなテーブルをエクスポートする際のメモリ使用量を制御する {#control-the-memory-usage-of-exporting-large-tables}

DumplingがTiDBから大きな単一のテーブルをエクスポートしている場合、エクスポートされたデータサイズが大きすぎるためにメモリ不足（OOM）が発生し、接続の中止とエクスポートの失敗が発生する可能性があります。次のパラメータを使用して、TiDBのメモリ使用量を減らすことができます。

-   エクスポートするデータをチャンクに分割するには、 `-r`を設定します。これにより、TiDBのデータスキャンのメモリオーバーヘッドが削減され、同時テーブルデータダンプが可能になり、エクスポートの効率が向上します。アップストリームデータベースがTiDBv3.0以降のバージョンの場合、このパラメーターの値が0より大きい場合は、TiDB領域情報が分割に使用され、ここで指定された値は無効になることを示します。
-   `--tidb-mem-quota-query`から`8589934592` （8 GB）以下の値を減らします。 `--tidb-mem-quota-query`は、TiDBの単一のクエリステートメントのメモリ使用量を制御します。
-   `--params "tidb_distsql_scan_concurrency=5"`パラメーターを調整します。 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)は、TiDBでのスキャン操作の同時実行性を制御するセッション変数です。

### 大量のデータ（1 TBを超える）をエクスポートする場合のTiDBGC設定 {#tidb-gc-settings-when-exporting-a-large-volume-of-data-more-than-1-tb}

TiDB（1 TBを超える）からデータをエクスポートするときに、TiDBのバージョンがv4.0.0以降で、 DumplingがTiDBクラスタのPDアドレスにアクセスできる場合、 Dumplingは元のクラスタに影響を与えることなくGC時間を自動的に延長します。

他のシナリオでは、データサイズが非常に大きい場合、エクスポートプロセス中のGCによるエクスポートの失敗を回避するために、事前にGC時間を延長できます。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_gc_life_time = '720h';
```

操作が完了したら、GC時間を元に戻します（デフォルト値は`10m`です）。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

最後に、エクスポートされたすべてのデータは、 [TiDB Lightning](/tidb-lightning/tidb-lightning-backends.md)を使用してTiDBにインポートして戻すことができます。

## Dumplingのオプションリスト {#option-list-of-dumpling}

| オプション                        | 使用法                                                                                                                                                                                                                                  | デフォルト値                                                                                                                                                                 |             |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `-V`または`--version`           | Dumplingバージョンを出力し、直接終了します                                                                                                                                                                                                            |                                                                                                                                                                        |             |
| `-B`または`--database`          | 指定されたデータベースをエクスポートする                                                                                                                                                                                                                 |                                                                                                                                                                        |             |
| `-T`または`--tables-list`       | 指定されたテーブルをエクスポートする                                                                                                                                                                                                                   |                                                                                                                                                                        |             |
| `-f`または`--filter`            | フィルタパターンに一致するテーブルをエクスポートします。フィルタの構文については、 [テーブルフィルター](/table-filter.md)を参照してください。                                                                                                                                                    | `[\*.\*,!/^(mysql&#124;sys&#124;INFORMATION_SCHEMA&#124;PERFORMANCE_SCHEMA&#124;METRICS_SCHEMA&#124;INSPECTION_SCHEMA)$/.\*]` （システムスキーマを除くすべてのデータベースまたはテーブルをエクスポートします） |             |
| `--case-sensitive`           | table-filterで大文字と小文字が区別されるかどうか                                                                                                                                                                                                       | false（大文字と小文字を区別しない）                                                                                                                                                   |             |
| `-h`または`--host`              | 接続されているデータベースホストのIPアドレス                                                                                                                                                                                                              | 「127.0.0.1」                                                                                                                                                            |             |
| `-t`または`--threads`           | 同時バックアップスレッドの数                                                                                                                                                                                                                       | 4                                                                                                                                                                      |             |
| `-r`または`--rows`              | テーブルを指定された行数の行に分割します（通常、大きなテーブルを複数のファイルに分割する同時操作に適用できます。アップストリームデータベースがTiDB v3.0以降のバージョンの場合、このパラメーターの値が0より大きい場合は、 TiDBリージョン情報は分割に使用され、ここで指定された値は無効になります。                                                                             |                                                                                                                                                                        |             |
| `-L`または`--logfile`           | ログ出力アドレス。空の場合、ログはコンソールに出力されます                                                                                                                                                                                                        | &quot;&quot;                                                                                                                                                           |             |
| `--loglevel`                 | ログレベル{debug、info、warn、error、dpanic、 panic、fatal}                                                                                                                                                                                     | &quot;情報&quot;                                                                                                                                                         |             |
| `--logfmt`                   | ログ出力形式{text、json}                                                                                                                                                                                                                    | &quot;文章&quot;                                                                                                                                                         |             |
| `-d`または`--no-data`           | データをエクスポートしない（スキーマのみがエクスポートされるシナリオに適しています）                                                                                                                                                                                           |                                                                                                                                                                        |             |
| `--no-header`                | ヘッダーを生成せずにテーブルのCSVファイルをエクスポートする                                                                                                                                                                                                      |                                                                                                                                                                        |             |
| `-W`または`--no-views`          | ビューをエクスポートしないでください                                                                                                                                                                                                                   | 真実                                                                                                                                                                     |             |
| `-m`または`--no-schemas`        | データのみをエクスポートした状態でスキーマをエクスポートしないでください                                                                                                                                                                                                 |                                                                                                                                                                        |             |
| `-s`または`--statement-size`    | `INSERT`ステートメントのサイズを制御します。単位はバイトです                                                                                                                                                                                                   |                                                                                                                                                                        |             |
| `-F`または`--filesize`          | 分割されたテーブルのファイルサイズ。単位は`128B`などで`32MiB`する必要が`1.5GiB` `64KiB` 。                                                                                                                                                                         |                                                                                                                                                                        |             |
| `--filetype`                 | エクスポートされたファイルタイプ（csv / sql）                                                                                                                                                                                                          | 「sql」                                                                                                                                                                  |             |
| `-o`または`--output`            | エクスポートされたローカルファイルのパスまたは[外部ストレージのURL](/br/backup-and-restore-storages.md)                                                                                                                                                             | &quot;./export-${time}&quot;                                                                                                                                           |             |
| `-S`または`--sql`               | 指定されたSQLステートメントに従ってデータをエクスポートします。このコマンドは、同時エクスポートをサポートしていません。                                                                                                                                                                        |                                                                                                                                                                        |             |
| `--consistency`              | フラッシュ：ダンプの前にFTWRLを使用します<br/>スナップショット：TSOの特定のスナップショットのTiDBデータをダンプします<br/>ロック：ダンプするすべてのテーブルで`lock tables read`を実行します<br/>none：ロックを追加せずにダンプします。これは一貫性を保証できません<br/>auto：MySQLの--consistencyflushを使用します。 TiDBの--consistencyスナップショットを使用します | 「自動」                                                                                                                                                                   |             |
| `--snapshot`                 | スナップショットTSO; `consistency=snapshot`の場合にのみ有効                                                                                                                                                                                          |                                                                                                                                                                        |             |
| `--where`                    | `where`条件でテーブルバックアップの範囲を指定します                                                                                                                                                                                                        |                                                                                                                                                                        |             |
| `-p`または`--password`          | 接続されているデータベースホストのパスワード                                                                                                                                                                                                               |                                                                                                                                                                        |             |
| `-P`または`--port`              | 接続されたデータベースホストのポート                                                                                                                                                                                                                   | 4000                                                                                                                                                                   |             |
| `-u`または`--user`              | 接続されたデータベースホストのユーザー名                                                                                                                                                                                                                 | &quot;根&quot;                                                                                                                                                          |             |
| `--dump-empty-database`      | 空のデータベースの`CREATE DATABASE`のステートメントをエクスポートします                                                                                                                                                                                         | 真実                                                                                                                                                                     |             |
| `--ca`                       | TLS接続用の認証局ファイルのアドレス                                                                                                                                                                                                                  |                                                                                                                                                                        |             |
| `--cert`                     | TLS接続用のクライアント証明書ファイルのアドレス                                                                                                                                                                                                            |                                                                                                                                                                        |             |
| `--key`                      | TLS接続用のクライアント秘密鍵ファイルのアドレス                                                                                                                                                                                                            |                                                                                                                                                                        |             |
| `--csv-delimiter`            | CSVファイルの文字型変数の区切り文字                                                                                                                                                                                                                  | &#39;&quot;&#39;                                                                                                                                                       |             |
| `--csv-separator`            | CSVファイルの各値のセパレータ。デフォルトの「、」を使用することはお勧めしません。 &#39;|+|&#39;の使用をお勧めしますまたは他の珍しい文字の組み合わせ                                                                                                                                                   | &#39;、&#39;                                                                                                                                                            | &#39;、&#39; |
| `--csv-null-value`           | CSVファイルでのnull値の表現                                                                                                                                                                                                                    | &quot;\ N&quot;                                                                                                                                                        |             |
| `--escape-backslash`         | バックスラッシュ（ `\` ）を使用して、エクスポートファイル内の特殊文字をエスケープします                                                                                                                                                                                       | 真実                                                                                                                                                                     |             |
| `--output-filename-template` | [golangテンプレート](https://golang.org/pkg/text/template/#hdr-Arguments)の形式で表されるファイル名テンプレート<br/>`{{.DB}}` 、および`{{.Table}}`の引数を`{{.Index}}`する<br/>3つの引数は、データファイルのデータベース名、テーブル名、およびチャンクIDを表します。                                             | &#39;{{。DB}}。{{。Table}}。{{。Index}}&#39;                                                                                                                                |             |
| `--status-addr`              | Prometheusがメトリックとpprofデバッグをプルするためのアドレスを含む餃子のサービスアドレス                                                                                                                                                                                 | &quot;：8281&quot;                                                                                                                                                      |             |
| `--tidb-mem-quota-query`     | Dumplingコマンドの1行でSQLステートメントをエクスポートするメモリ制限。単位はバイトです。 v4.0.10以降のバージョンでは、このパラメーターを設定しない場合、TiDBはデフォルトで`mem-quota-query`構成項目の値をメモリー制限値として使用します。 v4.0.10より前のバージョンの場合、パラメーター値のデフォルトは32GBです。                                                  | 34359738368                                                                                                                                                            |             |
| `--params`                   | エクスポートするデータベースの接続のセッション変数を指定します。必要な形式は`"character_set_client=latin1,character_set_connection=latin1"`です                                                                                                                              |                                                                                                                                                                        |             |
