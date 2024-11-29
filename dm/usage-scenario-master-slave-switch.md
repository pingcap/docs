---
title: Switch DM-worker Connection between Upstream MySQL Instances
summary: アップストリーム MySQL インスタンス間で DM ワーカー接続を切り替える方法を学習します。
---

# アップストリーム MySQL インスタンス間の DM ワーカー接続を切り替える {#switch-dm-worker-connection-between-upstream-mysql-instances}

DM-worker が接続するアップストリーム MySQL インスタンスでダウンタイム メンテナンスが必要になった場合、またはインスタンスが予期せずクラッシュした場合は、DM-worker 接続を同じ移行グループ内の別の MySQL インスタンスに切り替える必要があります。

> **注記：**
>
> -   DM ワーカー接続は、同じプライマリ - セカンダリ移行クラスター内のインスタンスにのみ切り替えることができます。
> -   新しく接続する MySQL インスタンスには、DM-worker に必要なbinlogが必要です。
> -   DM ワーカーは GTID セット モードで動作する必要があります。つまり、対応するソース構成ファイルで`enable-gtid: true`指定する必要があります。
> -   接続スイッチは、次の 2 つのシナリオのみをサポートします。各シナリオの手順に厳密に従ってください。そうしないと、新しく接続された MySQL インスタンスに従って DM クラスターを再デプロイし、データ移行タスクを最初からやり直す必要がある場合があります。

GTIDセットの詳細については[MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids-concepts.html#replication-gtids-concepts-gtid-sets)を参照してください。

## 仮想IP経由でDMワーカー接続を切り替える {#switch-dm-worker-connection-via-virtual-ip}

DM-worker が仮想 IP (VIP) を介してアップストリーム MySQL インスタンスに接続する場合、VIP 接続を別の MySQL インスタンスに切り替えると、アップストリーム接続アドレスは変更されずに、DM-worker に接続されている MySQL インスタンスが切り替わります。

> **注記：**
>
> このシナリオでは、DM に必要な変更を加えます。そうしないと、VIP 接続を別の MySQL インスタンスに切り替えるときに、DM が新しい MySQL インスタンスと古い MySQL インスタンスに同時に異なる接続で接続する可能性があります。この状況では、DM にレプリケートされたbinlogは、DM が受信する他のアップストリーム ステータスと一致しないため、予期しない異常が発生し、データが損傷することもあります。

あるアップストリーム MySQL インスタンス (DM ワーカーが VIP 経由で接続する場合) を別のインスタンスに切り替えるには、次の手順を実行します。

1.  `query-status`コマンドを使用して、binlogレプリケーションの現在の処理単位がダウンストリームに複製したbinlogに対応する GTID セット ( `syncerBinlogGtid` ) を取得します。セットを`gtid-S`としてマークします。
2.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_purged;`コマンドを使用して、削除されたバイナリログに対応する GTID セットを取得します。セットを`gtid-P`としてマークします。
3.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_executed;`コマンドを使用して、正常に実行されたすべてのトランザクションに対応する GTID セットを取得します。セットを`gtid-E`としてマークします。
4.  次の条件が満たされていることを確認してください。そうでない場合、DM 作業接続を新しい MySQL インスタンスに切り替えることはできません。
    -   `gtid-S`には`gtid-P`が含まれます。4 `gtid-P`空になる場合があります。
    -   `gtid-E`には`gtid-S`含まれます。
5.  `pause-task`使用すると、データ移行の実行中のすべてのタスクが一時停止されます。
6.  新しい MySQL インスタンスに直接アクセスするように VIP を変更します。
7.  以前の移行タスクを再開するには`resume-task`使用します。

## DM-workerが接続する上流MySQLインスタンスのアドレスを変更する {#change-the-address-of-the-upstream-mysql-instance-that-dm-worker-connects-to}

DM-worker 設定を変更して DM-worker をアップストリームの新しい MySQL インスタンスに接続するには、次の手順を実行します。

1.  `query-status`コマンドを使用して、binlogレプリケーションの現在の処理単位がダウンストリームに複製したbinlogに対応する GTID セット ( `syncerBinlogGtid` ) を取得します。このセットを`gtid-S`としてマークします。
2.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_purged;`コマンドを使用して、削除されたバイナリログに対応する GTID セットを取得します。このセットを`gtid-P`としてマークします。
3.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_executed;`コマンドを使用して、正常に実行されたすべてのトランザクションに対応する GTID セットを取得します。このセットを`gtid-E`としてマークします。
4.  次の条件が満たされていることを確認してください。そうでない場合、DM 作業接続を新しい MySQL インスタンスに切り替えることはできません。
    -   `gtid-S`には`gtid-P`が含まれます。4 `gtid-P`空になる場合があります。
    -   `gtid-E`には`gtid-S`含まれます。
5.  `stop-task`使用すると、データ移行の実行中のすべてのタスクが停止します。
6.  `operator-source stop`コマンドを使用して、古い MySQL インスタンスのアドレスに対応するソース構成を DM クラスターから削除します。
7.  ソース構成ファイル内の MySQL インスタンスのアドレスを更新し、 `operate-source create`コマンドを使用して DM クラスターに新しいソース構成を再ロードします。
8.  移行タスクを再開するには`start-task`使用します。
