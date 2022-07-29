---
title: TiDB Lightning Error Resolution
summary: Learn how to resolve type conversion and duplication errors during data import.
---

# TiDB Lightningエラー解決 {#tidb-lightning-error-resolution}

v5.4.0以降、無効な型変換や一意キーの競合などのエラーをスキップし、それらの間違った行データが存在しないかのようにデータ処理を続行するようにTiDB Lightningを構成できます。後でエラーを読んで手動で修正するためのレポートが生成されます。これは、エラーを手動で特定することが難しく、遭遇するたびにTiDB Lightningを再起動するのにコストがかかる、少し汚れたデータソースからインポートするのに理想的です。

このドキュメントでは、タイプエラー機能（ `lightning.max-error` ）と重複解決機能（ `tikv-importer.duplicate-resolution` ）の使用方法を紹介します。また、これらのエラーが保存されているデータベースも紹介します（ `lightning.task-info-schema-name` ）。このドキュメントの最後に、例を示します。

## タイプエラー {#type-error}

`lightning.max-error`構成を使用して、データ型に関連するエラーの許容度を上げることができます。この構成が*N*に設定されている場合、 TiDB Lightningは、データソースが存在する前に最大<em>N個</em>のエラーを許可およびスキップします。デフォルト値`0`は、エラーが許可されないことを意味します。

