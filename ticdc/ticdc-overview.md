---
title: TiCDC Overview
summary: TiCDC とは何か、TiCDC が提供する機能、TiCDC をインストールして展開する方法について学習します。
---

# TiCDCの概要 {#ticdc-overview}

[TiCDC](https://github.com/pingcap/tiflow/tree/release-8.1/cdc) 、TiDBから増分データを複製するためのツールです。具体的には、TiCDCはTiKVの変更ログを取得し、キャプチャしたデータをソートし、行ベースの増分データを下流のデータベースにエクスポートします。データ複製機能の詳細については、 [TiCDC データレプリケーション機能](/ticdc/ticdc-data-replication-capabilities.md)参照してください。

## 使用シナリオ {#usage-scenarios}

TiCDC には、次のような複数の使用シナリオがあります。

-   複数の TiDB クラスターに高可用性と災害復旧ソリューションを提供します。TiCDC は、災害発生時にプライマリ クラスターとセカンダリ クラスター間の最終的なデータ整合性を保証します。
-   リアルタイムのデータ変更を同種システムに複製します。これにより、監視、キャッシュ、グローバルインデックス作成、データ分析、異種データベース間のプライマリ-セカンダリレプリケーションなど、さまざまなシナリオに対応するデータソースが提供されます。

## 主な特徴 {#major-features}

### 主な機能 {#key-capabilities}

TiCDC には次の主な機能があります。

-   秒レベルの RPO と分レベルの RTO を使用して、TiDB クラスター間で増分データをレプリケートします。
-   TiDB クラスター間の双方向レプリケーションにより、TiCDC を使用したマルチアクティブ TiDB ソリューションの作成が可能になります。
-   TiDB クラスターから MySQL データベースまたはその他の MySQL 互換データベースに低レイテンシーで増分データを複製します。
-   TiDBクラスターからKafkaクラスターへの増分データのレプリケーション。推奨されるデータ形式[デベジウム](/ticdc/ticdc-debezium.md) [運河-JSON](/ticdc/ticdc-canal-json.md) [アブロ](/ticdc/ticdc-avro-protocol.md)
-   TiDB クラスターから Amazon S3、GCS、Azure Blob Storage、NFS などのstorageサービスに増分データを複製します。
-   データベース、テーブル、DML、DDL をフィルターする機能を使用してテーブルを複製します。
-   単一障害点のない高可用性、TiCDC ノードの動的な追加と削除をサポートします。
-   タスク ステータスの照会、タスク構成の動的な変更、タスクの作成または削除など、 [オープンAPI](/ticdc/ticdc-open-api-v2.md)を介したクラスタ管理。

### 複製順序 {#replication-order}

-   すべての DDL または DML ステートメントについて、TiCDC はそれらを**少なくとも 1 回**出力します。
-   TiKVまたはTiCDCクラスターで障害が発生すると、TiCDCは同じDDL/DML文を繰り返し送信することがあります。重複したDDL/DML文については、以下のようになります。

    -   MySQLシンクはDDL文を繰り返し実行できます。1 `TRUNCATE TABLE`ように下流で繰り返し実行できるDDL文は正常に実行されます。3 `CREATE TABLE`ように繰り返し実行できないDDL文は実行に失敗し、TiCDCはエラーを無視してレプリケーションプロセスを続行します。
    -   Kafka シンクは、データ分散のためのさまざまな戦略を提供します。
        -   テーブル、主キー、またはタイムスタンプに基づいて、データを異なるKafkaパーティションに分散できます。これにより、行の更新データが順番に同じパーティションに送信されるようになります。
        -   これらの分散戦略はすべて、すべてのトピックとパーティションに定期的に`Resolved TS`メッセージを送信します。これは、 `Resolved TS`より前のすべてのメッセージが既にトピックとパーティションに送信されていることを示します。Kafkaコンシューマーは`Resolved TS`使用して受信したメッセージをソートできます。
        -   Kafkaシンクは重複したメッセージを送信することがありますが、これらの重複メッセージは`Resolved Ts`の制約には影響しません。例えば、変更フィードが一時停止されてから再開された場合、Kafkaシンクは`msg1` 、 `msg2` 、 `msg3` 、 `msg2` 、 `msg3`の順に送信する可能性があります。Kafkaコンシューマーから重複メッセージをフィルタリングできます。

### レプリケーションの一貫性 {#replication-consistency}

-   MySQLシンク

    -   TiCDC は、REDO ログを有効にして、データ レプリケーションの最終的な一貫性を保証します。

    -   TiCDC は、単一行の更新の順序がアップストリームと一貫していることを保証します。

    -   TiCDC では、ダウンストリーム トランザクションがアップストリーム トランザクションと同じ順序で実行されることは保証されません。

    > **注記：**
    >
    > バージョン6.2以降、シンクURIパラメータ[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)を使用して、単一テーブルトランザクションを分割するかどうかを制御できます。単一テーブルトランザクションを分割することで、大規模トランザクションのレプリケーションにおけるレイテンシーとメモリ消費を大幅に削減できます。

## TiCDCアーキテクチャ {#ticdc-architecture}

TiCDCは、PDのetcdを通じて高可用性を実現するTiDB用の増分データレプリケーションツールです。レプリケーションプロセスは、以下のステップで構成されます。

1.  複数の TiCDC プロセスが TiKV ノードからデータの変更をプルします。
2.  TiCDC はデータの変更を並べ替えてマージします。
3.  TiCDC は、複数のレプリケーション タスク (変更フィード) を通じて、データの変更を複数の下流システムに複製します。

TiCDC のアーキテクチャは次の図に示されています。

![TiCDC architecture](/media/ticdc/cdc-architecture.png)

アーキテクチャ図のコンポーネントは次のように説明されます。

-   TiKVサーバー：TiDBクラスター内のTiKVノード。データ変更が発生すると、TiKVノードは変更内容を変更ログ（KV変更ログ）としてTiCDCノードに送信します。TiCDCノードは変更ログが連続していないことを検出すると、TiKVノードに変更ログの提供を積極的に要求します。
-   TiCDC: TiCDCプロセスが実行されるTiCDCノード。各ノードはTiCDCプロセスを実行します。各プロセスは、TiKVノード内の1つ以上のテーブルからデータ変更を取得し、シンクコンポーネントを介して下流システムに変更を複製します。
-   PD: TiDBクラスタ内のスケジューリングモジュール。このモジュールはクラスタデータのスケジューリングを担当し、通常は3つのPDノードで構成されます。PDはetcdクラスタを通じて高可用性を提供します。etcdクラスタでは、TiCDCがノードステータス情報や変更フィード設定などのメタデータを保存します。

アーキテクチャ図に示されているように、TiCDC は TiDB、MySQL、Kafka、およびstorageサービスへのデータの複製をサポートしています。

## ベストプラクティス {#best-practices}

-   TiCDC を使用して 2 つの TiDB クラスター間でデータをレプリケートする場合、2 つのクラスター間のネットワークレイテンシーが100 ミリ秒を超えると、次のようになります。

    -   v6.5.2 より前のバージョンの TiCDC の場合、ダウンストリーム TiDB クラスターが配置されているリージョン (IDC) に TiCDC をデプロイすることをお勧めします。
    -   TiCDC v6.5.2 から導入された一連の改善により、アップストリーム TiDB クラスターが配置されているリージョン (IDC) に TiCDC を展開することが推奨されます。

-   TiCDCは、少なくとも1つの有効なインデックスを持つテーブルのみを複製します。有効なインデックスは以下のように定義されます。

    -   主キー（ `PRIMARY KEY` ）は有効なインデックスです。
    -   ユニークインデックス（ `UNIQUE INDEX` ）は、インデックスのすべての列が明示的にNULL値不可として定義され（ `NOT NULL` ）、かつインデックスに仮想生成列（ `VIRTUAL GENERATED COLUMNS` ）がない場合に有効です。

-   TiCDC を災害復旧に使用する場合、最終的な一貫性を確保するには、 [再実行ログ](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)設定し、上流で災害が発生したときに、REDO ログが書き込まれるstorageシステムを正常に読み取ることができるようにする必要があります。

## 処理データの変更の実装 {#implementation-of-processing-data-changes}

このセクションでは主に、TiCDC がアップストリーム DML 操作によって生成されたデータ変更を処理する方法について説明します。

上流のDDL操作によって生成されたデータ変更については、TiCDCは完全なDDL SQL文を取得し、下流のシンクタイプに基づいて対応する形式に変換し、下流に送信します。このセクションではこれについては詳しく説明しません。

> **注記：**
>
> TiCDC がデータ変更を処理するロジックは、以降のバージョンで調整される可能性があります。

MySQLのbinlogは、上流で実行されたすべてのDML SQL文を直接記録します。MySQLとは異なり、TiCDCは上流TiKV内の各リージョンRaftログのリアルタイム情報をリッスンし、各トランザクションの前後のデータの差分に基づいて、複数のSQL文に対応するデータ変更情報を生成します。TiCDCは、出力された変更イベントが上流TiDBの変更と同等であることを保証するだけで、上流TiDBのデータ変更を引き起こしたSQL文を正確に復元できることは保証しません。

データ変更情報には、データ変更の種類と変更前後のデータ値が含まれます。トランザクション前後のデータの違いによって、以下の3種類のイベントが発生する可能性があります。

1.  `DELETE`イベント: 変更前のデータが含まれる`DELETE`種類のデータ変更メッセージに対応します。

2.  `INSERT`イベント: 変更後のデータが含まれる`PUT`種類のデータ変更メッセージに対応します。

3.  `UPDATE`イベント: 変更前と変更後の両方のデータが含まれる`PUT`種類のデータ変更メッセージに対応します。

TiCDCは、データ変更情報に基づいて、下流の様々なタイプに適した形式でデータを生成し、下流に送信します。例えば、Canal-JSONやAvroなどの形式でデータを生成し、Kafkaに書き込んだり、SQL文に変換して下流のMySQLやTiDBに送信したりします。

現在、TiCDCは対応するプロトコルに合わせてデータ変更情報を調整する際に、特定の`UPDATE`イベントについて、 `DELETE`イベントと`INSERT`イベントに分割することがあります。詳細については、 [MySQLシンクの`UPDATE`イベントを分割する](/ticdc/ticdc-split-update-behavior.md#split-update-events-for-mysql-sinks)と[MySQL以外のシンクの主キーまたは一意キーの`UPDATE`イベントを分割する](/ticdc/ticdc-split-update-behavior.md#split-primary-or-unique-key-update-events-for-non-mysql-sinks)参照してください。

下流がMySQLまたはTiDBの場合、TiCDCは下流に書き込まれるSQL文が上流で実行されたSQL文と完全に同一であることを保証できません。これは、TiCDCが上流で実行された元のDML文を直接取得するのではなく、データの変更情報に基づいてSQL文を生成するためです。ただし、TiCDCは最終結果の一貫性を保証します。

たとえば、次の SQL ステートメントはアップストリームで実行されます。

```sql
Create Table t1 (A int Primary Key, B int);

BEGIN;
Insert Into t1 values(1,2);
Insert Into t1 values(2,2);
Insert Into t1 values(3,3);
Commit;

Update t1 set b = 4 where b = 2;
```

TiCDC は、データ変更情報に基づいて次の 2 つの SQL ステートメントを生成し、ダウンストリームに書き込みます。

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

現在、次のシナリオはサポートされていません。

-   RawKV のみを使用する TiKV クラスター。
-   TiDBの[`CREATE SEQUENCE` DDL操作](/sql-statements/sql-statement-create-sequence.md)と[`SEQUENCE`関数](/sql-statements/sql-statement-create-sequence.md#sequence-function) 。上流のTiDBが`SEQUENCE`使用する場合、TiCDCは上流で実行された`SEQUENCE` DDL操作/関数を無視します。ただし、 `SEQUENCE`関数を使用するDML操作は正しく複製されます。
-   現在、TiCDCによって複製されているテーブルおよびデータベースに対する[BRデータ復旧](/br/backup-and-restore-overview.md)および[TiDB Lightning物理インポート](/tidb-lightning/tidb-lightning-physical-import-mode.md)インポートはサポートされていません。詳細については、 [TiCDC を使用したレプリケーションが、上流からTiDB LightningとBRを使用してデータを復元した後に停止したり、停止したりするのはなぜですか?](/ticdc/ticdc-faq.md#why-does-replication-using-ticdc-stall-or-even-stop-after-data-restore-using-tidb-lightning-physical-import-mode-and-br-from-upstream)参照してください。

TiCDCは、アップストリームにおける大規模トランザクションを含むシナリオを部分的にしかサポートしていません。詳細については、 [TiCDCFAQ](/ticdc/ticdc-faq.md#does-ticdc-support-replicating-large-transactions-is-there-any-risk)を参照してください。そこでは、TiCDCが大規模トランザクションの複製をサポートしているかどうか、および関連するリスクについて詳しく説明されています。
