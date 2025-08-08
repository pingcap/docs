---
title: Batch Processing
summary: パイプライン DML、非トランザクション DML、IMPORT INTO` ステートメント、非推奨の batch-dml 機能など、TiDB のバッチ処理機能を紹介します。
---

# バッチ処理 {#batch-processing}

バッチ処理は、実世界のシナリオにおいて一般的かつ不可欠な操作です。データ移行、一括インポート、アーカイブ、大規模な更新といったタスクにおいて、大規模なデータセットを効率的に処理することを可能にします。

バッチ操作のパフォーマンスを最適化するために、TiDB はバージョンの進化とともにさまざまな機能を導入しています。

-   データのインポート
    -   `IMPORT INTO`ステートメント (TiDB v7.2.0 で導入され、v7.5.0 で GA になりました)
-   データの挿入、更新、削除
    -   パイプライン DML (実験的、TiDB v8.0.0 で導入)
    -   非トランザクションDML（TiDB v6.1.0で導入）
    -   Batch-dml（非推奨）

このドキュメントでは、これらの機能の主な利点、制限事項、使用例について概説し、効率的なバッチ処理に最適なソリューションを選択できるようにします。

## データのインポート {#data-import}

`IMPORT INTO`ステートメントはデータインポートタスク用に設計されています。これにより、CSV、SQL、PARQUET などの形式のデータを空の TiDB テーブルに迅速にインポートでき、 [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)別途デプロイする必要はありません。

### 主なメリット {#key-benefits}

-   非常に高速なインポート速度
-   TiDB Lightningと比べて使いやすい

### 制限事項 {#limitations}

<CustomContent platform="tidb">

-   [ACID](/glossary.md#acid)保証なし
-   Subject to various usage restrictions

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)保証なし
-   さまざまな使用制限の対象となります

</CustomContent>

### ユースケース {#use-cases}

-   データの移行や復旧などのデータインポートシナリオに適しています。該当する場合は、 TiDB Lightningではなく`IMPORT INTO`使用することをお勧めします。

詳細については[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)参照してください。

## データの挿入、更新、削除 {#data-inserts-updates-and-deletions}

### パイプラインDML {#pipelined-dml}

パイプラインDMLは、TiDB v8.0.0で導入された実験的機能です。v8.5.0では、この機能が強化され、パフォーマンスが大幅に向上しました。

#### 主なメリット {#key-benefits}

-   Streams data to the storage layer during transaction execution instead of buffering it entirely in memory, allowing transaction size no longer limited by TiDB memory and supporting ultra-large-scale data processing
-   標準のDMLに比べて優れたパフォーマンスを実現
-   SQL を変更せずにシステム変数を通じて有効にすることができます

#### 制限事項 {#limitations}

-   [自動コミット](/transaction-overview.md#autocommit) `INSERT` `DELETE`のみ`UPDATE`サポートします`REPLACE`

#### ユースケース {#use-cases}

-   大量のデータの挿入、更新、削除などの一般的なバッチ処理タスクに適しています。

詳細については[パイプラインDML](/pipelined-dml.md)参照してください。

### 非トランザクションDMLステートメント {#non-transactional-dml-statements}

非トランザクションDMLはTiDB v6.1.0で導入されました。当初は`DELETE`ステートメントのみがこの機能をサポートしています。v6.5.0以降では、 `INSERT` 、 `REPLACE` 、 `UPDATE`ステートメントもこの機能をサポートします。

#### 主なメリット {#key-benefits}

-   メモリ制限を回避して、単一の SQL ステートメントを複数の小さなステートメントに分割します。
-   標準の DML よりもわずかに高速、または同等のパフォーマンスを実現します。

#### 制限事項 {#limitations}

-   [自動コミット](/transaction-overview.md#autocommit)ステートメントのみをサポートします
-   SQL文の変更が必要
-   SQL 構文に厳しい要件を課すため、一部のステートメントは書き直しが必要になる場合があります。
-   完全なトランザクションACID保証がないため、障害発生時には文が部分的に実行される可能性がある。

#### ユースケース {#use-cases}

-   大量のデータの挿入、更新、削除を伴うシナリオに適しています。ただし、その制限のため、パイプラインDMLが適用できない場合にのみ、非トランザクションDMLを検討することをお勧めします。

詳細については[非トランザクションDML](/non-transactional-dml.md)参照してください。

### 非推奨のbatch-dml機能 {#deprecated-batch-dml-feature}

TiDB v4.0より前のバージョンで利用可能だったbatch-dml機能は非推奨となり、推奨されなくなりました。この機能は、以下のシステム変数によって制御されます。

-   `tidb_batch_insert`
-   `tidb_batch_delete`
-   `tidb_batch_commit`
-   `tidb_enable_batch_dml`
-   `tidb_dml_batch_size`

データとインデックスの不一致によってデータが破損または失われるリスクがあるため、これらの変数は非推奨となり、将来のリリースでは削除される予定です。

いかなる状況においても、非推奨のbatch-dml機能の使用は**推奨されません**。代わりに、このドキュメントで概説されている他の代替機能の使用をご検討ください。
