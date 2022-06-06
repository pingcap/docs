---
title: TiDB Binlog Relay Log
summary: Learn how to use relay log to maintain data consistency in extreme cases.
---

# TiDBBinlogリレーログ {#tidb-binlog-relay-log}

binlogを複製する場合、Drainerはトランザクションをアップストリームから分割し、分割されたトランザクションを同時にダウンストリームに複製します。

アップストリームクラスターが使用できず、Drainerが異常終了する極端な場合、ダウンストリームクラスター（MySQLまたはTiDB）は、データに一貫性がない中間状態になる可能性があります。このような場合、Drainerはリレーログを使用して、ダウンストリームクラスターが一貫した状態にあることを確認できます。

## ドレイナー複製中の一貫した状態 {#consistent-state-during-drainer-replication}

ダウンストリームクラスターが一貫した状態に達するということは、ダウンストリームクラスターのデータが`tidb_snapshot = ts`を設定するアップストリームのスナップショットと同じであることを意味します。

チェックポイントの整合性とは、Drainerチェックポイントがレプリケーションの整合性のある状態を`consistent`に保存することを意味します。 Drainerを実行すると、 `consistent`は`false`になります。ドレイナーが正常に終了した後、 `consistent`は`true`に設定されます。

次のように、ダウンストリームチェックポイントテーブルをクエリできます。

{{< copyable "" >}}

```sql
select * from tidb_binlog.checkpoint;
```

```
+---------------------+----------------------------------------------------------------+
| clusterID           | checkPoint                                                     |
+---------------------+----------------------------------------------------------------+
| 6791641053252586769 | {"consistent":false,"commitTS":414529105591271429,"ts-map":{}} |
+---------------------+----------------------------------------------------------------+
```

## 実装の原則 {#implementation-principles}

Drainerはリレーログを有効にした後、最初にbinlogイベントをディスクに書き込み、次にイベントをダウンストリームクラスターに複製します。

アップストリームクラスターが使用できない場合、Drainerはリレーログを読み取ることにより、ダウンストリームクラスターを一貫した状態に復元できます。

> **ノート：**
>
> リレーログデータが同時に失われる場合、この方法は機能しませんが、その発生率は非常に低くなります。さらに、ネットワークファイルシステムを使用して、リレーログのデータの安全性を確保できます。

### Drainerがリレーログからbinlogを消費するシナリオをトリガーする {#trigger-scenarios-where-drainer-consumes-binlogs-from-the-relay-log}

Drainerの起動時に、アップストリームクラスターの配置ドライバー（PD）への接続に失敗し、チェックポイントで`consistent = false`を検出すると、Drainerはリレーログを読み取ろうとし、ダウンストリームクラスターを一貫した状態に復元します。その後、Drainerプロセスはチェックポイント`consistent`を`true`に設定し、終了します。

### リレーログのGCメカニズム {#gc-mechanism-of-relay-log}

データがダウンストリームに複製される前に、Drainerはデータをリレーログファイルに書き込みます。リレーログファイルのサイズが10MB（デフォルト）に達し、現在のトランザクションのbinlogデータが完全に書き込まれると、Drainerは次のリレーログファイルへのデータの書き込みを開始します。 Drainerは、データをダウンストリームに正常に複製した後、データが複製されたリレーログファイルを自動的にクリーンアップします。現在データが書き込まれているリレーログはクリーンアップされません。

## Configuration / コンフィグレーション {#configuration}

リレーログを有効にするには、Drainerに次の構成を追加します。

{{< copyable "" >}}

```
[syncer.relay]
# It saves the directory of the relay log. The relay log is not enabled if the value is empty.
# The configuration only comes to effect if the downstream is TiDB or MySQL.
log-dir = "/dir/to/save/log"
# The size limit of a single relay log file (unit: byte).
# When the size of a relay log file reaches this limit, data is written to the next relay log file.
max-file-size = 10485760
```
