---
title: Upstream and Downstream Clusters Data Validation and Snapshot Read
summary: TiDB アップストリーム クラスターとダウンストリーム クラスターのデータを確認する方法を学習します。
---

# 上流および下流のクラスタデータ検証とスナップショット読み取り {#upstream-and-downstream-clusters-data-validation-and-snapshot-read}

TiCDC を使用して TiDB の上流および下流クラスターを構築する場合、レプリケーションを停止せずに上流および下流で一貫性のあるスナップショット読み取りまたはデータ一貫性検証を実行する必要がある場合があります。通常のレプリケーション モードでは、TiCDC はデータの最終的な一貫性を保証するだけで、レプリケーション プロセス中のデータの一貫性は保証できません。そのため、動的に変化するデータの一貫性のある読み取りを実行することは困難です。このようなニーズを満たすために、TiCDC は Syncpoint 機能を提供します。

Syncpoint は、TiDB が提供するスナップショット機能を使用し、レプリケーション プロセス中に TiCDC が上流と下流のスナップショット間で一貫性のある`ts-map`維持できるようにします。これにより、動的データの一貫性の検証の問題が、静的スナップショット データの一貫性の検証の問題に変換され、ほぼリアルタイムの検証の効果が得られます。

## 同期ポイントを有効にする {#enable-syncpoint}

Syncpoint 機能を有効にすると、 [一貫性のあるスナップショットの読み取り](#consistent-snapshot-read)と[データ一貫性検証](#data-consistency-validation)が使用できるようになります。

Syncpoint 機能を有効にするには、レプリケーション タスクを作成するときに、TiCDC 構成項目の値を`enable-sync-point`から`true`に設定します。Syncpoint を有効にすると、TiCDC は次の情報をダウンストリーム TiDB クラスターに書き込みます。

1.  レプリケーション中、TiCDC は定期的に ( `sync-point-interval`で設定) アップストリームとダウンストリームの間でスナップショットを調整し、アップストリームとダウンストリームの TSO 対応をダウンストリーム`tidb_cdc.syncpoint_v1`テーブルに保存します。
2.  レプリケーション中、TiCDC は定期的に ( `sync-point-interval`で設定) `SET GLOBAL tidb_external_ts = @@tidb_current_ts`を実行し、バックアップ クラスターにレプリケートされた一貫性のあるスナップショット ポイントを設定します。

次の TiCDC 構成例では、レプリケーション タスクの作成時に Syncpoint を有効にします。

```toml
# Enables SyncPoint.
enable-sync-point = true

# Aligns the upstream and downstream snapshots every 5 minutes
sync-point-interval = "5m"

# Cleans up the ts-map data in the downstream tidb_cdc.syncpoint_v1 table every hour
sync-point-retention = "1h"
```

## 一貫性のあるスナップショットの読み取り {#consistent-snapshot-read}

> **注記：**
>
> 一貫性のあるスナップショット読み取りを実行する前に、 [同期ポイント機能を有効にしました](#enable-syncpoint)あることを確認してください。複数のレプリケーション タスクが同じダウンストリーム TiDB クラスターを使用し、同期ポイントが有効になっている場合、これらの各タスクは、それぞれのレプリケーションの進行状況に基づいて`tidb_external_ts`と`ts-map`更新します。この場合、 `ts-map`テーブルからレコードを読み取ることによって、レプリケーション タスク レベルで一貫性のあるスナップショット読み取りを設定する必要があります。一方、複数のレプリケーション タスクが互いに干渉し、一貫性のない結果になる可能性があるため、ダウンストリーム アプリケーションが`tidb_enable_external_ts_read`を使用してデータを読み取ることは避ける必要があります。

バックアップ クラスターからデータを照会する必要がある場合は、アプリケーションがバックアップ クラスター上でトランザクション的に一貫性のあるデータを取得するように`SET GLOBAL|SESSION tidb_enable_external_ts_read = ON;`設定できます。

さらに、 `ts-map`クエリすることで、スナップショット読み取りの以前の時点を選択することもできます。

## データ一貫性検証 {#data-consistency-validation}

> **注記：**
>
> データ一貫性検証を実行する前に、 [同期ポイント機能を有効にしました](#enable-syncpoint)あることを確認してください。

アップストリーム クラスターとダウンストリーム クラスターのデータを検証するには、sync-diff-inspector で`snapshot`設定するだけです。

### ステップ1: <code>ts-map</code>を取得する {#step-1-obtain-code-ts-map-code}

ダウンストリームTiDBクラスタで次のSQL文を実行すると、アップストリームTSO（ `primary_ts` ）とダウンストリームTSO（ `secondary_ts` ）を取得できます。

```sql
select * from tidb_cdc.syncpoint_v1;
+------------------+----------------+--------------------+--------------------+---------------------+
| ticdc_cluster_id | changefeed     | primary_ts         | secondary_ts       | created_at          |
+------------------+----------------+--------------------+--------------------+---------------------+
| default          | test-2 | 435953225454059520 | 435953235516456963 | 2022-09-13 08:40:15 |
+------------------+----------------+--------------------+--------------------+---------------------+
```

前述の`syncpoint_v1`表のフィールドの説明は次のとおりです。

-   `ticdc_cluster_id` : このレコード内の TiCDC クラスターの ID。
-   `changefeed` : このレコード内の変更フィードの ID。異なる TiCDC クラスターに同じ名前の変更フィードが存在する可能性があるため、変更フィードによって挿入された`ts-map`を TiCDC クラスター ID と変更フィード ID で確認する必要があります。
-   `primary_ts` : アップストリーム データベース スナップショットのタイムスタンプ。
-   `secondary_ts` : ダウンストリーム データベース スナップショットのタイムスタンプ。
-   `created_at` : このレコードが挿入された時刻。

### ステップ2: スナップショットを構成する {#step-2-configure-snapshot}

次に、 [ステップ1](#step-1-obtain-ts-map)で取得した`ts-map`情報を使用して、上流データベースと下流データベースのスナップショット情報を設定します。

セクション`Datasource config`の構成例を次に示します。

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

-   TiCDC が changefeed を作成する前に、TiCDC 構成項目`enable-sync-point`の値が`true`に設定されていることを確認してください。この方法でのみ、同期ポイントが有効になり、 `ts-map`ダウンストリームに保存されます。完全な構成については、 [TiCDC タスク構成ファイル](/ticdc/ticdc-changefeed-config.md)を参照してください。
-   Syncpoint を使用してデータ検証を実行する場合、データ チェック中にスナップショットに対応する履歴データが GC によって収集されないように、TiKV のガベージ コレクション (GC) 時間を変更する必要があります。GC 時間を 1 時間に変更し、チェック後に設定を復元することをお勧めします。
-   上記の例では`Datasource config`の部分のみを示しています。完全な設定については[sync-diff-inspector ユーザーガイド](/sync-diff-inspector/sync-diff-inspector-overview.md)を参照してください。
-   v6.4.0 以降では、権限`SYSTEM_VARIABLES_ADMIN`または`SUPER`を持つ changefeed のみが TiCDC Syncpoint 機能を使用できます。
