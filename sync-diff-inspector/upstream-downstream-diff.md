---
title: Data Check for TiDB Upstream and Downstream Clusters
summary: Learn how to check data for TiDB upstream and downstream clusters.
---

# TiDB アップストリームおよびダウンストリーム クラスタのデータ チェック {#data-check-for-tidb-upstream-and-downstream-clusters}

TiDB Binlogを使用して、TiDB のアップストリームおよびダウンストリーム クラスターを構築できます。 Drainerがデータを TiDB にレプリケートすると、チェックポイントが保存され、上流と下流の間の TSO マッピング関係も`ts-map`として保存されます。アップストリームとダウンストリーム間のデータを確認するには、sync-diff-inspector で`snapshot`を設定します。

## ステップ 1: <code>ts-map</code>を取得する {#step-1-obtain-code-ts-map-code}

`ts-map`を取得するには、下流の TiDB クラスターで次の SQL ステートメントを実行します。

```sql
mysql> select * from tidb_binlog.checkpoint;
+---------------------+---------------------------------------------------------------------------------------------------------+
| clusterID           | checkPoint                                                                                              |
+---------------------+---------------------------------------------------------------------------------------------------------+
| 6711243465327639221 | {"commitTS":409622383615541249,"ts-map":{"primary-ts":409621863377928194,"secondary-ts":409621863377928345}} |
+---------------------+---------------------------------------------------------------------------------------------------------+
```

## ステップ 2: スナップショットを構成する {#step-2-configure-snapshot}

[ステップ1](#step-1-obtain-ts-map)で取得した`ts-map`の情報を利用して、上流データベースと下流データベースのスナップショット情報を設定します。

`Datasource config`セクションの設定例を次に示します。

```toml
######################### Datasource config ########################
[data-sources.uptidb]
    host = "172.16.0.1"
    port = 4000
    user = "root"
    password = ""
    snapshot = "409621863377928194"

[data-sources.downtidb]
    host = "172.16.0.2"
    port = 4000
    user = "root"
    snapshot = "409621863377928345"
```

> **ノート：**
>
> -   Drainerの`db-type`を`tidb`に設定して、 `ts-map`がチェックポイントに保存されるようにします。
> -   TiKV のガベージ コレクション (GC) 時間を変更して、スナップショットに対応する履歴データがデータ チェック中に GC によって収集されないようにします。確認後、GC 時間を 1 時間に変更し、設定を元に戻すことをお勧めします。
> -   TiDB Binlogの一部のバージョンでは、 `master-ts`と`slave-ts`は`ts-map`に格納されます。 `master-ts`は`primary-ts`に相当し、 `slave-ts`は`secondary-ts`に相当します。
> -   上記の例は、 `Datasource config`のセクションのみを示しています。完全な構成については、 [sync-diff-inspector ユーザーガイド](/sync-diff-inspector/sync-diff-inspector-overview.md)を参照してください。
