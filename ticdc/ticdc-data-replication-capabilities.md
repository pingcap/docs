---
title: TiCDC Data Replication Capabilities
summary: TiCDC のデータ複製機能について学習します。
---

# TiCDC データレプリケーション機能 {#ticdc-data-replication-capabilities}

[TiCDC](/ticdc/ticdc-overview.md) （TiDB Change Data Capture）は、リアルタイムデータレプリケーションを実現するTiDBエコシステムの中核コンポーネントです。このドキュメントでは、TiCDCのデータレプリケーション機能について詳しく説明します。

## TiCDCの仕組み {#how-ticdc-works}

-   TiCDCはTiKV変更ログ（Raftログ）をリッスンし、行レベルのデータ変更（ `INSERT` `DELETE`操作） `UPDATE`下流と互換性のあるSQL文に変換します。TiCDCは上流データベースで実行された元のSQL文に依存しません。詳細については、 [TiCDCがデータ変更を処理する方法](/ticdc/ticdc-overview.md#implementation-of-processing-data-changes)参照してください。

-   TiCDCは、上流データベースで実行された元のSQL文`UPDATE`一つ一つ復元するのではなく、SQLセマンティクスに相当する論理演算（ `INSERT`など）を生成します。詳細については[TiCDCがデータ変更を処理する方法](/ticdc/ticdc-overview.md#implementation-of-processing-data-changes) `DELETE`してください。

-   TiCDCはトランザクションの最終的な一貫性を保証します。1 [再実行ログ](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)有効にすると、TiCDCは災害復旧シナリオにおいて最終的な一貫性を保証できます。3 [同期ポイント](/ticdc/ticdc-upstream-downstream-check.md#enable-syncpoint)有効にすると、TiCDCは一貫性のあるスナップショット読み取りとデータ整合性の検証をサポートします。

## サポートされている下流システム {#supported-downstream-systems}

TiCDC は、次のようなさまざまな下流システムへのデータの複製をサポートしています。

-   [TiDBデータベースまたはその他のMySQL互換データベース](/ticdc/ticdc-sink-to-mysql.md)
-   [アパッチカフカ](/ticdc/ticdc-sink-to-kafka.md)
-   [メッセージキュー（MQ）タイプのシンク](/ticdc/ticdc-changefeed-config.md#sink) 、例えば[パルサー](/ticdc/ticdc-sink-to-pulsar.md)
-   [ストレージ サービス (Amazon S3、GCS、Azure Blob Storage、NFS)](/ticdc/ticdc-sink-to-cloud-storage.md)
-   [Confluent Cloud 統合による Snowflake、ksqlDB、SQL Server](/ticdc/integrate-confluent-using-ticdc.md)
-   [Kafka で複製されたデータを消費するための Apache Flink](/replicate-data-to-kafka.md)

## データ複製の範囲 {#scope-of-data-replication}

TiCDC は、次の種類のアップストリーム データの変更をサポートします。

-   **サポート対象:**

    -   DDL および DML ステートメント (システム テーブルを除く)。
    -   インデックス操作 ( `ADD INDEX` 、 `CREATE INDEX` ): ダウンストリームが TiDB、TiCDC [`ADD INDEX`および`CREATE INDEX` DDL操作を非同期に実行します。](/ticdc/ticdc-ddl.md#asynchronous-execution-of-add-index-and-create-index-ddls)の場合、変更フィードレプリケーションのレイテンシーへの影響を軽減します。
    -   外部キー制約DDL文（ `ADD FOREIGN KEY` ）：TiCDCは上流のシステム変数設定を複製し**ません**。下流の外部キー制約チェックを有効にするには、下流で[`foreign_key_checks`](/system-variables.md#foreign_key_checks)手動で設定する必要があります。また、下流にデータを書き込む際に、TiCDCはセッションレベルの設定`SET SESSION foreign_key_checks = OFF;`自動的に有効にします。したがって、下流でグローバル外部キーチェックが有効になっている場合でも、TiCDCによって書き込まれたデータは外部キー制約の検証をトリガーしません。

-   **サポートされていません**:

    -   アップストリーム システム テーブルで実行された DDL および DML ステートメント ( `mysql.*`および`information_schema.*`を含む)。
    -   アップストリーム一時テーブルで実行された DDL および DML ステートメント。
    -   DQL (データ クエリ言語) および DCL (データ制御言語) ステートメント。

## 制限事項 {#limitations}

-   TiCDCは特定のシナリオをサポートしていません。詳細については[サポートされていないシナリオ](/ticdc/ticdc-overview.md#unsupported-scenarios)参照してください。
-   TiCDCは上流データの変更の整合性のみを検証します。変更が上流または下流の制約に準拠しているかどうかは検証しません。データが下流の制約に違反している場合、TiCDCは下流への書き込み時にエラーを返します。

    たとえば、変更フィードがすべての DDL イベントをフィルターするように構成されている場合、アップストリームが`DROP COLUMN`操作を実行しても、その列に関連する`INSERT`ステートメントの書き込みを継続すると、テーブル スキーマの不一致により、TiCDC はこれらの DML 変更をダウンストリームに複製できません。
