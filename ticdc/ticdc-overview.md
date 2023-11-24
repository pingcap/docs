---
title: TiCDC Overview
summary: Learn what TiCDC is, what features TiCDC provides, and how to install and deploy TiCDC.
---

# TiCDC の概要 {#ticdc-overview}

[TiCDC](https://github.com/pingcap/tiflow/tree/master/cdc)は、TiDB から増分データを複製するために使用されるツールです。具体的には、TiCDC は TiKV 変更ログを取得し、キャプチャしたデータを並べ替えて、行ベースの増分データをダウンストリーム データベースにエクスポートします。

## 使用シナリオ {#usage-scenarios}

TiCDC には、次のような複数の使用シナリオがあります。

-   複数の TiDB クラスターに高可用性および災害復旧ソリューションを提供します。 TiCDC は、災害発生時にプライマリ クラスタとセカンダリ クラスタ間の最終的なデータ整合性を保証します。
-   リアルタイムのデータ変更を同種システムに複製します。これにより、モニタリング、キャッシュ、グローバル インデックス作成、データ分析、異種データベース間のプライマリとセカンダリのレプリケーションなど、さまざまなシナリオにデータ ソースが提供されます。

## 主な特長 {#major-features}

### 主な機能 {#key-capabilities}

TiCDC には次の主要な機能があります。

-   第 2 レベルの RPO と分レベルの RTO を使用して、TiDB クラスター間で増分データをレプリケートします。
-   TiDB クラスター間の双方向レプリケーションにより、TiCDC を使用したマルチアクティブ TiDB ソリューションの作成が可能になります。
-   TiDB クラスターから MySQL データベースまたは他の MySQL 互換データベースに低レイテンシーで増分データをレプリケートします。
-   TiDB クラスターから Kafka クラスターへの増分データのレプリケーション。推奨されるデータ形式には[カナル-JSON](/ticdc/ticdc-canal-json.md)と[アブロ](/ticdc/ticdc-avro-protocol.md)があります。
-   TiDB クラスターから Amazon S3、GCS、Azure Blob Storage、NFS などのstorageサービスへの増分データのレプリケーション。
-   データベース、テーブル、DML、DDL をフィルタリングする機能を備えたテーブルのレプリケート。
-   単一障害点のない高可用性。TiCDC ノードの動的追加と削除をサポートします。
-   [オープンAPI](/ticdc/ticdc-open-api.md)によるクラスタ管理。これには、タスク ステータスのクエリ、タスク構成の動的変更、タスクの作成または削除が含まれます。

### レプリケーションの順序 {#replication-order}

-   すべての DDL または DML ステートメントについて、TiCDC はそれらを**少なくとも 1 回**出力します。
-   TiKV または TiCDC クラスターで障害が発生すると、TiCDC は同じ DDL/DML ステートメントを繰り返し送信する可能性があります。重複した DDL/DML ステートメントの場合:

    -   MySQL シンクは DDL ステートメントを繰り返し実行できます。 `TRUNCATE TABLE`など、ダウンストリームで繰り返し実行できる DDL ステートメントの場合、ステートメントは正常に実行されます。 `CREATE TABLE`など、繰り返し実行できないものについては、実行は失敗し、TiCDC はエラーを無視してレプリケーション プロセスを続行します。
    -   Kafka シンクは、データ分散のためのさまざまな戦略を提供します。
        -   テーブル、主キー、またはタイムスタンプに基づいて、データをさまざまな Kafka パーティションに分散できます。これにより、行の更新されたデータが同じパーティションに順番に送信されることが保証されます。
        -   これらすべての分散戦略は、すべてのトピックとパーティションに`Resolved TS`メッセージを定期的に送信します。これは、 `Resolved TS`つより前のすべてのメッセージがすでにトピックとパーティションに送信されていることを示します。 Kafka コンシューマーは`Resolved TS`使用して、受信したメッセージを並べ替えることができます。
        -   Kafka シンクは重複したメッセージを送信することがありますが、これらの重複したメッセージは`Resolved Ts`の制約には影響しません。たとえば、チェンジフィードが一時停止されてから再開される場合、Kafka シンクは`msg1` 、 `msg2` 、 `msg3` 、 `msg2` 、および`msg3`順番に送信する可能性があります。 Kafka コンシューマーからの重複メッセージをフィルターで除外できます。

### レプリケーションの一貫性 {#replication-consistency}

-   MySQLシンク

    -   TiCDC は、REDO ログを有効にして、データ レプリケーションの最終的な整合性を確保します。

    -   TiCDC は、単一行の更新の順序がアップストリームと一貫していることを保証します。

    -   TiCDC は、ダウンストリーム トランザクションがアップストリーム トランザクションと同じ順序で実行されることを保証しません。

    > **注記：**
    >
    > v6.2 以降、シンク URI パラメーター[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)を使用して、単一テーブルのトランザクションを分割するかどうかを制御できます。単一テーブルのトランザクションを分割すると、大規模なトランザクションをレプリケートする際のレイテンシーとメモリ消費量を大幅に削減できます。

## TiCDCアーキテクチャ {#ticdc-architecture}

TiCDC は TiDB 用の増分データ レプリケーション ツールであり、PD の etcd を通じて可用性が高くなります。レプリケーション プロセスは次の手順で構成されます。

1.  複数の TiCDC プロセスが TiKV ノードからデータ変更をプルします。
2.  TiCDC はデータ変更を並べ替えてマージします。
3.  TiCDC は、複数のレプリケーション タスク (変更フィード) を通じて、データ変更を複数のダウンストリーム システムにレプリケートします。

TiCDC のアーキテクチャを次の図に示します。

![TiCDC architecture](/media/ticdc/cdc-architecture.png)

アーキテクチャ図内のコンポーネントは次のように説明されています。

-   TiKV サーバー: TiDB クラスター内の TiKV ノード。データ変更が発生すると、TiKV ノードは変更を変更ログ (KV 変更ログ) として TiCDC ノードに送信します。 TiCDC ノードは、変更ログが連続していないことを検出すると、TiKV ノードに変更ログを提供するように積極的に要求します。
-   TiCDC: TiCDC プロセスが実行される TiCDC ノード。各ノードは TiCDC プロセスを実行します。各プロセスは、TiKV ノード内の 1 つ以上のテーブルからデータ変更を取得し、その変更をシンクコンポーネントを通じて下流システムに複製します。
-   PD: TiDB クラスター内のスケジューリング モジュール。このモジュールはクラスター データのスケジューリングを担当し、通常は 3 つの PD ノードで構成されます。 PD は、etcd クラスターを通じて高可用性を提供します。 etcd クラスターでは、TiCDC はノードのステータス情報や変更フィード構成などのメタデータを保存します。

アーキテクチャ図に示されているように、TiCDC は、TiDB、MySQL、Kafka、およびstorageサービスへのデータのレプリケーションをサポートしています。

## ベストプラクティス {#best-practices}

-   TiCDC を使用して 2 つの TiDB クラスター間でデータをレプリケートする場合、2 つのクラスター間のネットワークレイテンシーが100 ミリ秒を超える場合:

    -   v6.5.2 より前の TiCDC バージョンの場合、ダウンストリーム TiDB クラスターが配置されているリージョン (IDC) に TiCDC をデプロイすることをお勧めします。
    -   TiCDC v6.5.2 から導入された一連の改善により、上流の TiDB クラスターが配置されているリージョン (IDC) に TiCDC をデプロイすることをお勧めします。

-   TiCDC は、少なくとも 1 つの有効なインデックスを持つテーブルのみを複製します。有効なインデックスは次のように定義されます。

    -   主キー ( `PRIMARY KEY` ) は有効なインデックスです。
    -   一意のインデックス ( `UNIQUE INDEX` ) は、インデックスのすべての列が null 非許容として明示的に定義され ( `NOT NULL` )、インデックスに仮想生成列 ( `VIRTUAL GENERATED COLUMNS` ) がない場合に有効です。

-   災害復旧シナリオで TiCDC を使用するには、 [やり直しログ](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)を構成する必要があります。

> **注記：**
>
> v4.0.8 以降、TiCDC はタスク構成を変更することで、有効なインデックスのないテーブルの複製をサポートします。ただし、これによりデータの一貫性の保証がある程度損なわれます。詳細については、 [有効なインデックスのないテーブルをレプリケートする](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index)を参照してください。

## サポートされていないシナリオ {#unsupported-scenarios}

現在、次のシナリオはサポートされていません。

-   RawKV のみを使用する TiKV クラスター。
-   TiDB の[`CREATE SEQUENCE` DDL 操作](/sql-statements/sql-statement-create-sequence.md)と[`SEQUENCE`機能](/sql-statements/sql-statement-create-sequence.md#sequence-function) 。アップストリームの TiDB が`SEQUENCE`使用すると、TiCDC はアップストリームで実行された`SEQUENCE` DDL 操作/関数を無視します。ただし、 `SEQUENCE`関数を使用する DML 操作は正しく複製できます。

TiCDC は、アップストリームでの大規模なトランザクションを伴うシナリオを部分的にのみサポートします。詳細については、 [TiCDCFAQ](/ticdc/ticdc-faq.md#does-ticdc-support-replicating-large-transactions-is-there-any-risk)を参照してください。ここでは、TiCDC が大規模なトランザクションのレプリケーションとそれに関連するリスクをサポートしているかどうかの詳細を確認できます。
