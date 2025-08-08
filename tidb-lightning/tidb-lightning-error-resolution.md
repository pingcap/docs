---
title: TiDB Lightning Error Resolution
summary: データのインポート中に発生する型変換および重複エラーを解決する方法を学習します。
---

# TiDB Lightningエラー解決 {#tidb-lightning-error-resolution}

v5.4.0以降、 TiDB Lightningを設定して、無効な型変換や一意キーの競合などのエラーをスキップし、それらの誤った行データが存在しないかのようにデータ処理を続行できるようになりました。生成されたレポートを読んで、後で手動でエラーを修正できます。これは、やや乱れたデータソースからのインポートに最適です。手動でエラーを特定するのは困難で、発生するたびにTiDB Lightningを再起動するのはコストがかかります。

このドキュメントでは、TiDB Lightning のエラーの種類、エラーのクエリ方法、および例を紹介します。以下の設定項目が関係します。

-   `lightning.max-error` : 型エラーの許容閾値
-   `conflict.strategy` : 競合`conflict.max-record-rows` `conflict.threshold`に関連する構成
-   `tikv-importer.duplicate-resolution` (v8.0.0 で非推奨となり、将来のリリースで削除される予定): 物理インポート モードでのみ使用できる競合処理構成
-   `lightning.task-info-schema-name` : TiDB Lightningが競合を検出したときに競合するデータが格納されるデータベース

詳細については[TiDB Lightning （タスク）](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)参照してください。

## 入力エラー {#type-error}

`lightning.max-error`設定を使用すると、データ型に関連するエラーの許容範囲を広げることができます。この設定を*N*に設定すると、 TiDB Lightning はデータソースから最大*N*個のエラーを許容し、データソースが存在する前にスキップします。デフォルト値の`0` 、エラーが許容されないことを意味します。

