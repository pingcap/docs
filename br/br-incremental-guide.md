---
title: TiDB Incremental Backup and Restore Guide
summary: Learns about how to perform incremental backup and restore in TiDB.
---

# TiDB 増分バックアップおよび復元ガイド {#tidb-incremental-backup-and-restore-guide}

TiDB クラスターの増分データは、期間の開始スナップショットと終了スナップショットの間の差分データと、この期間中に生成された DDL です。フル (スナップショット) バックアップ データと比較して、増分データは小さいため、バックアップ データの量を減らすスナップショット バックアップを補完します。増分バックアップを実行するには、指定された期間内に生成された MVCC データが[TiDB GC メカニズム](/garbage-collection-overview.md)によってガベージ コレクションされていないことを確認してください。たとえば、1 時間ごとに増分バックアップを実行するには、 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) 1 時間より大きい値に設定する必要があります。

> **警告：**
>
> この機能の開発は停止しています。代わりに[ログのバックアップと PITR](/br/br-pitr-guide.md)を使用することをお勧めします。

## 増分データのバックアップ {#back-up-incremental-data}

増分データをバックアップするには、**最後のバックアップ タイムスタンプ**`--lastbackupts`を指定して`br backup`コマンドを実行します。このように、br コマンドライン ツールは、 `lastbackupts`から現在までの間に生成された増分データを自動的にバックアップします。 `--lastbackupts`取得するには、 `validate`コマンドを実行します。次に例を示します。

```shell
LAST_BACKUP_TS=`tiup br validate decode --field="end-version" --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"| tail -n1`
```

次のコマンドは、 `(LAST_BACKUP_TS, current PD timestamp]`からこの期間中に生成された DDL までの増分データをバックアップします。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330/incr?access-key=${access-key}&secret-access-key=${secret-access-key}" \
--lastbackupts ${LAST_BACKUP_TS} \
--ratelimit 128
```

-   `--lastbackupts` : 最後のバックアップのタイムスタンプ。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV ごとの**最大速度 (MiB/秒)。
-   `storage` : バックアップ データのstorageパス。増分バックアップ データは、以前のスナップショット バックアップとは別のパスに保存する必要があります。前の例では、増分バックアップ データは、フル バックアップ データの下の`incr`ディレクトリに保存されます。詳細については、 [バックアップstorageURL の構成](/br/backup-and-restore-storages.md#url-format)を参照してください。

## 増分データの復元 {#restore-incremental-data}

増分データを復元する場合は、 `LAST_BACKUP_TS`より前にバックアップされたすべてのデータがターゲット クラスターに復元されていることを確認してください。また、増分復元ではデータが更新されるため、復元中に他の書き込みが行われないようにする必要があります。そうしないと、競合が発生する可能性があります。

次のコマンドは、 `backup-101/snapshot-202209081330`ディレクトリに格納されている完全バックアップ データを復元します。

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

次のコマンドは、 `backup-101/snapshot-202209081330/incr`ディレクトリに保存されている増分バックアップ データを復元します。

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330/incr?access-key=${access-key}&secret-access-key=${secret-access-key}"
```
