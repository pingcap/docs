---
title: Compatibility Catalog of TiDB Data Migration
summary: This document describes the compatibility between DM of different versions and upstream/downstream databases.
---

# TiDB データ移行の互換性カタログ {#compatibility-catalog-of-tidb-data-migration}

DM は、さまざまなソースから TiDB クラスターへのデータの移行をサポートしています。データ ソースの種類に基づいて、DM には次の 4 つの互換性レベルがあります。

-   **一般公開 (GA)** : アプリケーション シナリオが検証され、GA テストに合格しました。
-   **Experimental**: アプリケーション シナリオは検証されていますが、テストはすべてのシナリオをカバーしていないか、限られた数のユーザーのみを対象としています。アプリケーション シナリオで問題が発生する場合があります。
-   **テストされていません**: DM は反復中に常に MySQL と互換性があることが期待されます。ただし、リソースの制約により、すべての MySQL フォークが DM でテストされているわけではありません。したがって、*テストされていない*ソースまたはターゲットは DM と技術的に互換性がありますが、完全にはテストされていません。つまり、使用する前に互換性を確認する必要があります。
-   **非互換性**: DM はデータ ソースと互換性がないことが証明されており、アプリケーションを本番環境で使用することはお勧めしません。

## データソース {#data-sources}

| 情報元                    | 互換性レベル       | 備考                   |
| ---------------------- | ------------ | -------------------- |
| MySQL ≤ 5.5            | 未検証          |                      |
| MySQL 5.6              | GA           |                      |
| MySQL 5.7              | GA           |                      |
| MySQL 8.0              | Experimental |                      |
| MariaDB &lt; 10.1.2    | 非互換          | 時間型のbinlogと互換性がありません |
| マリアDB 10.1.2 ~ 10.5.10 | Experimental |                      |
| MariaDB &gt; 10.5.10   | 非互換          | チェック手順で報告された権限エラー    |

## 対象データベース {#target-databases}

> **警告：**
>
> DM v5.3.0 は推奨されません。 DM v5.3.0 で GTID レプリケーションを有効にしてもリレー ログを有効にしない場合、データのレプリケーションは低い確率で失敗します。

| 対象データベース | 互換性レベル       | DM版               |
| -------- | ------------ | ----------------- |
| TiDB 6.0 | GA           | ≧5.3.1            |
| TiDB 5.4 | GA           | ≧5.3.1            |
| TiDB 5.3 | GA           | ≧5.3.1            |
| TiDB 5.2 | GA           | ≥ 2.0.7、推奨: 5.4   |
| TiDB 5.1 | GA           | ≥ 2.0.4、推奨: 5.4   |
| TiDB 5.0 | GA           | ≥ 2.0.4、推奨: 5.4   |
| TiDB 4.x | GA           | ≥ 2.0.1、推奨: 2.0.7 |
| TiDB 3.x | GA           | ≥ 2.0.1、推奨: 2.0.7 |
| MySQL    | Experimental |                   |
| マリアDB    | Experimental |                   |
