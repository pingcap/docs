---
title: Pipelined DML
summary: パイプラインDMLのユースケース、メソッド、制限事項、FAQを紹介します。パイプラインDMLはTiDBのバッチ処理機能を強化し、トランザクションサイズがTiDBのメモリ制限を回避できるようにします。
---

# パイプラインDML {#pipelined-dml}

> **警告：**
>
> パイプラインDMLは実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

このドキュメントでは、パイプライン DML に関連するユースケース、方法、制限、および一般的な問題について説明します。

## 概要 {#overview}

パイプラインDMLは、大規模データ書き込み操作のパフォーマンスを向上させるためにTiDB v8.0.0で導入された実験的機能です。この機能を有効にすると、TiDBはDML操作中にデータをメモリに完全にバッファリングするのではなく、storageレイヤーに直接ストリーミングします。このパイプラインのようなアプローチは、データの読み取り（入力）とstorageレイヤーへの書き込み（出力）を同時に行うことで、大規模DML操作における一般的な課題を以下のように効果的に解決します。

-   メモリ制限: 従来の DML 操作では、大規模なデータセットを処理するときにメモリ不足 (OOM) エラーが発生する可能性があります。
-   パフォーマンスのボトルネック: 大規模なトランザクションは非効率になることが多く、ワークロードの変動を引き起こしやすくなります。

パイプライン DML を有効にすると、次のことを実現できます。

-   TiDB のメモリ制限に制約されることなく、大規模なデータ操作を実行します。
-   よりスムーズなワークロードを管理、操作のレイテンシーを短縮します。
-   トランザクションメモリの使用量を予測可能に保ちます (通常は 1 GiB 以内)。

次のシナリオでは、パイプライン DML を有効にすることをお勧めします。

-   数百万行以上のデータ書き込みを処理します。
-   DML 操作中にメモリ不足エラーが発生しました。
-   大規模なデータ操作中に顕著なワークロードの変動が発生します。