これらのエラーはデータベースに記録されます。インポートが完了したら、データベース内のエラーを表示して手動で処理できます。詳細については、 [エラーレポート](#error-report)を参照してください。

{{< copyable "" >}}

```toml
[lightning]
max-error = 0
```

上記の構成は、次のエラーをカバーしています。

-   無効な値（例： `'Text'`をINT列に設定）。
-   数値オーバーフロー（例： `500`をTINYINT列に設定）
-   文字列オーバーフロー（例： `'Very Long Text'`をVARCHAR（5）列に設定）。
-   ゼロ日時（つまり、 `'0000-00-00'`と`'2021-12-00'` ）。
-   NULLをNOTNULL列に設定します。
-   生成された列式の評価に失敗しました。
-   カラム数の不一致。行の値の数がテーブルの列の数と一致しません。
-   `on-duplicate = "error"`の場合、TiDBバックエンドでの一意/主キーの競合。
-   その他のSQLエラー。

次のエラーは常に致命的であり、 `max-error`を変更してもスキップできません。

-   元のCSV、SQL、またはParquetファイルの構文エラー（閉じられていない引用符など）。
-   I / O、ネットワークまたはシステムのアクセス許可エラー。

ローカルバックエンドでの一意/主キーの競合は個別に処理され、次のセクションで説明されます。

## ローカルバックエンドモードでの重複解決 {#duplicate-resolution-in-local-backend-mode}

ローカルバックエンドモードでは、 TiDB Lightningは、最初にデータをKVペアに変換し、ペアをバッチでTiKVに取り込むことにより、データをインポートします。 TiDBバックエンドモードとは異なり、重複する行はタスクが終了するまで検出されません。したがって、ローカルバックエンドモードでの重複エラーは`max-error`によって制御されるのではなく、別の構成`duplicate-resolution`によって制御されます。

{{< copyable "" >}}

```toml
[tikv-importer]
duplicate-resolution = 'none'
```

`duplicate-resolution`の値オプションは次のとおりです。

-   **&#39;none&#39;** ：重複データを検出しません。一意/主キーの競合が存在する場合、インポートされたテーブルには一貫性のないデータとインデックスがあり、チェックサムチェックに失敗します。
-   **&#39;record&#39;** ：重複データを検出しますが、修正は試みません。一意/主キーの競合が存在する場合、インポートされたテーブルには一貫性のないデータとインデックスがあり、チェックサムをスキップして競合エラーの数を報告します。
-   **&#39;remove&#39;** ：重複データを検出し、重複した*すべての*行を削除します。インポートされたテーブルは一貫性がありますが、関連する行は無視され、手動で追加し直す必要があります。

TiDB Lightningの重複解像度は、データソース内でのみ重複データを検出できます。この機能は、 TiDB Lightningを実行する前に既存のデータとの競合を処理できません。

## エラーレポート {#error-report}

インポート中にTiDBLightningでエラーが発生した場合、 TiDB Lightningは、終了時に、端末とログファイルの両方にこれらのエラーに関する統計要約を出力します。

-   ターミナルのエラーレポートは、次の表のようになります。

    |   | エラータイプ  | エラーカウント | エラーデータテーブル                              |
    | - | ------- | ------- | --------------------------------------- |
    | 1 | データ・タイプ | 1000    | `lightning_task_info` 。 `type_error_v1` |

-   TiDB Lightningログファイルのエラーレポートは次のとおりです。

    ```shell
    [2022/03/13 05:33:57.736 +08:00] [WARN] [errormanager.go:459] ["Detect 1000 data type errors in total, please refer to table `lightning_task_info`.`type_error_v1` for more details"]
    ```

すべてのエラーは、ダウンストリームTiDBクラスタの`lightning_task_info`のデータベースのテーブルに書き込まれます。インポートが完了した後、エラーデータが収集された場合は、データベース内のエラーを表示して手動で処理できます。

`lightning.task-info-schema-name`を設定することにより、データベース名を変更できます。

{{< copyable "" >}}

```toml
[lightning]
task-info-schema-name = 'lightning_task_info'
```

TiDB Lightningは、このデータベースに3つのテーブルを作成します。

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

**type_error_v1**は、 `max-error`の構成によって管理される[タイプエラー](#type-error)すべてを記録します。エラーごとに1つの行があります。

**conflict_error_v1**は[ローカルバックエンドでの一意/主キーの競合](#duplicate-resolution-in-local-backend-mode)すべてを記録します。競合のペアごとに2つの行があります。

| カラム          | 構文 | タイプ | 対立 | 説明                                                                                |
| ------------ | -- | --- | -- | --------------------------------------------------------------------------------- |
| task_id      | ✓✓ | ✓✓  | ✓✓ | このエラーを生成するTiDB LightningタスクID                                                     |
| create_table | ✓✓ | ✓✓  | ✓✓ | エラーが記録された時刻                                                                       |
| table_name   | ✓✓ | ✓✓  | ✓✓ | エラーを含むテーブルの名前（ ``'`db`.`tbl`'``の形式）                                               |
| 道            | ✓✓ | ✓✓  |    | エラーを含むファイルのパス                                                                     |
| オフセット        | ✓✓ | ✓✓  |    | エラーが見つかったファイル内のバイト位置                                                              |
| エラー          | ✓✓ | ✓✓  |    | エラーメッセージ                                                                          |
| 環境           | ✓✓ |     |    | エラーを囲むテキスト                                                                        |
| index_name   |    |     | ✓✓ | 競合している一意のキーの名前。主キーの競合の場合は`'PRIMARY'`です。                                           |
| key_data     |    |     | ✓✓ | エラーの原因となった行のフォーマットされたキーハンドル。このコンテンツは人間が参照するためのものであり、機械で読み取り可能であることを意図したものではありません。 |
| row_data     |    | ✓✓  | ✓✓ | エラーの原因となるフォーマットされた行データ。コンテンツは人間が参照するためのものであり、機械で読み取り可能であることを意図したものではありません。        |
| raw_key      |    |     | ✓✓ | 競合するKVペアのキー                                                                       |
| raw_value    |    |     | ✓✓ | 競合するKVペアの値                                                                        |
| raw_handle   |    |     | ✓✓ | 競合する行の行ハンドル                                                                       |
| raw_row      |    |     | ✓✓ | 競合する行のエンコードされた値                                                                   |

> **ノート：**
>
> エラーレポートは、取得が非効率的な行/列番号ではなく、ファイルオフセットを記録します。次のコマンドを使用して、バイト位置の近くにすばやくジャンプできます（例として183を使用）。
>
> -   シェル、最初の数行を印刷します。
>
>     ```shell
>     head -c 183 file.csv | tail
>     ```
>
> -   シェル、次の数行を印刷します。
>
>     ```shell
>     tail -c +183 file.csv | head
>     ```
>
> -   vim `:goto 183`または`183go`

## 例 {#example}

この例では、データソースはいくつかの既知のエラーで準備されています。

1.  データベースとテーブルスキーマを準備します。

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
        (40, 'fourty'),         -- conflicts with the other 40 above
        (42, 'fifty-four');     -- conflicts with the other 'fifty-four' above

    EOF
    ```

3.  厳密なSQLモードを有効にするようにTiDB Lightningを構成し、ローカルバックエンドを使用してデータをインポートし、重複を削除し、最大10個のエラーをスキップします。

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

5.  インポートされたテーブルに2つの通常の行のみが含まれていることを確認します。

    ```sql
    $ mysql -u root -h 127.0.0.1 -P 4000 -e 'select * from example.t'
    +---+-----+
    | a | b   |
    +---+-----+
    | 1 | one |
    | 2 | two |
    +---+-----+
    ```

6.  `type_error_v1`つのテーブルが型変換を含む3つの行をキャッチしたかどうかを確認します。

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

7.  `conflict_error_v1`つのテーブルが一意/主キーの競合がある4つの行をキャッチしたかどうかを確認します。

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
       row_data: (40, "fourty")
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
