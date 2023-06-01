---
title: TiDB Lightning Error Resolution
summary: Learn how to resolve type conversion and duplication errors during data import.
---

# TiDB Lightningエラーの解決 {#tidb-lightning-error-resolution}

v5.4.0 以降、無効な型変換や一意のキーの競合などのエラーをスキップし、それらの間違った行データが存在しないかのようにデータ処理を続行するようにTiDB Lightningを設定できるようになりました。レポートが生成されるので、後で読んでエラーを手動で修正できます。これは、エラーを手動で特定することが難しく、エラーが発生するたびにTiDB Lightningを再起動するのはコストがかかる、少し汚れたデータ ソースからインポートする場合に最適です。

この文書では、タイプエラー機能 ( `lightning.max-error` ) と重複解決機能 ( `tikv-importer.duplicate-resolution` ) の使用方法を紹介します。また、これらのエラーが保存されるデータベースも紹介します ( `lightning.task-info-schema-name` )。このドキュメントの最後に例が示されています。

## タイプエラー {#type-error}

`lightning.max-error`構成を使用すると、データ型に関連するエラーの許容度を高めることができます。この構成が*N*に設定されている場合、 TiDB Lightning はデータ ソースが存在する前に最大*N 個の*エラーを許可し、スキップします。デフォルト値`0`エラーが許可されないことを意味します。

これらのエラーはデータベースに記録されます。インポートが完了したら、データベース内のエラーを表示し、手動で処理できます。詳細については、 [<a href="#error-report">エラーレポート</a>](#error-report)を参照してください。

{{< copyable "" >}}

```toml
[lightning]
max-error = 0
```

上記の構成では、次のエラーがカバーされます。

-   無効な値 (例: INT 列に`'Text'`を設定)。
-   数値オーバーフロー (例: TINYINT 列に`500`を設定)
-   文字列オーバーフロー (例: VARCHAR(5) 列に`'Very Long Text'`を設定)。
-   日時ゼロ (つまり`'0000-00-00'`と`'2021-12-00'` )。
-   NOT NULL 列に NULL を設定します。
-   生成された列式の評価に失敗しました。
-   カラム数が一致しません。行内の値の数がテーブルの列の数と一致しません。
-   TiDB バックエンドでの一意/主キーの競合 ( `on-duplicate = "error"`の場合)。
-   その他の SQL エラー。

次のエラーは常に致命的であり、 `max-error`を変更してもスキップできません。

-   元の CSV、SQL、または Parquet ファイル内の構文エラー (閉じられていない引用符など)。
-   I/O、ネットワーク、またはシステム権限エラー。

物理インポート モードでの一意/主キーの競合は個別に処理され、次のセクションで説明されます。

## エラーレポート {#error-report}

TiDB Lightning でインポート中にエラーが発生した場合、終了時にターミナルとログ ファイルの両方にこれらのエラーに関する統計概要が出力されます。

-   端末のエラー レポートは次の表のようになります。

    |   | エラーの種類  | エラー数 | エラーデータテーブル                              |
    | - | ------- | ---- | --------------------------------------- |
    | 1 | データ・タイプ | 1000 | `lightning_task_info` 。 `type_error_v1` |

-   TiDB Lightningログ ファイルのエラー レポートは次のとおりです。

    ```shell
    [2022/03/13 05:33:57.736 +08:00] [WARN] [errormanager.go:459] ["Detect 1000 data type errors in total, please refer to table `lightning_task_info`.`type_error_v1` for more details"]
    ```

すべてのエラーは、ダウンストリーム TiDB クラスターの`lightning_task_info`データベース内のテーブルに書き込まれます。インポートの完了後、エラー データが収集された場合は、データベース内のエラーを表示して手動で処理できます。

`lightning.task-info-schema-name`を設定することでデータベース名を変更できます。

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

**type_error_v1 は、** `max-error`の構成によって管理される[<a href="#type-error">タイプエラー</a>](#type-error)すべてを記録します。エラーごとに 1 行があります。

**conflict_error_v1 は、**ローカル バックエンド内のすべての一意/主キーの競合を記録します。競合のペアごとに 2 行があります。

| カラム       | 構文 | タイプ | 対立 | 説明                                                                           |
| --------- | -- | --- | -- | ---------------------------------------------------------------------------- |
| タスクID     | ✓  | ✓   | ✓  | このエラーを生成するTiDB Lightningタスク ID                                               |
| 作成時間      | ✓  | ✓   | ✓  | エラーが記録された時刻                                                                  |
| テーブル名     | ✓  | ✓   | ✓  | エラーを含むテーブルの名前 ( ``'`db`.`tbl`'``の形式)                                         |
| 道         | ✓  | ✓   |    | エラーが含まれるファイルのパス                                                              |
| オフセット     | ✓  | ✓   |    | ファイル内でエラーが見つかったバイト位置                                                         |
| エラー       | ✓  | ✓   |    | エラーメッセージ                                                                     |
| コンテクスト    | ✓  |     |    | エラーを囲むテキスト                                                                   |
| インデックス名   |    |     | ✓  | 競合している一意のキーの名前。主キーの競合の場合は`'PRIMARY'`です。                                      |
| キーデータ     |    |     | ✓  | エラーの原因となった行のフォーマットされたキー ハンドル。コンテンツは人間の参照のみを目的としており、機械で読み取り可能にすることを目的としていません。 |
| 行データ      |    | ✓   | ✓  | エラーの原因となったフォーマット済みの行データ。コンテンツは人間の参照のみを目的としており、機械で読み取り可能にすることを目的としていません。      |
| raw_key   |    |     | ✓  | 競合した KV ペアのキー                                                                |
| raw_value |    |     | ✓  | 競合する KV ペアの値                                                                 |
| raw_ハンドル  |    |     | ✓  | 競合している行の行ハンドル                                                                |
| 生の行       |    |     | ✓  | 競合した行のエンコードされた値                                                              |

> **ノート：**
>
> エラー レポートには、取得が非効率である行/列番号ではなく、ファイル オフセットが記録されます。次のコマンドを使用すると、バイト位置付近 (例として 183 を使用) にすばやくジャンプできます。
>
> -   シェル、最初の数行を出力します。
>
>     ```shell
>     head -c 183 file.csv | tail
>     ```
>
> -   シェルで次の数行を出力します。
>
>     ```shell
>     tail -c +183 file.csv | head
>     ```
>
> -   vim — `:goto 183`または`183go`

## 例 {#example}

この例では、いくつかの既知のエラーを含むデータ ソースが準備されています。

1.  データベースとテーブルのスキーマを準備します。

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

3.  TiDB Lightningを構成して厳密な SQL モードを有効にし、ローカル バックエンドを使用してデータをインポートし、重複を削除し、最大 10 件のエラーをスキップします。

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

7.  `conflict_error_v1`テーブルが一意/主キーの競合がある 4 つの行を検出したかどうかを確認します。

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
