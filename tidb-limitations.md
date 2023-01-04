---
title: TiDB Limitations
summary: Learn the usage limitations of TiDB.
---

# TiDB の制限事項 {#tidb-limitations}

このドキュメントでは、識別子の最大長、サポートされるデータベース、テーブル、インデックス、分割テーブル、シーケンスの最大数など、TiDB の一般的な使用制限について説明します。

## 識別子の長さの制限 {#limitations-on-identifier-length}

| 識別子の種類 | 最大長 (許容される文字数) |
| :----- | :------------- |
| データベース | 64             |
| テーブル   | 64             |
| カラム    | 64             |
| 索引     | 64             |
| ビュー    | 64             |
| シーケンス  | 64             |

## データベース、テーブル、ビュー、および接続の合計数に関する制限 {#limitations-on-the-total-number-of-databases-tables-views-and-connections}

| 識別子の種類 | 最大数 |
| :----- | :-- |
| データベース | 無制限 |
| テーブル   | 無制限 |
| ビュー    | 無制限 |
| 接続     | 無制限 |

## 単一データベースの制限 {#limitations-on-a-single-database}

| タイプ  | 上限  |
| :--- | :-- |
| テーブル | 無制限 |

## 単一テーブルの制限 {#limitations-on-a-single-table}

| タイプ     | 上限（デフォルト値）                     |
| :------ | :----------------------------- |
| コラム     | デフォルトは 1017 で、最大 4096 まで調整できます |
| インデックス  | デフォルトは 64 で、最大 512 まで調整できます    |
| 行       | 無制限                            |
| サイズ     | 無制限                            |
| パーティション | 8192                           |

<CustomContent platform="tidb">

-   `Columns`の上限は[`table-column-count-limit`](/tidb-configuration-file.md#table-column-count-limit-new-in-v50)で変更できます。
-   `Indexes`の上限は[`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50)で変更できます。

</CustomContent>

## 1 行の制限 {#limitation-on-a-single-row}

| タイプ | 上限（デフォルト値）                     |
| :-- | :----------------------------- |
| サイズ | デフォルトは 6 MiB で、120 MiB に調整できます |

<CustomContent platform="tidb">

[`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)構成項目でサイズ制限を調整できます。

</CustomContent>

## 単一列の制限 {#limitation-on-a-single-column}

| タイプ | 上限（デフォルト値）                     |
| :-- | :----------------------------- |
| サイズ | デフォルトは 6 MiB で、120 MiB に調整できます |

<CustomContent platform="tidb">

[`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)構成項目でサイズ制限を調整できます。

</CustomContent>

## データ型の制限 {#limitations-on-data-types}

| タイプ       | 上限                             |
| :-------- | :----------------------------- |
| CHAR      | 256文字                          |
| バイナリ      | 256文字                          |
| VARBINARY | 65535 文字                       |
| VARCHAR   | 16383 文字                       |
| TEXT      | デフォルトは 6 MiB で、120 MiB に調整できます |
| BLOB      | デフォルトは 6 MiB で、120 MiB に調整できます |

## SQL ステートメントの制限 {#limitations-on-sql-statements}

| タイプ                            | 上限                                               |
| :----------------------------- | :----------------------------------------------- |
| 1 つのトランザクション内の SQL ステートメントの最大数 | 楽観的トランザクションを使用し、トランザクションのリトライが有効な場合、上限は 5000 です。 |

<CustomContent platform="tidb">

[`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit)構成アイテムで制限を変更できます。

</CustomContent>

## TiKV版の制限事項 {#limitations-on-tikv-version}

クラスターで、TiDBコンポーネントのバージョンが v6.2.0 以降の場合、TiKV のバージョンは v6.2.0 以降である必要があります。
