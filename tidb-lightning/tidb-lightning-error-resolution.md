---
title: TiDB Lightning Error Resolution
summary: Learn how to resolve type conversion and duplication errors during data import.
---

# TiDB Lightningエラーの解決 {#tidb-lightning-error-resolution}

v5.4.0 から、無効な型変換や一意キーの競合などのエラーをスキップし、それらの間違った行データが存在しないかのようにデータ処理を続行するようにTiDB Lightningを構成できます。後でエラーを読んで手動で修正するためのレポートが生成されます。これは、手動でエラーを見つけるのが難しく、発生するたびにTiDB Lightningを再起動するのがコストがかかる、少し汚れたデータ ソースからインポートするのに理想的です。

このドキュメントでは、型エラー機能 ( `lightning.max-error` ) と重複解決機能 ( `tikv-importer.duplicate-resolution` ) の使用方法を紹介します。また、これらのエラーが保存されるデータベースについても紹介します ( `lightning.task-info-schema-name` )。このドキュメントの最後に、例を示します。

## タイプエラー {#type-error}

`lightning.max-error`構成を使用して、データ型に関連するエラーの許容度を高めることができます。この構成が*N*に設定されている場合、 TiDB Lightning は、データソースが存在する前に最大<em>N 個の</em>エラーを許可し、スキップします。デフォルト値`0`エラーが許可されないことを意味します。

