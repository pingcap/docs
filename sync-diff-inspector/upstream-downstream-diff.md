---
title: Data Check for TiDB Upstream and Downstream Clusters
summary: Learn how to check data for TiDB upstream and downstream clusters.
---

# TiDBアップストリームおよびダウンストリームクラスターのデータチェック {#data-check-for-tidb-upstream-and-downstream-clusters}

TiDB Binlogを使用して、TiDBのアップストリームおよびダウンストリームクラスターを構築できます。 DrainerがデータをTiDBに複製すると、チェックポイントが保存され、アップストリームとダウンストリーム間のTSOマッピング関係も`ts-map`として保存されます。アップストリームとダウンストリーム間のデータをチェックするには、sync-diff-inspectorで`snapshot`を設定します。

## ステップ1： <code>ts-map</code>を取得する {#step-1-obtain-code-ts-map-code}

`ts-map`を取得するには、ダウンストリームTiDBクラスタで次のSQLステートメントを実行します。

```sql
mysql> select * from tidb_binlog.checkpoint;
+---------------------+---------------------------------------------------------------------------------------------------------+
| clusterID           | checkPoint                                                                                              |
+---------------------+---------------------------------------------------------------------------------------------------------+
| 6711243465327639221 | {"commitTS":409622383615541249,"ts-map":{"primary-ts":409621863377928194,"secondary-ts":409621863377928345}} |
+---------------------+---------------------------------------------------------------------------------------------------------+
```

## ステップ2：スナップショットを構成する {#step-2-configure-snapshot}

次に、 [ステップ1](#step-1-obtain-ts-map)で取得した`ts-map`の情報を使用して、アップストリームおよびダウンストリームデータベースのスナップショット情報を構成します。

`Datasource config`セクションの構成例を次に示します。

```toml
######################### Datasource config ########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    snapshot = "409621863377928345"
[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    snapshot = "409621863377928345"
```

> **ノート：**
>
> -   Drainerの`db-type`を`tidb`に設定して、 `ts-map`がチェックポイントに保存されるようにします。
> -   TiKVのガベージコレクション（GC）時間を変更して、スナップショットに対応する履歴データがデータチェック中にGCによって収集されないようにします。 GC時間を1時間に変更し、チェック後に設定を復元することをお勧めします。
> -   TiDB Binlogの一部のバージョンでは、 `master-ts`と`slave-ts`が`ts-map`に格納されます。 `master-ts`は`primary-ts`に相当し、 `slave-ts`は`secondary-ts`に相当します。
> -   上記の例は、 `Datasource config`のセクションのみを示しています。完全な構成については、 [sync-diff-inspectorユーザーガイド](/sync-diff-inspector/sync-diff-inspector-overview.md)を参照してください。
