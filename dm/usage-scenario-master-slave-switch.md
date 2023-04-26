---
title: Switch DM-worker Connection between Upstream MySQL Instances
summary: Learn how to switch the DM-worker connection between upstream MySQL instances.
---

# アップストリーム MySQL インスタンス間の DM-worker 接続の切り替え {#switch-dm-worker-connection-between-upstream-mysql-instances}

DM-worker が接続する上流の MySQL インスタンスでダウンタイム メンテナンスが必要な場合、またはインスタンスが予期せずクラッシュした場合、DM-worker 接続を同じ移行グループ内の別の MySQL インスタンスに切り替える必要があります。

> **ノート：**
>
> -   DM-worker 接続を、同じプライマリ - セカンダリ移行クラスター内のインスタンスのみに切り替えることができます。
> -   新しく接続する MySQL インスタンスには、DM-worker が必要とするbinlogが必要です。
> -   DM-worker は GTID セット モードで動作する必要があります。つまり、対応するソース構成ファイルで`enable-gtid: true`を指定する必要があります。
> -   接続スイッチは、次の 2 つのシナリオのみをサポートします。各シナリオの手順に厳密に従ってください。そうしないと、新しく接続された MySQL インスタンスに従って DM クラスターを再デプロイし、データ移行タスクを最初からやり直す必要がある場合があります。

GTID セットの詳細については、 [MySQL ドキュメント](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html#replication-gtids-concepts-gtid-sets)を参照してください。

## 仮想 IP 経由で DM-worker 接続を切り替える {#switch-dm-worker-connection-via-virtual-ip}

DM-worker が仮想 IP (VIP) 経由で上流の MySQL インスタンスに接続する場合、VIP 接続を別の MySQL インスタンスに切り替えることは、上流の接続アドレスを変更せずに、DM-worker に接続されている MySQL インスタンスを切り替えることを意味します。

> **ノート：**
>
> このシナリオでは、DM に必要な変更を加えます。そうしないと、VIP 接続を別の MySQL インスタンスに切り替えると、DM が新しいおよび古い MySQL インスタンスに同時に異なる接続で接続する可能性があります。この状況では、DM にレプリケートされたbinlogは、DM が受け取る他のアップストリーム ステータスと一致せず、予測できない異常やデータの損傷さえ引き起こします。

アップストリームの MySQL インスタンス (DM ワーカーが VIP 経由で接続する場合) を別のインスタンスに切り替えるには、次の手順を実行します。

1.  `query-status`コマンドを使用して、binlogレプリケーションの現在の処理単位がダウンストリームにレプリケートしたbinlogに対応する GTID セット ( `syncerBinlogGtid` ) を取得します。セットを`gtid-S`としてマークします。
2.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_purged;`コマンドを使用して、パージされたバイナリログに対応する GTID セットを取得します。セットを`gtid-P`としてマークします。
3.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_executed;`コマンドを使用して、正常に実行されたすべてのトランザクションに対応する GTID セットを取得します。セットを`gtid-E`としてマークします。
4.  以下の条件を満たしていることを確認してください。そうしないと、DM-work 接続を新しい MySQL インスタンスに切り替えることができません。
    -   `gtid-S`は`gtid-P`含まれます。 `gtid-P`空にすることができます。
    -   `gtid-E`は`gtid-S`含まれます。
5.  実行中のデータ移行タスクをすべて一時停止するには、 `pause-task`を使用します。
6.  VIP を変更して、新しい MySQL インスタンスに向けます。
7.  前の移行タスクを再開するには、 `resume-task`を使用します。

## DM-worker が接続する上流の MySQL インスタンスのアドレスを変更します {#change-the-address-of-the-upstream-mysql-instance-that-dm-worker-connects-to}

DM-worker 設定を変更して DM-worker をアップストリームの新しい MySQL インスタンスに接続するには、次の手順を実行します。

1.  `query-status`コマンドを使用して、binlogレプリケーションの現在の処理単位がダウンストリームにレプリケートしたbinlogに対応する GTID セット ( `syncerBinlogGtid` ) を取得します。このセットを`gtid-S`としてマークします。
2.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_purged;`コマンドを使用して、パージされたバイナリログに対応する GTID セットを取得します。このセットを`gtid-P`としてマークします。
3.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_executed;`コマンドを使用して、正常に実行されたすべてのトランザクションに対応する GTID セットを取得します。このセットを`gtid-E`としてマークします。
4.  以下の条件を満たしていることを確認してください。そうしないと、DM-work 接続を新しい MySQL インスタンスに切り替えることができません。
    -   `gtid-S`は`gtid-P`含まれます。 `gtid-P`空にすることができます。
    -   `gtid-E`は`gtid-S`含まれます。
5.  実行中のデータ移行タスクをすべて停止するには、 `stop-task`を使用します。
6.  `operator-source stop`コマンドを使用して、古い MySQL インスタンスのアドレスに対応するソース構成を DM クラスターから削除します。
7.  ソース構成ファイルで MySQL インスタンスのアドレスを更新し、 `operate-source create`コマンドを使用して DM クラスターに新しいソース構成をリロードします。
8.  移行タスクを再開するには、 `start-task`を使用します。
