---
title: Data Check for TiDB Upstream and Downstream Clusters
summary: Learn how to check data for TiDB upstream and downstream clusters.
---

# TiDB アップストリームおよびダウンストリーム クラスタのデータ チェック {#data-check-for-tidb-upstream-and-downstream-clusters}

TiCDC を使用して TiDB のアップストリームおよびダウンストリーム クラスターを構築する場合、レプリケーションを停止せずにアップストリームおよびダウンストリーム データの整合性を検証する必要がある場合があります。通常のレプリケーション モードでは、TiCDC はデータが最終的に一貫していることのみを保証しますが、レプリケーション プロセス中にデータが一貫していることを保証することはできません。したがって、動的に変化するデータの整合性を検証することは困難です。そのようなニーズを満たすために、TiCDC は Syncpoint 機能を提供します。

Syncpoint は、TiDB が提供するスナップショット機能を使用し、TiCDC がレプリケーション プロセス中にアップストリームとダウンストリームのスナップショット間で一貫性を持つ`ts-map`を維持できるようにします。このように、動的データの整合性を検証する問題は、静的なスナップショット データの整合性を検証する問題に変換され、ほぼリアルタイムの検証の効果が得られます。

同期点機能を有効にするには、レプリケーション タスクの作成時に TiCDC 構成項目の値を`enable-sync-point`から`true`に設定します。同期点を有効にした後、TiCDC は、データ複製プロセス中に TiCDC パラメータ`sync-point-interval`に従って定期的にアップストリームとダウンストリームのスナップショットを調整し、アップストリームとダウンストリームの TSO 対応をダウンストリーム`tidb_cdc.syncpoint_v1`テーブルに保存します。

次に、sync-diff-inspector で`snapshot`を構成するだけで、TiDB の上流と下流のクラスターのデータを検証できます。次の TiCDC 構成例では、作成されたレプリケーション タスクの同期点を有効にします。

```toml
# Enables SyncPoint.
enable-sync-point = true

# Aligns the upstream and downstream snapshots every 5 minutes
sync-point-interval = "5m"

# Cleans up the ts-map data in the downstream tidb_cdc.syncpoint_v1 table every hour
sync-point-retention = "1h"
```

## ステップ 1: <code>ts-map</code>を取得する {#step-1-obtain-code-ts-map-code}

下流の TiDB クラスターで次の SQL ステートメントを実行して、上流の TSO ( `primary_ts` ) と下流の TSO ( `secondary_ts` ) を取得できます。

```sql
select * from tidb_cdc.syncpoint_v1;
+------------------+----------------+--------------------+--------------------+---------------------+
| ticdc_cluster_id | changefeed     | primary_ts         | secondary_ts       | created_at          |
+------------------+----------------+--------------------+--------------------+---------------------+
| default          | test-2 | 435953225454059520 | 435953235516456963 | 2022-09-13 08:40:15 |
+------------------+----------------+--------------------+--------------------+---------------------+
```

前述の`syncpoint_v1`表のフィールドは、次のように説明されています。

-   `ticdc_cluster_id` : このレコードの TiCDC クラスターの ID。
-   `changefeed` : このレコードの変更フィードの ID。異なる TiCDC クラスターには同じ名前の変更フィードがある可能性があるため、変更フィードによって挿入された`ts-map`を TiCDC クラスター ID と変更フィード ID で確認する必要があります。
-   `primary_ts` : アップストリーム データベース スナップショットのタイムスタンプ。
-   `secondary_ts` : ダウンストリーム データベース スナップショットのタイムスタンプ。
-   `created_at` : このレコードが挿入された時刻。

## ステップ 2: スナップショットを構成する {#step-2-configure-snapshot}

[ステップ1](#step-1-obtain-ts-map)で取得した`ts-map`情報を利用して、上流データベースと下流データベースのスナップショット情報を設定します。

`Datasource config`セクションの設定例を次に示します。

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

-   TiCDC が変更フィードを作成する前に、TiCDC 構成項目`enable-sync-point`の値が`true`に設定されていることを確認してください。このようにしてのみ、同期点が有効になり、 `ts-map`がダウンストリームに保存されます。完全な構成については、 [TiCDC タスク構成ファイル](/ticdc/ticdc-changefeed-config.md)を参照してください。
-   TiKV のガベージ コレクション (GC) 時間を変更して、スナップショットに対応する履歴データがデータ チェック中に GC によって収集されないようにします。確認後、GC 時間を 1 時間に変更し、設定を元に戻すことをお勧めします。
-   上記の例は、 `Datasource config`のセクションのみを示しています。完全な構成については、 [sync-diff-inspector ユーザーガイド](/sync-diff-inspector/sync-diff-inspector-overview.md)を参照してください。
-   v6.4.0 以降、TiCDC Syncpoint 機能を使用できるのは、 `SYSTEM_VARIABLES_ADMIN`または`SUPER`特権を持つ changefeed のみです。
