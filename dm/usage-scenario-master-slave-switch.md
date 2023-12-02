---
title: Switch DM-worker Connection between Upstream MySQL Instances
summary: Learn how to switch the DM-worker connection between upstream MySQL instances.
---

# アップストリーム MySQL インスタンス間の DM ワーカー接続を切り替える {#switch-dm-worker-connection-between-upstream-mysql-instances}

DM ワーカーが接続する上流の MySQL インスタンスでダウンタイム メンテナンスが必要な場合、またはインスタンスが予期せずクラッシュした場合は、DM ワーカーの接続を同じ移行グループ内の別の MySQL インスタンスに切り替える必要があります。

> **注記：**
>
> -   DM ワーカー接続を、同じプライマリ - セカンダリ移行クラスター内のインスタンスにのみ切り替えることができます。
> -   新しく接続する MySQL インスタンスには、DM ワーカーが必要とするbinlogが必要です。
> -   DM ワーカーは GTID セット モードで動作する必要があります。つまり、対応するソース構成ファイルで`enable-gtid: true`を指定する必要があります。
> -   接続スイッチは、次の 2 つのシナリオのみをサポートします。各シナリオの手順に厳密に従ってください。それ以外の場合は、新しく接続された MySQL インスタンスに従って DM クラスターを再デプロイし、データ移行タスクを最初からやり直す必要がある場合があります。

GTID セットの詳細については、 [MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids-concepts.html#replication-gtids-concepts-gtid-sets)を参照してください。

## 仮想 IP 経由で DM とワーカーの接続を切り替える {#switch-dm-worker-connection-via-virtual-ip}

DM-worker が仮想 IP (VIP) 経由で上流の MySQL インスタンスに接続している場合、VIP 接続を別の MySQL インスタンスに切り替えることは、上流の接続アドレスを変更せずに、DM-worker に接続されている MySQL インスタンスを切り替えることを意味します。

> **注記：**
>
> このシナリオでは、DM に必要な変更を加えます。そうしないと、VIP 接続を別の MySQL インスタンスに切り替えると、DM が異なる接続で新しい MySQL インスタンスと古い MySQL インスタンスに同時に接続する可能性があります。この状況では、DM にレプリケートされたbinlogは、DM が受信する他のアップストリーム ステータスと一貫性がなく、予測できない異常が発生し、さらにはデータ損傷が発生します。

1 つのアップストリーム MySQL インスタンス (DM ワーカーが VIP 経由で接続する場合) を別のインスタンスに切り替えるには、次の手順を実行します。

1.  `query-status`コマンドを使用して、binlogレプリケーションの現在の処理ユニットがダウンストリームにレプリケートしたbinlogに対応する GTID セット ( `syncerBinlogGtid` ) を取得します。セットを`gtid-S`としてマークします。
2.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_purged;`コマンドを使用して、パージされたバイナリログに対応する GTID セットを取得します。セットを`gtid-P`としてマークします。
3.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_executed;`コマンドを使用して、正常に実行されたすべてのトランザクションに対応する GTID セットを取得します。セットを`gtid-E`としてマークします。
4.  以下の条件が満たされていることを確認してください。そうしないと、DM ワーク接続を新しい MySQL インスタンスに切り替えることができません。
    -   `gtid-S`は`gtid-P`含まれます。 `gtid-P`空でも構いません。
    -   `gtid-E`は`gtid-S`含まれます。
5.  データ移行の実行中のタスクをすべて一時停止するには、 `pause-task`を使用します。
6.  新しい MySQL インスタンスを宛先とするように VIP を変更します。
7.  以前の移行タスクを再開するには、 `resume-task`を使用します。

## DM-worker が接続する上流の MySQL インスタンスのアドレスを変更します。 {#change-the-address-of-the-upstream-mysql-instance-that-dm-worker-connects-to}

DM ワーカーの構成を変更して、DM ワーカーがアップストリームの新しい MySQL インスタンスに接続できるようにするには、次の手順を実行します。

1.  `query-status`コマンドを使用して、binlogレプリケーションの現在の処理ユニットがダウンストリームにレプリケートしたbinlogに対応する GTID セット ( `syncerBinlogGtid` ) を取得します。このセットを`gtid-S`としてマークします。
2.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_purged;`コマンドを使用して、パージされたバイナリログに対応する GTID セットを取得します。このセットを`gtid-P`としてマークします。
3.  新しい MySQL インスタンスで`SELECT @@GLOBAL.gtid_executed;`コマンドを使用して、正常に実行されたすべてのトランザクションに対応する GTID セットを取得します。このセットを`gtid-E`としてマークします。
4.  以下の条件が満たされていることを確認してください。そうしないと、DM ワーク接続を新しい MySQL インスタンスに切り替えることができません。
    -   `gtid-S`は`gtid-P`含まれます。 `gtid-P`空でも構いません。
    -   `gtid-E`は`gtid-S`含まれます。
5.  データ移行の実行中のタスクをすべて停止するには、 `stop-task`を使用します。
6.  `operator-source stop`コマンドを使用して、古い MySQL インスタンスのアドレスに対応するソース構成を DM クラスターから削除します。
7.  ソース構成ファイル内の MySQL インスタンスのアドレスを更新し、 `operate-source create`コマンドを使用して DM クラスター内の新しいソース構成を再ロードします。
8.  移行タスクを再開するには、 `start-task`を使用します。
