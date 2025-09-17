---
title: TiDB Limitations
summary: TiDB の使用制限について学習します。
---

# TiDB の制限 {#tidb-limitations}

このドキュメントでは、識別子の最大長や、サポートされるデータベース、テーブル、インデックス、パーティション テーブル、シーケンスの最大数など、TiDB の一般的な使用上の制限について説明します。

> **注記：**
>
> TiDBはMySQLのプロトコルおよび構文と高い互換性を備えていますが、MySQLの多くの制限事項も含まれています。例えば、1つのインデックスには最大16列まで含めることができます。詳細については、 [MySQLの互換性](/mysql-compatibility.md)およびMySQLの公式ドキュメントをご覧ください。

## 識別子の長さの制限 {#limitations-on-identifier-length}

| 識別子の種類 | 最大長（許容文字数） |
| :----- | :--------- |
| データベース | 64         |
| テーブル   | 64         |
| カラム    | 64         |
| 索引     | 64         |
| ビュー    | 64         |
| シーケンス  | 64         |

## データベース、テーブル、ビュー、接続の合計数の制限 {#limitations-on-the-total-number-of-databases-tables-views-and-connections}

| タイプ    | 最大数 |
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

| タイプ     | 上限（デフォルト値）                  |
| :------ | :-------------------------- |
| 列       | デフォルトは1017で、最大4096まで調整できます。 |
| インデックス  | デフォルトは64で、最大512まで調整可能       |
| 行       | 無制限                         |
| サイズ     | 無制限                         |
| パーティション | 8192                        |

<CustomContent platform="tidb">

-   上限値`Columns`は[`table-column-count-limit`](/tidb-configuration-file.md#table-column-count-limit-new-in-v50)で変更できます。
-   上限値`Indexes`は[`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50)で変更できます。

</CustomContent>

## 1行の制限 {#limitation-on-a-single-row}

| タイプ | 上限（デフォルト値）                      |
| :-- | :------------------------------ |
| サイズ | デフォルトは6 MiBですが、120 MiBまで調整可能です。 |

<CustomContent platform="tidb">

[`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)構成項目を介してサイズ制限を調整できます。

</CustomContent>

## インデックスの制限 {#limitations-on-indexes}

インデックスの最大長は3072バイトで、4バイトUTF-8エンコードでは768文字に相当します。1つのインデックスに含まれる列の最大数は16に制限されています。

<CustomContent platform="tidb">

この制限は、 [`max-index-length`](/tidb-configuration-file.md#max-index-length)構成項目を使用して調整できます。

</CustomContent>

## データ型の制限 {#limitations-on-data-types}

| タイプ       | 上限       |
| :-------- | :------- |
| チャー       | 255文字    |
| バイナリ      | 255バイト   |
| VARBINARY | 65535バイト |
| ヴァルチャー    | 16383文字  |
| TEXT      | 65535バイト |
| ブロブ       | 65535バイト |

## SQL文の制限 {#limitations-on-sql-statements}

| タイプ                  | 上限                                                  |
| :------------------- | :-------------------------------------------------- |
| 単一トランザクション内のSQL文の最大数 | 楽観的トランザクションを使用し、トランザクション再試行が有効になっている場合、上限は 5000 です。 |

<CustomContent platform="tidb">

[`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit)構成項目を介して制限を変更できます。

</CustomContent>

## TiKVバージョンの制限 {#limitations-on-tikv-version}

クラスター内の TiDBコンポーネントのバージョンが v6.2.0 以降の場合、TiKV のバージョンも v6.2.0 以降である必要があります。