これらのエラーはデータベースに記録されます。インポート完了後、データベース内のエラーを確認し、手動で処理することができます。詳細については、 [エラーレポート](#error-report)参照してください。

```toml
[lightning]
max-error = 0
```

上記の構成では、次のエラーがカバーされます。

-   無効な値 (例: INT 列に`'Text'`設定する)。
-   数値オーバーフロー（例：TINYINT列に`500`設定する）
-   文字列オーバーフロー（例：VARCHAR(5)列に`'Very Long Text'`設定する）。
-   日付と時刻がゼロ (つまり`'0000-00-00'`と`'2021-12-00'` )。
-   NOT NULL 列に NULL を設定します。
-   生成された列式の評価に失敗しました。
-   カラム数が一致しません。行内の値の数がテーブルの列数と一致しません。
-   その他の SQL エラー。

以下のエラーは常に致命的であり、 `lightning.max-error`変更してもスキップすることはできません。

-   元の CSV、SQL、または Parquet ファイルの構文エラー (閉じられていない引用符など)。
-   I/O、ネットワーク、またはシステムの権限エラー。

## 競合エラー {#conflict-errors}

設定項目[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)使用すると、データ競合に関連するエラーの許容度を高めることができます。この設定項目を*N*に設定すると、 TiDB Lightning はデータソースから最大*N 個の*競合エラーを許容し、それをスキップしてから終了します。デフォルト値は`10000`で、これは 10000 個のエラーが許容されることを意味します。

これらのエラーはテーブルに記録されます。インポートが完了したら、データベースでエラーを確認し、手動で処理することができます。詳細については、 [エラーレポート](#error-report)をご覧ください。

## エラーレポート {#error-report}

TiDB Lightning がインポート中にエラーに遭遇した場合、終了時にターミナルとログ ファイルの両方にこれらのエラーに関する統計の概要が出力されます。

-   ターミナルのエラーレポートは次の表のようになります。

    |   | エラーの種類 | エラー数 | エラーデータテーブル                            |
    | - | ------ | ---- | ------------------------------------- |
    | 1 | データ型   | 1000 | `lightning_task_info` `type_error_v1` |

-   TiDB Lightningログ ファイル内のエラー レポートは次のとおりです。

    ```shell
    [2022/03/13 05:33:57.736 +08:00] [WARN] [errormanager.go:459] ["Detect 1000 data type errors in total, please refer to table `lightning_task_info`.`type_error_v1` for more details"]
    ```

すべてのエラーは、下流TiDBクラスタの`lightning_task_info`のデータベース内のテーブルに書き込まれます。インポートが完了した後、エラーデータが収集されていれば、データベース内のエラーを確認し、手動で処理することができます。

`lightning.task-info-schema-name`設定することでデータベース名を変更できます。

```toml
[lightning]
task-info-schema-name = 'lightning_task_info'
```

TiDB Lightning はこのデータベースに 3 つのテーブルと 1 つのビューを作成します。

```sql
CREATE TABLE type_error_v1 (
    task_id     bigint NOT NULL,
    create_time datetime(6) NOT NULL DEFAULT now(6),
    table_name  varchar(261) NOT NULL,
    path        varchar(2048) NOT NULL,
    offset      bigint NOT NULL,
    error       text NOT NULL,
    row_data    text NOT NULL
);
CREATE TABLE conflict_error_v3 (
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
    kv_type     tinyint NOT NULL,
    INDEX (task_id, table_name),
    INDEX (index_name),
    INDEX (table_name, index_name),
    INDEX (kv_type)
);
CREATE TABLE conflict_records (
    task_id     bigint NOT NULL,
    create_time datetime(6) NOT NULL DEFAULT now(6),
    table_name  varchar(261) NOT NULL,
    path        varchar(2048) NOT NULL,
    offset      bigint NOT NULL,
    error       text NOT NULL,
    row_id      bigint NOT NULL COMMENT 'the row id of the conflicted row',
    row_data    text NOT NULL COMMENT 'the row data of the conflicted row',
    KEY (task_id, table_name)
);
CREATE VIEW conflict_view AS
    SELECT 0 AS is_precheck_conflict, task_id, create_time, table_name, index_name, key_data, row_data, raw_key, raw_value, raw_handle, raw_row, kv_type, NULL AS path, NULL AS offset, NULL AS error, NULL AS row_id
    FROM conflict_error_v3
    UNION ALL
    SELECT 1 AS is_precheck_conflict, task_id, create_time, table_name, NULL AS index_name, NULL AS key_data, row_data, NULL AS raw_key, NULL AS raw_value, NULL AS raw_handle, NULL AS raw_row, NULL AS kv_type, path, offset, error, row_id
    FROM conflict_records;
```

`type_error_v1`テーブルには、 `lightning.max-error`によって管理される[型エラー](#type-error)がすべて記録されます。各エラーは 1 行に対応します。

`conflict_error_v3`テーブルは、後処理の競合検出時に検出された競合を記録します。これは、物理インポートモードの`conflict`構成グループによって管理されます。各競合ペアは 2 行に対応します。

`conflict_records`テーブルには、インポート前の競合検出で検出された競合が記録されます。この競合は、論理インポートモードと物理インポートモードの両方で`conflict`構成グループによって管理されます。各エラーは 1 行に対応します。

`conflict_view`ビューは、インポート前とインポート後の競合検出の両方で検出された競合を記録します。これらの競合は、論理インポートモードと物理インポートモードの両方で`conflict`設定グループによって管理されます。このビューは、 `conflict_error_v3`テーブルと`conflict_records`テーブルに対して`UNION`操作を実行することで作成されます。

| カラム     | 構文 | タイプ | 対立 | 説明                                                                          |
| ------- | -- | --- | -- | --------------------------------------------------------------------------- |
| タスクID   | ✓  | ✓   | ✓  | このエラーを生成するTiDB Lightningタスク ID                                              |
| 作成時間    | ✓  | ✓   | ✓  | エラーが記録された時刻                                                                 |
| テーブル名   | ✓  | ✓   | ✓  | エラーを含むテーブルの名前（ ``'`db`.`tbl`'``の形式）                                         |
| path    | ✓  | ✓   |    | エラーを含むファイルのパス                                                               |
| オフセット   | ✓  | ✓   |    | ファイル内でエラーが見つかったバイト位置                                                        |
| エラー     | ✓  | ✓   |    | エラーメッセージ                                                                    |
| コンテクスト  | ✓  |     |    | エラーを囲むテキスト                                                                  |
| インデックス名 |    |     | ✓  | 競合している一意キーの名前。主キーが競合している場合は`'PRIMARY'`なります。                                 |
| キーデータ   |    |     | ✓  | エラーの原因となった行のフォーマットされたキーハンドル。この内容は人間による参照のみを目的としており、機械による読み取りを意図したものではありません。 |
| 行データ    |    | ✓   | ✓  | エラーの原因となったフォーマットされた行データ。この内容は人間による参照のみを目的としており、機械による読み取りを意図したものではありません。     |
| 生のキー    |    |     | ✓  | 競合するKVペアのキー                                                                 |
| 生の値     |    |     | ✓  | 競合するKVペアの値                                                                  |
| 生のハンドル  |    |     | ✓  | 競合した行の行ハンドル                                                                 |
| 生の行     |    |     | ✓  | 競合行のエンコードされた値                                                               |

> **注記：**
>
> エラーレポートにはファイルオフセットが記録されますが、行番号や列番号を取得するのは非効率的です。以下のコマンドを使用すると、バイト位置（例えば183）の近くまで素早くジャンプできます。
>
> -   シェル、最初の数行を出力します。
>
>     ```shell
>     head -c 183 file.csv | tail
>     ```
>
> -   シェルは、次の数行を出力します。
>
>     ```shell
>     tail -c +183 file.csv | head
>     ```
>
> -   vim — `:goto 183`または`183go`

## 例 {#example}

この例では、いくつかの既知のエラーを含むデータ ソースが準備されます。

1.  データベースとテーブル スキーマを準備します。

    ```shell
    mkdir example && cd example

    echo 'CREATE SCHEMA example;' > example-schema-create.sql
    echo 'CREATE TABLE t(a TINYINT PRIMARY KEY, b VARCHAR(12) NOT NULL UNIQUE);' > example.t-schema.sql
    ```

2.  データを準備します。

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

3.  TiDB Lightningを構成して厳密な SQL モードを有効にし、ローカル バックエンドを使用してデータをインポートし、重複を置き換え、最大 10 個のエラーをスキップします。

    ```shell
    cat <<EOF > config.toml

        [lightning]
        max-error = 10

        [tikv-importer]
        backend = 'local'
        sorted-kv-dir = '/tmp/lightning-tmp/'

        [conflict]
        strategy = 'replace'
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

    ```shell
    tiup tidb-lightning -c config.toml
    ```

5.  インポートされたテーブルに次の 2 つの通常の行のみが含まれていることを確認します。

    ```sql
    $ mysql -u root -h 127.0.0.1 -P 4000 -e 'select * from example.t'
    +---+-----+
    | a | b   |
    +---+-----+
    | 1 | one |
    | 2 | two |
    +---+-----+
    ```

6.  `type_error_v1`テーブルに型変換を含む 3 つの行が含まれているかどうかを確認します。

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
          error: failed to cast value as tinyint for column `a` (#1): [types:1690]constant 600 overflows tinyint
       row_data: (600,'six hundred')
    ```

7.  `conflict_error_v3`テーブルに、一意/主キーの競合がある 4 つの行が含まれているかどうかを確認します。

    ```sql
    $ mysql -u root -h 127.0.0.1 -P 4000 -e 'select * from lightning_task_info.conflict_error_v3;' --binary-as-hex -E

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
