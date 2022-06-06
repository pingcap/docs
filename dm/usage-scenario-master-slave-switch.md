---
title: Switch DM-worker Connection between Upstream MySQL Instances
summary: Learn how to switch the DM-worker connection between upstream MySQL instances.
---

# アップストリームMySQLインスタンス間のDM-worker接続の切り替え {#switch-dm-worker-connection-between-upstream-mysql-instances}

DM-workerが接続するアップストリームMySQLインスタンスでダウンタイムのメンテナンスが必要な場合、またはインスタンスが予期せずクラッシュした場合は、DM-worker接続を同じ移行グループ内の別のMySQLインスタンスに切り替える必要があります。

> **ノート：**
>
> -   DM-worker接続を、同じプライマリ-セカンダリ移行クラスタ内のインスタンスのみに切り替えることができます。
> -   新しく接続するMySQLインスタンスには、DM-workerが必要とするbinlogが必要です。
> -   DM-workerはGTIDセットモードで動作する必要があります。つまり、対応するソース構成ファイルで`enable-gtid: true`を指定する必要があります。
> -   接続スイッチは、次の2つのシナリオのみをサポートします。各シナリオの手順に厳密に従ってください。そうしないと、新しく接続されたMySQLインスタンスに従ってDMクラスタを再デプロイし、データ移行タスクを最初からやり直す必要がある場合があります。

GTIDセットの詳細については、 [MySQLドキュメント](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html#replication-gtids-concepts-gtid-sets)を参照してください。

## 仮想IPを介したDM-worker接続の切り替え {#switch-dm-worker-connection-via-virtual-ip}

DM-workerが仮想IP（VIP）を介してアップストリームMySQLインスタンスに接続する場合、VIP接続を別のMySQLインスタンスに切り替えることは、アップストリーム接続アドレスを変更せずに、DM-workerに接続されたMySQLインスタンスを切り替えることを意味します。

> **ノート：**
>
> このシナリオでは、DMに必要な変更を加えます。そうしないと、VIP接続を別のMySQLインスタンスに切り替えるときに、DMが新しいMySQLインスタンスと古いMySQLインスタンスに同時に異なる接続で接続する可能性があります。この状況では、DMに複製されたbinlogは、DMが受信する他のアップストリームステータスと一致しないため、予測できない異常やデータの損傷が発生します。

1つのアップストリームMySQLインスタンス（DM-workerがVIPを介してそれに接続する場合）を別のインスタンスに切り替えるには、次の手順を実行します。

1.  `query-status`コマンドを使用して、binlogレプリケーションの現在の処理装置がダウンストリームに複製したbinlogに対応するGTIDセット（ `syncerBinlogGtid` ）を取得します。セットを`gtid-S`としてマークします。
2.  新しいMySQLインスタンスで`SELECT @@GLOBAL.gtid_purged;`コマンドを使用して、パージされたbinlogに対応するGTIDセットを取得します。セットを`gtid-P`としてマークします。
3.  新しいMySQLインスタンスで`SELECT @@GLOBAL.gtid_executed;`コマンドを使用して、正常に実行されたすべてのトランザクションに対応するGTIDセットを取得します。セットを`gtid-E`としてマークします。
4.  以下の条件を満たしていることを確認してください。そうしないと、DM-work接続を新しいMySQLインスタンスに切り替えることができません。
    -   `gtid-S`には`gtid-P`が含まれます。 `gtid-P`は空にすることができます。
    -   `gtid-E`には`gtid-S`が含まれます。
5.  `pause-task`を使用して、データ移行の実行中のすべてのタスクを一時停止します。
6.  新しいMySQLインスタンスに向けるようにVIPを変更します。
7.  `resume-task`を使用して、前の移行タスクを再開します。

## DM-workerが接続するアップストリームMySQLインスタンスのアドレスを変更します {#change-the-address-of-the-upstream-mysql-instance-that-dm-worker-connects-to}

DM-workerの構成を変更して、DM-workerをアップストリームの新しいMySQLインスタンスに接続するには、次の手順を実行します。

1.  `query-status`コマンドを使用して、binlogレプリケーションの現在の処理装置がダウンストリームに複製したbinlogに対応するGTIDセット（ `syncerBinlogGtid` ）を取得します。このセットを`gtid-S`としてマークします。
2.  新しいMySQLインスタンスで`SELECT @@GLOBAL.gtid_purged;`コマンドを使用して、パージされたbinlogに対応するGTIDセットを取得します。このセットを`gtid-P`としてマークします。
3.  新しいMySQLインスタンスで`SELECT @@GLOBAL.gtid_executed;`コマンドを使用して、正常に実行されたすべてのトランザクションに対応するGTIDセットを取得します。このセットを`gtid-E`としてマークします。
4.  以下の条件を満たしていることを確認してください。そうしないと、DM-work接続を新しいMySQLインスタンスに切り替えることができません。
    -   `gtid-S`には`gtid-P`が含まれます。 `gtid-P`は空にすることができます。
    -   `gtid-E`には`gtid-S`が含まれます。
5.  `stop-task`を使用して、データ移行の実行中のすべてのタスクを停止します。
6.  `operator-source stop`コマンドを使用して、古いMySQLインスタンスのアドレスに対応するソース構成をDMクラスタから削除します。
7.  ソース構成ファイルのMySQLインスタンスのアドレスを更新し、 `operate-source create`コマンドを使用してDMクラスタに新しいソース構成を再ロードします。
8.  `start-task`を使用して、移行タスクを再開します。
