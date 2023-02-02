---
title: TiDB Binlog Relay Log
summary: Learn how to use relay log to maintain data consistency in extreme cases.
---

# TiDB Binlog {#tidb-binlog-relay-log}

バイナリログを複製するとき、 Drainerは上流からトランザクションを分割し、分割されたトランザクションを同時に下流に複製します。

アップストリーム クラスターが利用できず、 Drainerが異常終了するという極端なケースでは、ダウンストリーム クラスター (MySQL または TiDB) がデータの一貫性のない中間状態にある可能性があります。このような場合、 Drainerはリレー ログを使用して、ダウンストリーム クラスターが一貫した状態であることを確認できます。

## Drainerレプリケーション中の一貫した状態 {#consistent-state-during-drainer-replication}

ダウンストリーム クラスタが一貫した状態に達するということは、ダウンストリーム クラスタのデータが`tidb_snapshot = ts`を設定するアップストリームのスナップショットと同じであることを意味します。

チェックポイントの一貫性とは、 Drainerチェックポイントがレプリケーションの一貫した状態を`consistent`に保存することを意味します。 Drainerが実行されると、 `consistent`は`false`になります。 Drainerが正常に終了した後、 `consistent`が`true`に設定されます。

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

Drainerがリレー ログを有効にすると、最初に binlog イベントがディスクに書き込まれ、次にそのイベントがダウンストリーム クラスターにレプリケートされます。

アップストリーム クラスタが利用できない場合、 Drainerはリレー ログを読み取ることで、ダウンストリーム クラスタを一貫した状態に復元できます。

> **ノート：**
>
> リレー ログ データが同時に失われる場合、この方法は機能しませんが、その発生率は非常に低いです。さらに、ネットワーク ファイル システムを使用して、リレー ログのデータの安全性を確保できます。

### Drainerがリレー ログからバイナリログを消費するトリガー シナリオ {#trigger-scenarios-where-drainer-consumes-binlogs-from-the-relay-log}

Drainerの起動時に、上流クラスターの Placement Driver (PD) への接続に失敗し、チェックポイントで`consistent = false`を検出すると、 Drainerはリレー ログを読み取り、下流クラスターを一貫した状態に復元しようとします。その後、 Drainerプロセスはチェックポイント`consistent`を`true`に設定して終了します。

### リレーログの GC メカニズム {#gc-mechanism-of-relay-log}

データがダウンストリームにレプリケートされる前に、 Drainerはリレー ログ ファイルにデータを書き込みます。リレー ログ ファイルのサイズが 10 MB (デフォルト) に達し、現在のトランザクションのバイナリ ログ データが完全に書き込まれると、 Drainerは次のリレー ログ ファイルへのデータの書き込みを開始します。 Drainerは、データをダウンストリームに正常に複製した後、データが複製されたリレー ログ ファイルを自動的にクリーンアップします。現在データが書き込まれているリレー ログはクリーンアップされません。

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