これらのエラーはデータベースに記録されます。インポートが完了したら、データベース内のエラーを表示して手動で処理できます。詳細については、 [エラーレポート](#error-report)を参照してください。

{{< copyable "" >}}

```toml
[lightning]
max-error = 0
```

上記の構成は、次のエラーをカバーしています。

-   無効な値 (例: INT 列に`'Text'`を設定)。
-   数値のオーバーフロー (例: TINYINT 列に`500`を設定)
-   文字列のオーバーフロー (例: VARCHAR(5) 列に`'Very Long Text'`を設定)。
-   ゼロの日時 (つまり、 `'0000-00-00'`および`'2021-12-00'` )。
-   NOT NULL 列に NULL を設定します。
-   生成された列の式を評価できませんでした。
-   カラム数が一致しません。行の値の数がテーブルの列の数と一致しません。
-   `on-duplicate = "error"`の場合、TiDB バックエンドでの一意/主キーの競合。
-   その他の SQL エラー。

次のエラーは常に致命的であり、 `max-error`を変更してもスキップできません。

-   元の CSV、SQL、または Parquet ファイルの構文エラー (閉じていない引用符など)。
-   I/O、ネットワーク、またはシステムの許可エラー。

ローカル バックエンドでの一意/主キーの競合は、個別に処理され、次のセクションで説明されます。

## エラーレポート {#error-report}

インポート中にTiDB Lightning でエラーが発生した場合、終了時に端末とログ ファイルの両方にこれらのエラーに関する統計の概要が出力されます。

-   ターミナルのエラー レポートは、次の表のようになります。

    |   | エラーの種類  | エラー数 | エラーデータテーブル                              |
    | - | ------- | ---- | --------------------------------------- |
    | 1 | データ・タイプ | 1000 | `lightning_task_info` . `type_error_v1` |

-   TiDB Lightningログ ファイルのエラー レポートは次のとおりです。

    ```shell
    [2022/03/13 05:33:57.736 +08:00] [WARN] [errormanager.go:459] ["Detect 1000 data type errors in total, please refer to table `lightning_task_info`.`type_error_v1` for more details"]
    ```

すべてのエラーは、ダウンストリーム TiDB クラスターの`lightning_task_info`データベース内のテーブルに書き込まれます。インポートが完了した後、エラー データが収集されている場合は、データベース内のエラーを表示して手動で処理できます。

`lightning.task-info-schema-name`を構成することにより、データベース名を変更できます。

{{< copyable "" >}}

```toml
[lightning]
task-info-schema-name = 'lightning_task_info'
```

TiDB Lightning は、このデータベースに 3 つのテーブルを作成します。

```sql
CREATE TABLE syntax_error_v1 (
    task_id     bigint NOT NULL,
    create_time datetime(6) NOT NULL DEFAULT now(6),
    table_name  varchar(261) NOT NULL,
    path        varchar(2048) NOT NULL,
    offset      bigint NOT NULL,
    error       text NOT NULL,
    context     text
);

CREATE TABLE type_error_v1 (
    task_id     bigint NOT NULL,
    create_time datetime(6) NOT NULL DEFAULT now(6),
    table_name  varchar(261) NOT NULL,
    path        varchar(2048) NOT NULL,
    offset      bigint NOT NULL,
    error       text NOT NULL,
    row_data    text NOT NULL
);

CREATE TABLE conflict_error_v1 (
    task_id     bigint NOT NULL,
    create_time datetime(6) NOT NULL DEFAULT now(6),
    table_name  varchar(261) NOT NULL,
    index_name  varchar(128) NOT NULL,
    key_data    text NOT NULL,
    row_data    text NOT NULL,
    raw_key     mediumblob NOT NULL,
    raw_value   mediumblob NOT NULL,
    raw_handle  mediumblob NOT NULL,
    raw_row     mediumblob NOT NULL,
    KEY (task_id, table_name)
);
```

<!--
**syntax_error_v1** is intended to record syntax error from files. It is not implemented yet.
-->

**type_error_v1 は、** `max-error`の構成によって管理されるすべての[タイプエラー](#type-error)を記録します。エラーごとに 1 行あります。

**conflict_error_v1 は、**ローカル バックエンドでのすべての一意/主キーの競合を記録します。競合のペアごとに 2 つの行があります。

| カラム         | 構文 | タイプ | 対立 | 説明                                                                   |
| ----------- | -- | --- | -- | -------------------------------------------------------------------- |
| task_id     | ✓  | ✓   | ✓  | このエラーを生成するTiDB Lightningタスク ID                                       |
| create_time | ✓  | ✓   | ✓  | エラーが記録された時刻                                                          |
| テーブル名       | ✓  | ✓   | ✓  | エラーを含むテーブルの名前 ( ``'`db`.`tbl`'``の形式)                                 |
| 道           | ✓  | ✓   |    | エラーを含むファイルのパス                                                        |
| オフセット       | ✓  | ✓   |    | エラーが見つかったファイル内のバイト位置                                                 |
| エラー         | ✓  | ✓   |    | エラーメッセージ                                                             |
| コンテクスト      | ✓  |     |    | エラーを囲むテキスト                                                           |
| インデックス名     |    |     | ✓  | 競合している一意のキーの名前。主キーの競合の場合は`'PRIMARY'`です。                              |
| key_data    |    |     | ✓  | エラーの原因となった行の書式設定されたキー ハンドル。コンテンツは人間の参照のみを目的としており、機械可読を意図したものではありません。 |
| 行データ        |    | ✓   | ✓  | エラーの原因となった書式設定された行データ。コンテンツは人間の参照のみを目的としており、機械可読を意図したものではありません       |
| raw_key     |    |     | ✓  | 競合する KV ペアのキー                                                        |
| raw_value   |    |     | ✓  | 競合する KV ペアの値                                                         |
| raw_handle  |    |     | ✓  | 競合する行の行ハンドル                                                          |
| raw_row     |    |     | ✓  | 競合する行のエンコードされた値                                                      |

> **ノート：**
>
> エラー レポートには、取得するのが非効率な行/列番号ではなく、ファイル オフセットが記録されます。次のコマンドを使用して、バイト位置の近く (例として 183 を使用) にすばやくジャンプできます。
>
> -   シェル、最初の数行を出力します。
>
>     ```shell
>     head -c 183 file.csv | tail
>     ```
>
> -   シェル、次の数行を出力します。
>
>     ```shell
>     tail -c +183 file.csv | head
>     ```
>
> -   vim — `:goto 183`または`183go`

## 例 {#example}

この例では、いくつかの既知のエラーを含むデータ ソースが準備されています。

1.  データベースとテーブル スキーマを準備します。

    {{< copyable "" >}}

    ```shell
    mkdir example && cd example

    echo 'CREATE SCHEMA example;' > example-schema-create.sql
    echo 'CREATE TABLE t(a TINYINT PRIMARY KEY, b VARCHAR(12) NOT NULL UNIQUE);' > example.t-schema.sql
    ```

2.  データを準備します。

    {{< copyable "" >}}

    ```shell
    cat <<EOF > example.t.1.sql

        INSERT INTO t (a, b) VALUES
        (0, NULL),              -- column is NOT NULL
        (1, 'one'),
        (2, 'two'),
        (40, 'forty'),          -- conflicts with the other 40 below
        (54, 'fifty-four'),     -- conflicts with the other 'fifty-four' below
        (77, 'seventy-seven'),  -- the string is longer than 12 characters
        (600, 'six hundred'),   -- the number overflows TINYINT
        (40, 'forty'),         -- conflicts with the other 40 above
        (42, 'fifty-four');     -- conflicts with the other 'fifty-four' above

    EOF
    ```

3.  厳密な SQL モードを有効にするようにTiDB Lightningを構成し、ローカル バックエンドを使用してデータをインポートし、重複を削除し、最大 10 個のエラーをスキップします。

    {{< copyable "" >}}

    ```shell
    cat <<EOF > config.toml

        [lightning]
        max-error = 10

        [tikv-importer]
        backend = 'local'
        sorted-kv-dir = '/tmp/lightning-tmp/'
        duplicate-resolution = 'remove'

        [mydumper]
        data-source-dir = '.'
        [tidb]
        host = '127.0.0.1'
        port = 4000
        user = 'root'
        password = ''
        sql-mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE'

    EOF
    ```

4.  TiDB Lightningを実行します。すべてのエラーがスキップされるため、このコマンドは正常に終了します。

    {{< copyable "" >}}

    ```shell
    tiup tidb-lightning -c config.toml
    ```

5.  インポートされたテーブルに 2 つの通常の行のみが含まれていることを確認します。

    ```sql
    $ mysql -u root -h 127.0.0.1 -P 4000 -e 'select * from example.t'
    +---+-----+
    | a | b   |
    +---+-----+
    | 1 | one |
    | 2 | two |
    +---+-----+
    ```

6.  `type_error_v1`テーブルが型変換を含む 3 つの行をキャッチしたかどうかを確認します。

    ```sql
    $ mysql -u root -h 127.0.0.1 -P 4000 -e 'select * from lightning_task_info.type_error_v1;' -E

    *************************** 1. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.620090
     table_name: `example`.`t`
           path: example.t.1.sql
         offset: 46
          error: failed to cast value as varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin for column `b` (#2): [table:1048]Column 'b' cannot be null
       row_data: (0,NULL)

    *************************** 2. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.627496
     table_name: `example`.`t`
           path: example.t.1.sql
         offset: 183
          error: failed to cast value as varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin for column `b` (#2): [types:1406]Data Too Long, field len 12, data len 13
       row_data: (77,'seventy-seven')

    *************************** 3. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.629929
     table_name: `example`.`t`
           path: example.t.1.sql
         offset: 253
          error: failed to cast value as tinyint(4) for column `a` (#1): [types:1690]constant 600 overflows tinyint
       row_data: (600,'six hundred')
    ```

7.  `conflict_error_v1`テーブルが、一意/主キーの競合がある 4 つの行をキャッチしたかどうかを確認します。

    ```sql
    $ mysql -u root -h 127.0.0.1 -P 4000 -e 'select * from lightning_task_info.conflict_error_v1;' --binary-as-hex -E

    *************************** 1. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.669601
     table_name: `example`.`t`
     index_name: PRIMARY
       key_data: 40
       row_data: (40, "forty")
        raw_key: 0x7480000000000000C15F728000000000000028
      raw_value: 0x800001000000020500666F727479
     raw_handle: 0x7480000000000000C15F728000000000000028
        raw_row: 0x800001000000020500666F727479

    *************************** 2. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.674798
     table_name: `example`.`t`
     index_name: PRIMARY
       key_data: 40
       row_data: (40, "forty")
        raw_key: 0x7480000000000000C15F728000000000000028
      raw_value: 0x800001000000020600666F75727479
     raw_handle: 0x7480000000000000C15F728000000000000028
        raw_row: 0x800001000000020600666F75727479

    *************************** 3. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.680332
     table_name: `example`.`t`
     index_name: b
       key_data: 54
       row_data: (54, "fifty-four")
        raw_key: 0x7480000000000000C15F6980000000000000010166696674792D666FFF7572000000000000F9
      raw_value: 0x0000000000000036
     raw_handle: 0x7480000000000000C15F728000000000000036
        raw_row: 0x800001000000020A0066696674792D666F7572

    *************************** 4. row ***************************
        task_id: 1635888701843303564
    create_time: 2021-11-02 21:31:42.681073
     table_name: `example`.`t`
     index_name: b
       key_data: 42
       row_data: (42, "fifty-four")
        raw_key: 0x7480000000000000C15F6980000000000000010166696674792D666FFF7572000000000000F9
      raw_value: 0x000000000000002A
     raw_handle: 0x7480000000000000C15F72800000000000002A
        raw_row: 0x800001000000020A0066696674792D666F7572
    ```
