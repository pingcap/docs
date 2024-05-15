---
title: TiCDC Overview
summary: Learn what TiCDC is, what features TiCDC provides, and how to install and deploy TiCDC.
---

# TiCDC の概要 {#ticdc-overview}

[ティCDC](https://github.com/pingcap/tiflow/tree/release-7.5/cdc)は、TiDB から増分データを複製するために使用されるツールです。具体的には、TiCDC は TiKV 変更ログを取得し、キャプチャしたデータをソートし、行ベースの増分データを下流のデータベースにエクスポートします。

## 使用シナリオ {#usage-scenarios}

TiCDC には、次のような複数の使用シナリオがあります。

-   複数の TiDB クラスターに高可用性と災害復旧ソリューションを提供します。TiCDC は、災害発生時にプライマリ クラスターとセカンダリ クラスター間の最終的なデータ整合性を保証します。
-   リアルタイムのデータ変更を同種システムに複製します。これにより、監視、キャッシュ、グローバル インデックス作成、データ分析、異種データベース間のプライマリ/セカンダリ レプリケーションなど、さまざまなシナリオのデータ ソースが提供されます。

## 主な特徴 {#major-features}

### 主な機能 {#key-capabilities}

TiCDC には次の主要な機能があります。

-   2 番目レベルの RPO と 1 分レベルの RTO を使用して、TiDB クラスター間で増分データを複製します。
-   TiDB クラスター間の双方向レプリケーションにより、TiCDC を使用したマルチアクティブ TiDB ソリューションの作成が可能になります。
-   TiDB クラスターから MySQL データベースまたはその他の MySQL 互換データベースに低レイテンシーで増分データを複製します。
-   TiDB クラスターから Kafka クラスターに増分データを複製します。推奨されるデータ形式には[運河-JSON](/ticdc/ticdc-canal-json.md)と[アブロ](/ticdc/ticdc-avro-protocol.md)が含まれます。
-   TiDB クラスターから Amazon S3、GCS、Azure Blob Storage、NFS などのstorageサービスに増分データを複製します。
-   データベース、テーブル、DML、および DDL をフィルタリングする機能を使用してテーブルを複製します。
-   単一障害点のない高可用性、TiCDC ノードの動的な追加と削除をサポートします。
-   [オープンAPI](/ticdc/ticdc-open-api-v2.md)を介したクラスタ管理（タスク ステータスの照会、タスク構成の動的な変更、タスクの作成または削除など）。

### 複製順序 {#replication-order}

-   すべての DDL または DML ステートメントについて、TiCDC はそれらを**少なくとも 1 回**出力します。
-   TiKV または TiCDC クラスターで障害が発生すると、TiCDC は同じ DDL/DML ステートメントを繰り返し送信することがあります。重複した DDL/DML ステートメントの場合:

    -   MySQL シンクは、DDL ステートメントを繰り返し実行できます。 `TRUNCATE TABLE`のように下流で繰り返し実行できる DDL ステートメントの場合、ステートメントは正常に実行されます。 `CREATE TABLE`のように繰り返し実行できない DDL ステートメントの場合、実行は失敗し、TiCDC はエラーを無視してレプリケーション プロセスを続行します。
    -   Kafka シンクは、データ分散のためのさまざまな戦略を提供します。
        -   テーブル、主キー、またはタイムスタンプに基づいて、データを異なる Kafka パーティションに分散できます。これにより、行の更新されたデータが順番に同じパーティションに送信されるようになります。
        -   これらのすべての分散戦略は、すべてのトピックとパーティションに`Resolved TS`メッセージを定期的に送信します。これは、 `Resolved TS`より前のすべてのメッセージがトピックとパーティションにすでに送信されていることを示します。Kafka コンシューマーは、 `Resolved TS`を使用して受信したメッセージを並べ替えることができます。
        -   Kafka シンクは重複したメッセージを送信することがありますが、これらの重複したメッセージは`Resolved Ts`の制約に影響しません。たとえば、変更フィードが一時停止されて再開された場合、Kafka シンクは`msg1` 、 `msg2` 、 `msg3` 、 `msg2` 、および`msg3`順に送信する可能性があります。Kafka コンシューマーからの重複メッセージをフィルター処理できます。

### レプリケーションの一貫性 {#replication-consistency}

-   MySQLシンク

    -   TiCDC は、REDO ログを有効にして、データ レプリケーションの最終的な一貫性を保証します。

    -   TiCDC は、単一行の更新の順序がアップストリームと一貫していることを保証します。

    -   TiCDC では、ダウンストリーム トランザクションがアップストリーム トランザクションと同じ順序で実行されることは保証されません。

    > **注記：**
    >
    > v6.2 以降では、シンク URI パラメータ[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)を使用して、単一テーブル トランザクションを分割するかどうかを制御できます。単一テーブル トランザクションを分割すると、大規模なトランザクションを複製する際のレイテンシーとメモリ消費を大幅に削減できます。

## TiCDCアーキテクチャ {#ticdc-architecture}

TiCDC は TiDB の増分データ レプリケーション ツールであり、PD の etcd を通じて高可用性を実現します。レプリケーション プロセスは次の手順で構成されます。

1.  複数の TiCDC プロセスが TiKV ノードからデータの変更を取得します。
2.  TiCDC はデータの変更をソートしてマージします。
3.  TiCDC は、複数のレプリケーション タスク (変更フィード) を通じて、データの変更を複数の下流システムに複製します。

TiCDC のアーキテクチャは次の図に示されています。

![TiCDC architecture](/media/ticdc/cdc-architecture.png)

アーキテクチャ図のコンポーネントは次のように説明されます。

-   TiKV サーバー: TiDB クラスター内の TiKV ノード。データの変更が発生すると、TiKV ノードは変更内容を変更ログ (KV 変更ログ) として TiCDC ノードに送信します。TiCDC ノードは変更ログが連続していないことを検出すると、TiKV ノードに変更ログを提供するよう積極的に要求します。
-   TiCDC: TiCDC プロセスが実行される TiCDC ノード。各ノードは TiCDC プロセスを実行します。各プロセスは、TiKV ノード内の 1 つ以上のテーブルからデータの変更を取得し、シンクコンポーネントを通じてダウンストリーム システムにその変更を複製します。
-   PD: TiDB クラスターのスケジューリング モジュール。このモジュールはクラスター データのスケジューリングを担当し、通常は 3 つの PD ノードで構成されます。PD は etcd クラスターを通じて高可用性を提供します。etcd クラスターでは、TiCDC はノードのステータス情報や変更フィード構成などのメタデータを保存します。

アーキテクチャ図に示されているように、TiCDC は TiDB、MySQL、Kafka、およびstorageサービスへのデータの複製をサポートしています。

## ベストプラクティス {#best-practices}

-   TiCDC を使用して 2 つの TiDB クラスター間でデータをレプリケートする場合、2 つのクラスター間のネットワークレイテンシーが 100 ミリ秒を超えると、次のようになります。

    -   v6.5.2 より前のバージョンの TiCDC の場合、ダウンストリーム TiDB クラスターが配置されているリージョン (IDC) に TiCDC をデプロイすることをお勧めします。
    -   TiCDC v6.5.2 から導入された一連の改善により、アップストリーム TiDB クラスターが配置されているリージョン (IDC) に TiCDC をデプロイすることが推奨されます。

-   TiCDC は、少なくとも 1 つの有効なインデックスを持つテーブルのみを複製します。有効なインデックスは次のように定義されます。

    -   主キー（ `PRIMARY KEY` ）は有効なインデックスです。
    -   ユニークインデックス（ `UNIQUE INDEX` ）は、インデックスのすべての列が明示的に非NULL値として定義され（ `NOT NULL` ）、インデックスに仮想生成列（ `VIRTUAL GENERATED COLUMNS` ）がない場合に有効です。

-   TiCDC を災害復旧に使用する場合、最終的な一貫性を確保するには、 [再実行ログ](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)設定し、上流で災害が発生したときに、REDO ログが書き込まれるstorageシステムが正常に読み取れるようにする必要があります。

## サポートされていないシナリオ {#unsupported-scenarios}

現在、次のシナリオはサポートされていません。

-   RawKV のみを使用する TiKV クラスター。
-   TiDB の[`CREATE SEQUENCE` DDL操作](/sql-statements/sql-statement-create-sequence.md)と[`SEQUENCE`機能](/sql-statements/sql-statement-create-sequence.md#sequence-function)上流の TiDB が`SEQUENCE`を使用する場合、TiCDC は上流で実行された`SEQUENCE` DDL 操作/関数を無視します。ただし、 `SEQUENCE`関数を使用する DML 操作は正しく複製できます。
-   現在、TiCDC によって複製されているテーブルおよびデータベースに対して[BRデータ復旧](/br/backup-and-restore-overview.md)および[TiDB Lightning物理インポート](/tidb-lightning/tidb-lightning-physical-import-mode.md)インポートを実行することはサポートされていません。詳細については、 [TiCDC を使用したレプリケーションが、上流からTiDB LightningとBRを使用してデータを復元した後に停止したり、停止したりする理由](/ticdc/ticdc-faq.md#why-does-replication-using-ticdc-stall-or-even-stop-after-data-restore-using-tidb-lightning-physical-import-mode-and-br-from-upstream)を参照してください。

TiCDC は、アップストリームでの大規模なトランザクションを伴うシナリオを部分的にのみサポートしています。詳細については、 [TiCDCFAQ](/ticdc/ticdc-faq.md#does-ticdc-support-replicating-large-transactions-is-there-any-risk)を参照してください。そこでは、TiCDC が大規模なトランザクションの複製をサポートしているかどうか、および関連するリスクについての詳細が説明されています。
