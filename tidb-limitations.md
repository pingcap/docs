---
title: TiDB Limitations
summary: Learn the usage limitations of TiDB.
---

# TiDBの制限 {#tidb-limitations}

このドキュメントでは、サポートされるデータベース、テーブル、インデックス、パーティションテーブル、シーケンスの最大識別子の長さや最大数など、TiDBの一般的な使用制限について説明します。

## 識別子の長さの制限 {#limitations-on-identifier-length}

| 識別子の種類 | 最大長（許可される文字数） |
| :----- | :------------ |
| データベース | 64            |
| テーブル   | 64            |
| 桁      | 64            |
| 索引     | 64            |
| 意見     | 64            |
| 順序     | 64            |

## データベース、テーブル、ビュー、および接続の総数の制限 {#limitations-on-the-total-number-of-databases-tables-views-and-connections}

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

## 単一のテーブルの制限 {#limitations-on-a-single-table}

| タイプ     | 上限（デフォルト値）                  |
| :------ | :-------------------------- |
| 列       | デフォルトは1017で、最大4096まで調整できます。 |
| インデックス  | デフォルトは64で、最大512まで調整できます     |
| 行       | 無制限                         |
| サイズ     | 無制限                         |
| パーティション | 8192                        |

-   `Columns`の上限は[`table-column-count-limit`](/tidb-configuration-file.md#table-column-count-limit-new-in-v50)を介して変更できます。
-   `Indexes`の上限は[`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50)を介して変更できます。

## 単一行の制限 {#limitation-on-a-single-row}

| タイプ | 上限                                                                                                                      |
| :-- | :---------------------------------------------------------------------------------------------------------------------- |
| サイズ | デフォルトでは6MB。サイズ制限は、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)の構成アイテムで調整できます。 |

## 単一列の制限 {#limitation-on-a-single-column}

| タイプ | 上限   |
| :-- | :--- |
| サイズ | 6 MB |

## 文字列タイプの制限 {#limitations-on-string-types}

| タイプ       | 上限      |
| :-------- | :------ |
| CHAR      | 256文字   |
| バイナリ      | 256文字   |
| VARBINARY | 65535文字 |
| VARCHAR   | 16383文字 |
| 文章        | 6 MB    |
| BLOB      | 6 MB    |

## SQLステートメントの制限 {#limitations-on-sql-statements}

| タイプ                         | 上限                                                                                                                                        |
| :-------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| 1回のトランザクションでのSQLステートメントの最大数 | 楽観的トランザクションが使用され、トランザクションの再試行が有効になっている場合、デフォルトの上限は5000であり、 [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit)を使用して変更できます。 |
