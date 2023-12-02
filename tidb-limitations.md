---
title: TiDB Limitations
summary: Learn the usage limitations of TiDB.
---

# TiDB の制限事項 {#tidb-limitations}

このドキュメントでは、識別子の最大長や、サポートされるデータベース、テーブル、インデックス、パーティション化されたテーブル、シーケンスの最大数など、TiDB の一般的な使用上の制限について説明します。

## 識別子の長さの制限 {#limitations-on-identifier-length}

| 識別子の種類 | 最大長（許可される文字数） |
| :----- | :------------ |
| データベース | 64            |
| テーブル   | 64            |
| カラム    | 64            |
| 索引     | 64            |
| ビュー    | 64            |
| シーケンス  | 64            |

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

| タイプ     | 上限値（デフォルト値）                      |
| :------ | :------------------------------- |
| コラム     | デフォルトは 1017 ですが、最大 4096 まで調整できます |
| インデックス  | デフォルトは 64 ですが、最大 512 まで調整できます    |
| 行       | 無制限                              |
| サイズ     | 無制限                              |
| パーティション | 8192                             |

<CustomContent platform="tidb">

-   `Columns`の上限は[`table-column-count-limit`](/tidb-configuration-file.md#table-column-count-limit-new-in-v50)によって変更できます。
-   上限`Indexes`は[`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50)によって変更できます。

</CustomContent>

## 単一行の制限 {#limitation-on-a-single-row}

| タイプ | 上限値（デフォルト値）                      |
| :-- | :------------------------------- |
| サイズ | デフォルトは 6 MiB ですが、120 MiB に調整可能です |

<CustomContent platform="tidb">

[`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)設定項目でサイズ制限を調整できます。

</CustomContent>

## データ型の制限 {#limitations-on-data-types}

| タイプ     | 上限                               |
| :------ | :------------------------------- |
| チャー     | 256文字                            |
| バイナリ    | 256文字                            |
| ヴァービナリー | 65535文字                          |
| VARCHAR | 16383文字                          |
| TEXT    | デフォルトは 6 MiB ですが、120 MiB に調整可能です |
| BLOB    | デフォルトは 6 MiB ですが、120 MiB に調整可能です |

## SQL ステートメントの制限事項 {#limitations-on-sql-statements}

| タイプ                          | 上限                                            |
| :--------------------------- | :-------------------------------------------- |
| 単一トランザクション内の SQL ステートメントの最大数 | 楽観的トランザクションを使用し、トランザクションリトライが有効な場合、上限は5000です。 |

<CustomContent platform="tidb">

[`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit)設定項目を使用して制限を変更できます。

</CustomContent>

## TiKV バージョンの制限事項 {#limitations-on-tikv-version}

クラスター内で、TiDBコンポーネントのバージョンが v6.2.0 以降である場合、TiKV のバージョンは v6.2.0 以降である必要があります。