パイプライン DML によりトランザクション処理中のメモリ使用量が大幅に削減されますが、大規模なデータ操作中に他のコンポーネント (エグゼキュータなど) が適切に機能することを保証するには、 [適切なメモリ閾値](/system-variables.md#tidb_mem_quota_query) (少なくとも 2 GiB を推奨) を構成する必要があることに注意してください。

## 制限事項 {#limitations}

現在、パイプライン DML には次の制限があります。

-   パイプラインDMLは現在、TiCDC、 TiFlash、またはBRと互換性がありません。これらのコンポーネントに関連付けられたテーブルではパイプラインDMLを使用しないでください。これらのコンポーネントでブロッキングやOOMなどの問題が発生する可能性があります。
-   パイプライン DML は、パフォーマンスの大幅な低下やロールバックを必要とする操作の失敗につながる可能性があるため、書き込み競合が発生するシナリオには適していません。
-   パイプライン DML 操作中に[メタデータロック](/metadata-lock.md)が有効になっていることを確認します。
-   パイプラインDMLを有効にしてDML文を実行する際、TiDBは以下の条件をチェックします。いずれかの条件が満たされない場合、TiDBは標準のDML実行にフォールバックし、警告を生成します。
    -   サポートされるステートメントは[自動コミット](/transaction-overview.md#autocommit)だけです。
    -   `INSERT` 、 `REPLACE` `DELETE` `UPDATE`のみがサポートされます。
    -   ターゲット テーブルには[一時テーブル](/temporary-tables.md)または[キャッシュされたテーブル](/cached-tables.md)含めることはできません。
    -   [外部キー制約](/foreign-key.md)有効になっている場合（ `foreign_key_checks = ON` ）、ターゲットテーブルに外部キー関係を含めることはできません。
-   `INSERT IGNORE ... ON DUPLICATE KEY UPDATE`ステートメントを実行すると、競合する更新によって`Duplicate entry`エラーが発生する可能性があります。

## 使用法 {#usage}

このセクションでは、パイプライン DML を有効にして、それが有効かどうかを確認する方法について説明します。

### パイプラインDMLを有効にする {#enable-pipelined-dml}

パイプライン DML は、次のいずれかの方法で有効にできます。

-   現在のセッションでパイプライン DML を有効にするには、 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)変数を`"bulk"`に設定します。

    ```sql
    SET tidb_dml_type = "bulk";
    ```

-   特定のステートメントに対してパイプライン DML を有効にするには、ステートメントに[`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value)ヒントを追加します。

    -   データアーカイブの例:

        ```sql
        INSERT /*+ SET_VAR(tidb_dml_type='bulk') */ INTO target_table SELECT * FROM source_table;
        ```

    -   一括データ更新の例:

        ```sql
        UPDATE /*+ SET_VAR(tidb_dml_type='bulk') */ products
        SET price = price * 1.1
        WHERE category = 'electronics';
        ```

    -   一括削除の例:

        ```sql
        DELETE /*+ SET_VAR(tidb_dml_type='bulk') */ FROM logs WHERE log_time < '2023-01-01';
        ```

### パイプラインDMLの検証 {#verify-pipelined-dml}

DML ステートメントを実行した後、 [`tidb_last_txn_info`](/system-variables.md#tidb_last_txn_info-new-in-v409)変数をチェックすることで、ステートメントの実行にパイプライン DML が使用されているかどうかを確認できます。

```sql
SELECT @@tidb_last_txn_info;
```

出力の`pipelined`フィールドが`true`場合、パイプライン DML が正常に使用されていることを示します。

## ベストプラクティス {#best-practices}

-   Executorなどのコンポーネントのメモリ使用量が制限を超えないように、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)の値を少し増やしてください。少なくとも2GiBの値を推奨します。十分なTiDBメモリがある環境では、この値をさらに増やすことができます。
-   新しいテーブルにデータを挿入するシナリオでは、パイプラインDMLのパフォーマンスがホットスポットの影響を受ける可能性があります。最適なパフォーマンスを実現するには、事前にホットスポットに対処することをお勧めします。詳細については、 [ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)参照してください。

## 関連構成 {#related-configurations}

<CustomContent platform="tidb">

-   [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)システム変数は、パイプライン DML がセッション レベルで有効かどうかを制御します。
-   [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) `"bulk"`に設定すると、 [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成項目は`false`に設定されているかのように動作します。
-   パイプライン DML を使用して実行されるトランザクションは、TiDB 構成項目[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)で指定されたサイズ制限の対象ではありません。
-   パイプラインDMLを使用して実行される大規模なトランザクションでは、トランザクションの実行時間が長くなる可能性があります。このような場合、トランザクションロックの最大TTLは[`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl)または24時間のいずれか大きい方の値になります。
-   トランザクションの実行時間が[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)で設定された値を超えると、ガベージコレクション(GC) によってトランザクションが強制的にロールバックされ、失敗する可能性があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)システム変数は、パイプライン DML がセッション レベルで有効かどうかを制御します。
-   [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) `"bulk"`に設定すると、 [`pessimistic-auto-commit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#pessimistic-auto-commit-new-in-v600)構成項目は`false`に設定されているかのように動作します。
-   パイプライン DML を使用して実行されるトランザクションは、TiDB 構成項目[`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit)で指定されたサイズ制限の対象ではありません。
-   パイプラインDMLを使用して実行される大規模なトランザクションでは、トランザクションの実行時間が長くなる可能性があります。このような場合、トランザクションロックの最大TTLは[`max-txn-ttl`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#max-txn-ttl)または24時間のいずれか大きい方の値になります。
-   トランザクションの実行時間が[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)で設定された値を超えると、ガベージコレクション(GC) によってトランザクションが強制的にロールバックされ、失敗する可能性があります。

</CustomContent>

## パイプラインDMLを監視する {#monitor-pipelined-dml}

次の方法を使用して、パイプライン DML の実行を監視できます。

-   パイプライン DML が使用されたかどうかなど、現在のセッションで実行された最後のトランザクションに関する情報を取得するには、 [`tidb_last_txn_info`](/system-variables.md#tidb_last_txn_info-new-in-v409)システム変数を確認します。
-   TiDB ログで`"[pipelined dml]"`含む行を探して、現在のステージや書き込まれたデータの量など、パイプライン DML の実行プロセスと進行状況を把握します。
-   長時間実行されるステートメントの進行状況を追跡するには、 [`expensive query`](https://docs.pingcap.com/tidb/stable/identify-expensive-queries#expensive-query-log-example)ログの`affected rows`フィールドをビュー。
-   トランザクションの実行状況を確認するには、 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)テーブルをクエリします。パイプラインDMLは通常、大規模なトランザクションで使用されるため、このテーブルを使用して実行状況を監視することができます。

## よくある質問 {#faqs}

### パイプライン DML を使用してクエリが実行されなかったのはなぜですか? {#why-wasn-t-my-query-executed-using-pipelined-dml}

TiDBがパイプラインDMLを使用したステートメントの実行を拒否した場合、それに応じた警告メッセージが生成されます。1 `SHOW WARNINGS;`実行すると警告の内容を確認し、原因を特定できます。

一般的な理由:

-   DML ステートメントは自動コミットされません。
-   ステートメントには、 [一時テーブル](/temporary-tables.md)や[キャッシュされたテーブル](/cached-tables.md)などのサポートされていないテーブル タイプが含まれています。
-   操作には外部キーが関係し、外部キーのチェックが有効になっています。

### パイプライン DML はトランザクションの分離レベルに影響しますか? {#does-pipelined-dml-affect-the-isolation-level-of-transactions}

いいえ。パイプライン DML はトランザクション中のデータ書き込みメカニズムを変更するだけで、TiDB トランザクションの分離保証には影響しません。

### パイプライン DML を有効にした後でもメモリ不足 (OOM) エラーが発生するのはなぜですか? {#why-do-i-still-encounter-out-of-memory-oom-errors-after-enabling-pipelined-dml}

パイプライン DML が有効になっている場合でも、メモリ制限の問題によってクエリが終了する可能性があります。

    The query has been canceled due to exceeding the memory limit allowed for a single SQL query. Please try to narrow the query scope or increase the tidb_mem_quota_query limit, and then try again.

このエラーは、パイプラインDMLがトランザクション実行中のデータによるメモリ使用量のみを制御するために発生します。しかし、ステートメント実行中に消費されるメモリの総量には、エグゼキューターなどの他のコンポーネントによって使用されるメモリも含まれます。必要なメモリの総量がTiDBのメモリ制限を超えると、メモリ不足（OOM）エラーが発生する可能性があります。

ほとんどの場合、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)値を大きくすることでこの問題を解決できます。推奨値は2GiB以上です。複雑な演算子を含むSQL文や大規模なデータセットを扱うSQL文の場合は、この値をさらに大きくする必要があるかもしれません。

## もっと詳しく知る {#learn-more}

<CustomContent platform="tidb">

-   [バッチ処理](/batch-processing.md)
-   [TiDB メモリ制御](/configure-memory-usage.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [バッチ処理](/batch-processing.md)
-   [TiDB メモリ制御](https://docs.pingcap.com/tidb/stable/configure-memory-usage)

</CustomContent>
