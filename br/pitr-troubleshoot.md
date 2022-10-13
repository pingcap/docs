---
title: Troubleshoot Log Backup
summary: Learn about common problems of log backup and how to fix them.
---

# ログ バックアップのトラブルシューティング {#troubleshoot-log-backup}

このドキュメントでは、ログ バックアップ中の一般的な問題とその解決策をまとめています。

## <code>br restore point</code>コマンドを使用してダウンストリーム クラスターを復元した後、TiFlash からデータにアクセスできません。私は何をすべきか？ {#after-restoring-a-downstream-cluster-using-the-code-br-restore-point-code-command-data-cannot-be-accessed-from-tiflash-what-should-i-do}

v6.2.0 では、PITR はクラスターの TiFlash レプリカの復元をサポートしていません。データを復元した後、次のステートメントを実行して、スキーマまたはテーブルの TiFlash レプリカを設定する必要があります。

```sql
ALTER TABLE table_name SET TIFLASH REPLICA @count;
```

v6.3.0 以降のバージョンでは、PITR がデータの復元を完了した後、BR は、対応する時間の上流クラスター内の TiFlash レプリカの数に従って、 `ALTER TABLE SET TIFLASH REPLICA`の DDL ステートメントを自動的に実行します。次の SQL ステートメントを使用して、TiFlash レプリカの設定を確認できます。

```sql
SELECT * FROM INFORMATION_SCHEMA.tiflash_replica;
```

> **ノート：**
>
> 現在、PITR は、復元段階での TiFlash へのデータの直接書き込みをサポートしていません。したがって、PITR がデータの復元を完了した直後は、TiFlash レプリカは使用できません。代わりに、TiKV ノードからデータがレプリケートされるまで、一定期間待機する必要があります。レプリケーションの進行状況を確認するには、 `INFORMATION_SCHEMA.tiflash_replica`テーブルの`progress`情報を確認します。

## ログ バックアップ タスクの<code>status</code>が<code>ERROR</code>になった場合はどうすればよいですか? {#what-should-i-do-if-the-code-status-code-of-a-log-backup-task-becomes-code-error-code}

ログ バックアップ タスク中に失敗し、再試行後に回復できない場合、タスク ステータスは`ERROR`になります。次に例を示します。

```shell
br log status --pd x.x.x.x:2379

● Total 1 Tasks.
> #1 <
                    name: task1
                  status: ○ ERROR
                   start: 2022-07-25 13:49:02.868 +0000
                     end: 2090-11-18 14:07:45.624 +0000
                 storage: s3://tmp/br-log-backup0ef49055-5198-4be3-beab-d382a2189efb/Log
             speed(est.): 0.00 ops/s
      checkpoint[global]: 2022-07-25 14:46:50.118 +0000; gap=11h31m29s
          error[store=1]: KV:LogBackup:RaftReq
error-happen-at[store=1]: 2022-07-25 14:54:44.467 +0000; gap=11h23m35s
  error-message[store=1]: retry time exceeds: and error failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }: failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }: failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }
```

この問題を解決するには、エラー メッセージで原因を確認し、指示に従ってください。問題が解決したら、次のコマンドを実行してタスクを再開します。

```shell
br log resume --task-name=task1 --pd x.x.x.x:2379
```

バックアップ タスクが再開されたら、 `br log status`を使用してステータスを確認できます。タスクのステータスが`NORMAL`になると、バックアップ タスクは続行されます。

```shell
● Total 1 Tasks.
> #1 <
              name: task1
            status: ● NORMAL
             start: 2022-07-25 13:49:02.868 +0000
               end: 2090-11-18 14:07:45.624 +0000
           storage: s3://tmp/br-log-backup0ef49055-5198-4be3-beab-d382a2189efb/Log
       speed(est.): 15509.75 ops/s
checkpoint[global]: 2022-07-25 14:46:50.118 +0000; gap=6m28s
```

> **ノート：**
>
> この機能は、複数のバージョンのデータをバックアップします。長時間のバックアップ タスクが失敗し、ステータスが`ERROR`になると、このタスクのチェックポイント データは`safe point`に設定され、 `safe point`のデータは 24 時間以内にガベージ コレクションされません。したがって、エラーが再開された後、バックアップ タスクは最後のチェックポイントから続行されます。タスクが 24 時間以上失敗し、最後のチェックポイント データがガベージ コレクションされている場合、タスクを再開するとエラーが報告されます。この場合、最初にタスクを停止してから新しいバックアップ タスクを開始する`br log stop`コマンドしか実行できません。

## <code>br log resume</code>コマンドを使用して中断されたタスクを再開するときに、エラー メッセージ<code>ErrBackupGCSafepointExceeded</code>が返された場合はどうすればよいですか? {#what-should-i-do-if-the-error-message-code-errbackupgcsafepointexceeded-code-is-returned-when-using-the-code-br-log-resume-code-command-to-resume-the-suspended-task}

```shell
Error: failed to check gc safePoint, checkpoint ts 433177834291200000: GC safepoint 433193092308795392 exceed TS 433177834291200000: [BR:Backup:ErrBackupGCSafepointExceeded]backup GC safepoint exceeded
```

ログ バックアップ タスクを一時停止した後、MVCC データがガベージ コレクションされるのを防ぐために、一時停止中のタスク プログラムは、現在のチェックポイントをサービス セーフポイントとして自動的に設定します。これにより、24 時間以内に生成された MVCC データを確実に残すことができます。バックアップ チェックポイントの MVCC データが 24 時間以上生成されている場合、チェックポイントのデータはガベージ コレクションされ、バックアップ タスクは再開できません。

この問題に対処するには、 `br log stop`を使用して現在のタスクを削除し、 `br log start`を使用してログ バックアップ タスクを作成します。同時に、後続の PITR のフル バックアップを実行できます。
