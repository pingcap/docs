---
title: Upstream and Downstream Clusters Data Validation and Snapshot Read
summary: Learn how to check data for TiDB upstream and downstream clusters.
---

# 上流および下流クラスターのデータ検証とスナップショット読み取り {#upstream-and-downstream-clusters-data-validation-and-snapshot-read}

TiCDC を使用して TiDB のアップストリームおよびダウンストリームのクラスターを構築する場合、レプリケーションを停止せずに、アップストリームとダウンストリームで一貫したスナップショットの読み取りまたはデータの整合性検証を実行する必要がある場合があります。通常のレプリケーション モードでは、TiCDC はデータの最終的な整合性のみを保証しますが、レプリケーション プロセス中のデータの整合性は保証できません。したがって、動的に変化するデータを一貫して読み取ることは困難です。このようなニーズを満たすために、TiCDC は Syncpoint 機能を提供します。

Syncpoint は、TiDB が提供するスナップショット機能を使用し、TiCDC がレプリケーション プロセス中にアップストリーム スナップショットとダウンストリーム スナップショットの間で一貫性のある`ts-map`を維持できるようにします。このようにして、動的データの整合性検証の問題が、静的なスナップショット データの整合性検証の問題に変換され、ほぼリアルタイムの検証の効果が得られます。

## 同期点を有効にする {#enable-syncpoint}

同期ポイント機能を有効にすると、 [一貫したスナップショット読み取り](#consistent-snapshot-read)と[データの整合性の検証](#data-consistency-validation)を使用できるようになります。

同期ポイント機能を有効にするには、レプリケーション タスクの作成時に TiCDC 構成項目の値`enable-sync-point`から`true`を設定します。 Syncpoint を有効にすると、TiCDC は次の情報をダウンストリーム TiDB クラスターに書き込みます。

1.  レプリケーション中、TiCDC は定期的に ( `sync-point-interval`で構成) アップストリームとダウンストリームの間でスナップショットを調整し、アップストリームとダウンストリームの TSO の対応をダウンストリーム`tidb_cdc.syncpoint_v1`テーブルに保存します。
2.  レプリケーション中、TiCDC は定期的に ( `sync-point-interval`で構成) `SET GLOBAL tidb_external_ts = @@tidb_current_ts`を実行します。これは、バックアップ クラスターにレプリケートされた一貫性のあるスナップショット ポイントを設定します。

次の TiCDC 構成例では、レプリケーション タスクの作成時に同期ポイントを有効にします。

```toml
# Enables SyncPoint.
enable-sync-point = true

# Aligns the upstream and downstream snapshots every 5 minutes
sync-point-interval = "5m"

# Cleans up the ts-map data in the downstream tidb_cdc.syncpoint_v1 table every hour
sync-point-retention = "1h"
```

## 一貫したスナップショット読み取り {#consistent-snapshot-read}

> **注記：**
>
> 一貫したスナップショット読み取りを実行する前に、 [同期ポイント機能を有効にしました](#enable-syncpoint)があることを確認してください。

バックアップ クラスターからデータをクエリする必要がある場合は、アプリケーションに`SET GLOBAL|SESSION tidb_enable_external_ts_read = ON;`を設定して、バックアップ クラスター上でトランザクションの一貫性のあるデータを取得できます。

さらに、 `ts-map`をクエリして、スナップショット読み取りの前の時点を選択することもできます。

## データの整合性の検証 {#data-consistency-validation}

> **注記：**
>
> データの整合性検証を実行する前に、 [同期ポイント機能を有効にしました](#enable-syncpoint)あることを確認してください。

アップストリーム クラスターとダウンストリーム クラスターのデータを検証するには、sync-diff-inspector で`snapshot`を設定するだけです。

### ステップ 1: <code>ts-map</code>を取得する {#step-1-obtain-code-ts-map-code}

ダウンストリーム TiDB クラスターで次の SQL ステートメントを実行して、アップストリーム TSO ( `primary_ts` ) とダウンストリーム TSO ( `secondary_ts` ) を取得できます。

```sql
select * from tidb_cdc.syncpoint_v1;
+------------------+----------------+--------------------+--------------------+---------------------+
| ticdc_cluster_id | changefeed     | primary_ts         | secondary_ts       | created_at          |
+------------------+----------------+--------------------+--------------------+---------------------+
| default          | test-2 | 435953225454059520 | 435953235516456963 | 2022-09-13 08:40:15 |
+------------------+----------------+--------------------+--------------------+---------------------+
```

前述の`syncpoint_v1`の表のフィールドは次のように説明されています。

-   `ticdc_cluster_id` : このレコードの TiCDC クラスターの ID。
-   `changefeed` : このレコードの変更フィードの ID。異なる TiCDC クラスターに同じ名前の変更フィードがある可能性があるため、変更フィードによって挿入された`ts-map`を TiCDC クラスター ID と変更フィード ID で確認する必要があります。
-   `primary_ts` : アップストリーム データベース スナップショットのタイムスタンプ。
-   `secondary_ts` : ダウンストリーム データベース スナップショットのタイムスタンプ。
-   `created_at` : このレコードが挿入された時刻。

### ステップ 2: スナップショットを構成する {#step-2-configure-snapshot}

次に、 [ステップ1](#step-1-obtain-ts-map)で取得した`ts-map`情報を使用して、上流データベースと下流データベースのスナップショット情報を設定します。

`Datasource config`セクションの構成例を次に示します。

```toml
######################### Datasource config ########################
[data-sources.uptidb]
    host = "172.16.0.1"
    port = 4000
    user = "root"
    password = ""
    snapshot = "435953225454059520"

[data-sources.downtidb]
    host = "172.16.0.2"
    port = 4000
    user = "root"
    snapshot = "435953235516456963"
```

## ノート {#notes}

-   TiCDC が変更フィードを作成する前に、TiCDC 構成項目`enable-sync-point`の値が`true`に設定されていることを確認してください。この方法でのみ、同期ポイントが有効になり、 `ts-map`がダウンストリームに保存されます。完全な構成については、 [TiCDC タスク構成ファイル](/ticdc/ticdc-changefeed-config.md)を参照してください。
-   Syncpoint を使用してデータ検証を実行する場合、TiKV のガベージ コレクション (GC) 時間を変更して、スナップショットに対応する履歴データがデータ チェック中に GC によって収集されないようにする必要があります。 GC 時間を 1 時間に変更し、チェック後に設定を復元することをお勧めします。
-   上記の例は`Datasource config`のセクションのみを示しています。完全な構成については、 [sync-diff-inspector ユーザーガイド](/sync-diff-inspector/sync-diff-inspector-overview.md)を参照してください。
-   v6.4.0 以降、TiCDC Syncpoint 機能を使用できるのは、 `SYSTEM_VARIABLES_ADMIN`または`SUPER`権限を持つ変更フィードのみです。
