---
title: TiDB Binlog Relay Log
summary: 極端な場合にリレー ログを使用してデータの一貫性を維持する方法を学習します。
---

# TiDBBinlogリレーログ {#tidb-binlog-relay-log}

バイナリログを複製する場合、 Drainer はアップストリームからトランザクションを分割し、分割されたトランザクションを同時にダウンストリームに複製します。

上流のクラスターが利用できず、 Drainer が異常終了する極端なケースでは、下流のクラスター (MySQL または TiDB) がデータの不整合がある中間状態になる可能性があります。このような場合、 Drainer はリレー ログを使用して下流のクラスターが一貫した状態であることを確認できます。

## Drainerレプリケーション中の一貫した状態 {#consistent-state-during-drainer-replication}

下流のクラスターが一貫した状態に達するということは、下流のクラスターのデータが`tidb_snapshot = ts`に設定された上流のスナップショットと同じであることを意味します。

チェックポイントの一貫性とは、 Drainerチェックポイントがレプリケーションの一貫性のある状態を`consistent`に保存することを意味します。Drainerが実行されると、 `consistent` `false`になります。Drainerが正常に終了すると、 `consistent` `true`に設定されます。

ダウンストリーム チェックポイント テーブルを次のようにクエリできます。

```sql
select * from tidb_binlog.checkpoint;
```

    +---------------------+----------------------------------------------------------------+
    | clusterID           | checkPoint                                                     |
    +---------------------+----------------------------------------------------------------+
    | 6791641053252586769 | {"consistent":false,"commitTS":414529105591271429,"ts-map":{}} |
    +---------------------+----------------------------------------------------------------+

## 実施原則 {#implementation-principles}

Drainer はリレー ログを有効にすると、まずbinlogイベントをディスクに書き込み、次にそのイベントをダウンストリーム クラスターに複製します。

上流のクラスターが利用できない場合、 Drainer はリレー ログを読み取ることで下流のクラスターを一貫した状態に復元できます。

> **注記：**
>
> リレーログデータが同時に失われる場合、この方法は機能しませんが、その発生率は非常に低いです。また、ネットワークファイルシステムを使用して、リレーログのデータ安全性を確保できます。

### Drainer がリレーログからバイナリログを消費するシナリオをトリガーする {#trigger-scenarios-where-drainer-consumes-binlogs-from-the-relay-log}

Drainer が起動すると、上流クラスターの Placement Driver (PD) への接続に失敗し、チェックポイントで`consistent = false`を検出すると、 Drainer はリレー ログを読み取って、下流クラスターを整合性のある状態に復元しようとします。その後、 Drainerプロセスはチェックポイント`consistent`を`true`に設定して終了します。

### リレーログのGCメカニズム {#gc-mechanism-of-relay-log}

データがダウンストリームに複製される前に、 Drainer はリレー ログ ファイルにデータを書き込みます。リレー ログ ファイルのサイズが 10 MB (デフォルト) に達し、現在のトランザクションのbinlogデータが完全に書き込まれると、 Drainer は次のリレー ログ ファイルへのデータの書き込みを開始します。Drainerはダウンストリームへのデータの複製に成功すると、データが複製されたリレー ログ ファイルを自動的にクリーンアップします。現在データが書き込まれているリレー ログはクリーンアップされません。

## コンフィグレーション {#configuration}

リレー ログを有効にするには、 Drainerに次の構成を追加します。

    [syncer.relay]
    # It saves the directory of the relay log. The relay log is not enabled if the value is empty.
    # The configuration only comes to effect if the downstream is TiDB or MySQL.
    log-dir = "/dir/to/save/log"
    # The size limit of a single relay log file (unit: byte).
    # When the size of a relay log file reaches this limit, data is written to the next relay log file.
    max-file-size = 10485760
