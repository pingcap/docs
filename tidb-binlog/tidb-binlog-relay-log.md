---
title: TiDB Binlog Relay Log
summary: Learn how to use relay log to maintain data consistency in extreme cases.
---

# TiDB Binlogリレーログ {#tidb-binlog-relay-log}

バイナリログを複製するとき、 Drainer は上流からトランザクションを分割し、分割されたトランザクションを同時に下流に複製します。

アップストリーム クラスターが利用できず、 Drainer が異常終了するという極端なケースでは、ダウンストリーム クラスター (MySQL または TiDB) がデータの一貫性のない中間状態にある可能性があります。このような場合、 Drainer はリレー ログを使用して、ダウンストリーム クラスターが一貫した状態であることを確認できます。

## Drainerレプリケーション中の一貫した状態 {#consistent-state-during-drainer-replication}

ダウンストリーム クラスタが一貫した状態に達するということは、ダウンストリーム クラスタのデータが`tidb_snapshot = ts`を設定するアップストリームのスナップショットと同じであることを意味します。

チェックポイントの一貫性とは、 Drainerチェックポイントがレプリケーションの一貫した状態を`consistent`に保存することを意味します。 Drainer が実行されると、 `consistent`は`false`になります。 Drainer が正常に終了した後、 `consistent`が`true`に設定されます。

次のように、ダウンストリーム チェックポイント テーブルをクエリできます。

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

## 実施原則 {#implementation-principles}

Drainer がリレー ログを有効にすると、最初にbinlogイベントがディスクに書き込まれ、次にそのイベントがダウンストリーム クラスターにレプリケートされます。

アップストリーム クラスタが利用できない場合、 Drainer はリレー ログを読み取ることで、ダウンストリーム クラスタを一貫した状態に復元できます。

> **ノート：**
>
> リレー ログ データが同時に失われる場合、この方法は機能しませんが、その発生率は非常に低いです。さらに、ネットワーク ファイル システムを使用して、リレー ログのデータの安全性を確保できます。

### Drainer がリレー ログからバイナリログを消費するトリガー シナリオ {#trigger-scenarios-where-drainer-consumes-binlogs-from-the-relay-log}

Drainerの起動時に、上流クラスターの Placement Driver (PD) への接続に失敗し、チェックポイントで`consistent = false`を検出すると、 Drainer はリレー ログを読み取り、下流クラスターを一貫した状態に復元しようとします。その後、 Drainerプロセスはチェックポイント`consistent`を`true`に設定して終了します。

### リレーログの GC メカニズム {#gc-mechanism-of-relay-log}

データがダウンストリームにレプリケートされる前に、 Drainer はリレー ログ ファイルにデータを書き込みます。リレー ログ ファイルのサイズが 10 MB (デフォルト) に達し、現在のトランザクションのbinlogデータが完全に書き込まれると、 Drainer は次のリレー ログ ファイルへのデータの書き込みを開始します。 Drainer は、データをダウンストリームに正常に複製した後、データが複製されたリレー ログ ファイルを自動的にクリーンアップします。現在データが書き込まれているリレー ログはクリーンアップされません。

## コンフィグレーション {#configuration}

リレー ログを有効にするには、次の構成をDrainerに追加します。

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
