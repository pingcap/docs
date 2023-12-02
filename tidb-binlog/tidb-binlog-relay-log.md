---
title: TiDB Binlog Relay Log
summary: Learn how to use relay log to maintain data consistency in extreme cases.
---

# TiDBBinlogリレー ログ {#tidb-binlog-relay-log}

バイナリログをレプリケートするとき、 Drainer はアップストリームからトランザクションを分割し、分割されたトランザクションをダウンストリームに同時にレプリケートします。

上流のクラスターが利用できず、 Drainer が異常終了するという極端なケースでは、下流のクラスター (MySQL または TiDB) が中間状態になり、データに一貫性がない可能性があります。このような場合、 Drainer はリレー ログを使用して、ダウンストリーム クラスターが一貫した状態にあることを確認できます。

## Drainerレプリケーション中の一貫した状態 {#consistent-state-during-drainer-replication}

下流クラスターが一貫した状態に達すると、下流クラスターのデータが`tidb_snapshot = ts`を設定した上流クラスターのスナップショットと同じであることを意味します。

チェックポイントの一貫性とは、Drainerチェックポイントがレプリケーションの一貫した状態を`consistent`に保存することを意味します。Drainerが実行されると、 `consistent`は`false`になります。 Drainer が正常に終了すると、 `consistent`は`true`に設定されます。

次のように、ダウンストリーム チェックポイント テーブルをクエリできます。

```sql
select * from tidb_binlog.checkpoint;
```

    +---------------------+----------------------------------------------------------------+
    | clusterID           | checkPoint                                                     |
    +---------------------+----------------------------------------------------------------+
    | 6791641053252586769 | {"consistent":false,"commitTS":414529105591271429,"ts-map":{}} |
    +---------------------+----------------------------------------------------------------+

## 実装原則 {#implementation-principles}

Drainer はリレー ログを有効にすると、まずbinlogイベントをディスクに書き込み、次にそのイベントをダウンストリーム クラスターにレプリケートします。

上流のクラスターが使用できない場合、 Drainer はリレー ログを読み取ることで、下流のクラスターを一貫した状態に復元できます。

> **注記：**
>
> リレーログデータも同時に失われた場合、この方法は機能しませんが、その発生率は非常に低いです。さらに、ネットワーク ファイル システムを使用して、リレー ログのデータの安全性を確保できます。

### Drainer がリレー ログからバイナリ ログを消費するトリガー シナリオ {#trigger-scenarios-where-drainer-consumes-binlogs-from-the-relay-log}

Drainerの起動時に、上流クラスターの配置Driver(PD) への接続に失敗し、チェックポイントで`consistent = false`が検出された場合、 Drainer はリレー ログを読み取り、下流クラスターを一貫した状態に復元しようとします。その後、 Drainerプロセスはチェックポイント`consistent`を`true`に設定して終了します。

### リレーログのGC機構 {#gc-mechanism-of-relay-log}

データがダウンストリームにレプリケートされる前に、 Drainer はデータをリレー ログ ファイルに書き込みます。リレー ログ ファイルのサイズが 10 MB (デフォルト) に達し、現在のトランザクションのbinlogデータが完全に書き込まれると、 Drainer は次のリレー ログ ファイルへのデータの書き込みを開始します。 Drainer は、データをダウンストリームに正常にレプリケートすると、データがレプリケートされたリレー ログ ファイルを自動的にクリーンアップします。現在データが書き込まれているリレー ログはクリーンアップされません。

## コンフィグレーション {#configuration}

リレー ログを有効にするには、 Drainerに次の設定を追加します。

    [syncer.relay]
    # It saves the directory of the relay log. The relay log is not enabled if the value is empty.
    # The configuration only comes to effect if the downstream is TiDB or MySQL.
    log-dir = "/dir/to/save/log"
    # The size limit of a single relay log file (unit: byte).
    # When the size of a relay log file reaches this limit, data is written to the next relay log file.
    max-file-size = 10485760
