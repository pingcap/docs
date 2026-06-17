---
title: TiCDC Overview
summary: TiCDCとは何か、TiCDCが提供する機能、そしてTiCDCのインストールと展開方法について学びましょう。
---

# TiCDCの概要 {#ticdc-overview}

[TiCDC](https://github.com/pingcap/tiflow/tree/release-8.5/cdc)は、TiDB から増分データをレプリケートするために使用されるツールです。具体的には、TiCDC は TiKV 変更ログを取得し、キャプチャしたデータを並べ替えて、行ベースの増分データをダウンストリーム データベースにエクスポートします。データ レプリケーション機能の詳細については、 [TiCDCのデータレプリケーション機能](/ticdc/ticdc-data-replication-capabilities.md)を参照してください。

## 使用シナリオ {#usage-scenarios}

TiCDCには、以下のような複数の使用シナリオがあります。

-   複数のTiDBクラスタ向けに、高可用性とディザスタリカバリソリューションを提供します。TiCDCは、災害発生時にプライマリクラスタとセカンダリクラスタ間のデータ整合性を確保します。
-   リアルタイムのデータ変更を同種システムに複製します。これにより、監視、キャッシング、グローバルインデックス作成、データ分析、異種データベース間のプライマリ/セカンダリ複製など、さまざまなシナリオに対応するデータソースが提供されます。

## 主な特徴 {#major-features}

### 主な機能 {#key-capabilities}

TiCDCには、以下の主要な機能があります。

-   秒単位のRPOと分単位のRTOで、TiDBクラスタ間で増分データを複製します。
-   TiDBクラスタ間の双方向レプリケーションにより、TiCDCを使用してマルチアクティブTiDBソリューションを構築できます。
-   TiDBクラスタからMySQLデータベースまたはその他のMySQL互換データベースへ、低レイテンシーで増分データを複製します。
-   TiDB クラスターから Kafka クラスターへの増分データのレプリケーション。推奨されるデータ形式には、 [Canal-JSON](/ticdc/ticdc-canal-json.md) 、[Avro](/ticdc/ticdc-avro-protocol.md)、[デベジウム](/ticdc/ticdc-debezium.md)が含まれます。
-   TiDBクラスタからAmazon S3、GCS、Azure Blob Storage、NFSなどのstorageサービスへ増分データを複製する。
-   データベース、テーブル、DML、DDLをフィルタリングする機能を備えたテーブルの複製。
-   単一障害点のない高可用性を実現し、TiCDCノードの動的な追加と削除をサポートします。
-   [オープンAPI](/ticdc/ticdc-open-api-v2.md)を介したクラスタ管理。タスクの状態照会、タスク構成の動的な変更、タスクの作成または削除などが含まれます。

### 複製順序 {#replication-order}

-   TiCDCは、すべてのDDLまたはDMLステートメントを**少なくとも1回**出力します。
-   TiKVまたはTiCDCクラスタで障害が発生した場合、TiCDCは同じDDL/DMLステートメントを繰り返し送信する可能性があります。重複したDDL/DMLステートメントについては、以下を参照してください。

    -   MySQLシンクはDDLステートメントを繰り返し実行できます。 `TRUNCATE TABLE`のようにダウンストリームで繰り返し実行できるDDLステートメントは正常に実行されます。 `CREATE TABLE`のように繰り返し実行できないステートメントは実行に失敗し、TiCDCはエラーを無視してレプリケーション処理を続行します。
    -   Kafkaシンクは、データ配信のためのさまざまな戦略を提供します。
        -   テーブル、主キー、またはタイムスタンプに基づいて、データを異なるKafkaパーティションに分散させることができます。これにより、行の更新されたデータが常に同じパーティションに順番に送信されることが保証されます。
        -   これらの配信戦略はすべて`Resolved TS`メッセージをすべてのトピックとパーティションに定期的に送信します。これは`Resolved TS`より前のすべてのメッセージが既にトピックとパーティションに送信されていることを示しています。Kafka コンシューマーは`Resolved TS`を使用して受信したメッセージをソートできます。
        -   Kafka シンクは重複したメッセージを送信することがありますが、これらの重複メッセージは`Resolved Ts`の制約には影響しません。たとえば、変更フィードが一時停止されてから再開された場合、Kafka シンクは`msg1` 、 `msg2` 、 `msg3` 、 `msg2` 、 `msg3`順番に送信する可能性があります。Kafka コンシューマーから重複メッセージをフィルタリングすることができます。

### レプリケーションの一貫性 {#replication-consistency}

-   MySQLシンク

    -   TiCDCは、データレプリケーションの最終的な整合性を確保するために、リドゥログを有効にします。

    -   TiCDCは、単一行の更新順序がアップストリームと一致することを保証します。

    -   TiCDCは、下流のトランザクションが上流のトランザクションと同じ順序で実行されることを保証しません。

    > **注記：**
    >
    > バージョン6.2以降では、シンクURIパラメータ[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)を使用して、単一テーブルトランザクションを分割するかどうかを制御できます。単一テーブルトランザクションを分割することで、大規模トランザクションのレプリケーションにおけるレイテンシーとメモリ消費量を大幅に削減できます。

## TiCDCアーキテクチャの概要 {#ticdc-architecture-overview}

TiCDCは、PDのetcdを介して高可用性を実現するTiDB用の増分データレプリケーションツールです。レプリケーションプロセスは、以下の手順で構成されます。

1.  複数のTiCDCプロセスがTiKVノードからデータ変更を取得します。
2.  TiCDCはデータの変更を分類して統合します。
3.  TiCDCは、複数のレプリケーションタスク（チェンジフィード）を通じて、データの変更を複数の下流システムに複製します。

TiCDCのアーキテクチャを次の図に示す。

![TiCDC architecture](/media/ticdc/cdc-architecture.png)

アーキテクチャ図における各構成要素は、以下のように説明されます。

-   TiKVサーバー：TiDBクラスタ内のTiKVノード。データに変更が発生すると、TiKVノードは変更ログ（KV変更ログ）として変更内容をTiCDCノードに送信します。TiCDCノードは、変更ログが連続していないことを検出した場合、TiKVノードに変更ログの提供を積極的に要求します。
-   TiCDC: TiCDCプロセスが実行されるTiCDCノード。各ノードではTiCDCプロセスが実行されます。各プロセスは、TiKVノード内の1つ以上のテーブルからデータ変更を取得し、シンクコンポーネントを介して下流システムにその変更を複製します。
-   PD：TiDBクラスタのスケジューリングモジュール。このモジュールはクラスタデータのスケジューリングを担当し、通常は3つのPDノードで構成されます。PDはetcdクラスタを介して高可用性を提供します。etcdクラスタでは、TiCDCはノードの状態情報や変更フィードの設定などのメタデータを保存します。

実装では、TiCDC の[新しいアーキテクチャ](/ticdc/ticdc-architecture.md)と[古典アーキテクチャ](/ticdc/ticdc-classic-architecture.md)両方が、同じ増分データ レプリケーション モデルに基づいて構築されます。クラシックアーキテクチャと比較して、新しいアーキテクチャはタスク スケジューリングとレプリケーション メカニズムをリファクタリングして最適化し、リソース コストを削減しながら、リアルタイム データ レプリケーションのパフォーマンス、スケーラビリティ、安定性を大幅に向上させます。

アーキテクチャ図に示すように、TiCDCはTiDB、MySQL、Kafka、およびstorageサービスへのデータ複製をサポートしています。

## 有効なインデックス {#valid-index}

一般的に、TiCDC は有効なインデックスを少なくとも 1 つ持つテーブルのみをダウンストリームにレプリケートします。テーブル内のインデックスが以下のいずれかの要件を満たしている場合、そのインデックスは有効です。

-   プライマリキー（ `PRIMARY KEY` ）は有効なインデックスです。
-   一意のインデックス ( `UNIQUE INDEX` ) は、インデックスのすべての列が明示的に非 null 許容 ( `NOT NULL` ) として定義され、インデックスに仮想生成列 ( `VIRTUAL GENERATED COLUMNS` ) がない場合に有効です。

> **注記：**
>
> [`force-replicate`](/ticdc/ticdc-changefeed-config.md#force-replicate) `true`に設定すると、TiCDC は[有効なインデックスのないテーブルを複製する](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index)。

## ベストプラクティス {#best-practices}

-   TiCDCを使用して2つのTiDBクラスタ間でデータを複製する場合、2つのクラスタ間のネットワークレイテンシーが100msを超えると、次のようになります。

    -   TiCDCのバージョンがv6.5.2より前の場合は、下流のTiDBクラスタが配置されているリージョン（IDC）にTiCDCをデプロイすることをお勧めします。
    -   TiCDC v6.5.2以降に導入された一連の改善により、TiCDCは上流のTiDBクラスタが配置されているリージョン（IDC）にデプロイすることが推奨されます。

-   TiCDC によって複製される各テーブルには、少なくとも 1 つの[有効なインデックス](#valid-index)があります。

-   TiCDC をディザスタリカバリに使用する際に最終的な整合性を確保するには、 [リドゥログ](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)を設定し、上流で災害が発生した場合でも、リドゥログが書き込まれるstorageシステムが正常に読み取れるようにする必要があります。

## データ処理変更の実装 {#implementation-of-processing-data-changes}

このセクションでは主に、TiCDCが上流のDML操作によって生成されたデータ変更をどのように処理するかについて説明します。

上流の DDL 操作によって生成されたデータ変更については、TiCDC は完全な DDL SQL ステートメントを取得し、下流のシンクタイプに基づいて対応する形式に変換して、下流に送信します。このセクションでは、これについては詳しく説明しません。

> **注記：**
>
> TiCDCがデータ変更を処理するロジックは、今後のバージョンで調整される可能性があります。

MySQLのbinlogは、アップストリームで実行されたすべてのDML SQLステートメントを直接記録します。MySQLとは異なり、TiCDCはアップストリームTiKVの各リージョンRaftログのリアルタイム情報を監視し、各トランザクションの前後のデータの差分に基づいてデータ変更情報を生成します。この差分は複数のSQLステートメントに対応します。TiCDCは、出力変更イベントがアップストリームTiDBの変更と同等であることのみを保証し、アップストリームTiDBのデータ変更を引き起こしたSQLステートメントを正確に復元できることを保証するものではありません。

データ変更情報には、データ変更の種類と、変更前後のデータ値が含まれます。トランザクション前後のデータの違いによって、次の3種類のイベントが発生する可能性があります。

1.  `DELETE`イベント: `DELETE`タイプのデータ変更メッセージに対応し、変更前のデータが含まれています。

2.  `INSERT`イベント: `PUT`タイプのデータ変更メッセージに対応し、変更後のデータが含まれます。

3.  `UPDATE`イベント: `PUT`タイプのデータ変更メッセージに対応し、変更前と変更後の両方のデータが含まれます。

TiCDCは、データ変更情報に基づいて、さまざまなダウンストリームタイプに適した形式でデータを生成し、ダウンストリームに送信します。例えば、Canal-JSONやAvroなどの形式でデータを生成してKafkaに書き込んだり、データをSQL文に変換してダウンストリームのMySQLやTiDBに送信したりします。

現在、TiCDC が対応するプロトコルのデータ変更情報を適応させる場合、特定の`UPDATE`イベントについて、それらのイベントを 1 つの`DELETE`イベントと 1 つの`INSERT`イベントに分割する場合があります。詳細については、 [MySQLシンクの`UPDATE`イベントを分割する](/ticdc/ticdc-split-update-behavior.md#split-update-events-for-mysql-sinks)および[MySQL以外のシンクにおける、主キーまたは一意キーを分割した`UPDATE`イベント](/ticdc/ticdc-split-update-behavior.md#split-primary-or-unique-key-update-events-for-non-mysql-sinks)参照してください。

ダウンストリームがMySQLまたはTiDBの場合、TiCDCはダウンストリームに書き込まれるSQL文がアップストリームで実行されるSQL文と完全に一致することを保証できません。これは、TiCDCがアップストリームで実行される元のDML文を直接取得するのではなく、データ変更情報に基づいてSQL文を生成するためです。ただし、TiCDCは最終結果の一貫性を保証します。

例えば、アップストリームでは次のSQL文が実行されます。

```sql
Create Table t1 (A int Primary Key, B int);

BEGIN;
Insert Into t1 values(1,2);
Insert Into t1 values(2,2);
Insert Into t1 values(3,3);
Commit;

Update t1 set b = 4 where b = 2;
```

TiCDCは、データ変更情報に基づいて以下の2つのSQL文を生成し、下流に書き込みます。

```sql
INSERT INTO `test.t1` (`A`,`B`) VALUES (1,2),(2,2),(3,3);
UPDATE `test`.`t1`
SET `A` = CASE
        WHEN `A` = 1 THEN 1
        WHEN `A` = 2 THEN 2
END, `B` = CASE
        WHEN `A` = 1 THEN 4
        WHEN `A` = 2 THEN 4
END
WHERE `A` = 1 OR `A` = 2;
```

## サポートされていないシナリオ {#unsupported-scenarios}

現在、以下のシナリオはサポートされていません。

-   RawKVのみを使用するTiKVクラスター。
-   TiDB の[`CREATE SEQUENCE` DDL操作](/sql-statements/sql-statement-create-sequence.md)と[`SEQUENCE`関数](/sql-statements/sql-statement-create-sequence.md#sequence-function)上流の TiDB が`SEQUENCE`を使用している場合、TiCDC は上流で実行された`SEQUENCE` DDL 操作/関数を無視します。ただし、 `SEQUENCE`関数を使用した DML 操作は正しく複製できます。
-   現在、TiCDC によってレプリケートされているテーブルおよびデータベースへの[TiDB Lightning物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を使用したデータのインポートはサポートされていません。詳細については、 [TiDB Lightningの物理インポートモードとTiCDCの互換性に関する制限事項は何ですか？](/ticdc/ticdc-faq.md#what-are-the-compatibility-limitations-between-tidb-lightning-physical-import-mode-and-ticdc)参照してください。
-   v8.2.0 より前では、 BR はTiCDC レプリケーション タスクを使用するクラスター[データの復元](/br/backup-and-restore-overview.md)サポートしていません。詳細については、 [BR （バックアップ＆リストア）とTiCDCの互換性に関する制限事項は何ですか？](/ticdc/ticdc-faq.md#what-are-the-compatibility-limitations-between-br-and-ticdc)参照してください。
-   バージョン8.2.0以降、 BRはTiCDCのデータ復元に関する制限を緩和しました。復元対象データの`BackupTS` （バックアップ時刻）がchangefeed [`CheckpointTS`](/ticdc/ticdc-classic-architecture.md#checkpointts) （現在のレプリケーションの進行状況を示すタイムスタンプ）よりも前であれば、 BRは正常にデータ復元を進めることができます。 `BackupTS`は通常かなり前であることを考慮すると、ほとんどのシナリオにおいて、 BRはTiCDCレプリケーションタスクを持つクラスタのデータ復元をサポートしていると考えられます。

TiCDCは、アップストリームにおける大規模トランザクションを含むシナリオを部分的にのみサポートしています。詳細については、 [TiCDCに関するFAQ](/ticdc/ticdc-faq.md#does-ticdc-support-replicating-large-transactions-is-there-any-risk)を参照してください。FAQでは、TiCDCが大規模トランザクションのレプリケーションをサポートしているかどうか、および関連するリスクについて詳しく説明されています。

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="TiDB Admin Lab 11: Replicating TiDB Change Events Using TiCDC" type="lab" link="https://labs.tidb.io/labs/dba_303_lab_ff10" imgSrc="https://lab-static.pingcap.com/quick-demo/dba_303_ch12_en.png" duration="60 mins" />
</RelatedResources>
