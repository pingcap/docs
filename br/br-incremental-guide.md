---
title: TiDB Incremental Backup and Restore Guide
summary: Learns about how to perform incremental backup and restore in TiDB.
---

# TiDB 増分バックアップおよび復元ガイド {#tidb-incremental-backup-and-restore-guide}

TiDB クラスターの増分データは、期間の開始スナップショットと終了スナップショットの間の差分データ、およびこの期間中に生成された DDL です。増分データは完全 (スナップショット) バックアップ データと比較してデータ量が小さいため、スナップショット バックアップを補完するものであり、バックアップ データの量を削減します。増分バックアップを実行するには、指定された期間内に生成された MVCC データが[TiDB GC メカニズム](/garbage-collection-overview.md)によってガベージ コレクションされていないことを確認してください。たとえば、増分バックアップを 1 時間ごとに実行するには、 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) 1 時間より大きい値に設定する必要があります。

> **警告：**
>
> この機能の開発は停止されました。代わりに[ログバックアップとPITR](/br/br-pitr-guide.md)を使用することをお勧めします。

## 増分データをバックアップする {#back-up-incremental-data}

増分データをバックアップするには、**最後のバックアップのタイムスタンプ**`--lastbackupts`を指定して`br backup`コマンドを実行します。このようにして、br コマンド ライン ツールは、 `lastbackupts`から現在までの間に生成された増分データを自動的にバックアップします。 `--lastbackupts`取得するには、 `validate`コマンドを実行します。以下は例です。

```shell
LAST_BACKUP_TS=`tiup br validate decode --field="end-version" --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"| tail -n1`
```

次のコマンドは、 `(LAST_BACKUP_TS, current PD timestamp]`とこの期間中に生成された DDL の間の増分データをバックアップします。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330/incr?access-key=${access-key}&secret-access-key=${secret-access-key}" \
--lastbackupts ${LAST_BACKUP_TS} \
--ratelimit 128
```

-   `--lastbackupts` : 最後のバックアップのタイムスタンプ。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV ごとの**最大速度 (MiB/秒)。
-   `storage` : バックアップデータのstorageパス。増分バックアップ データは、以前のスナップショット バックアップとは別のパスに保存する必要があります。前の例では、増分バックアップ データは完全バックアップ データの下の`incr`ディレクトリに保存されます。詳細は[外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。

## 増分データの復元 {#restore-incremental-data}

増分データを復元するときは、 `LAST_BACKUP_TS`より前にバックアップされたすべてのデータがターゲット クラスターに復元されていることを確認してください。また、増分復元ではデータが更新されるため、復元中に他の書き込みがないことを確認する必要があります。そうしないと、競合が発生する可能性があります。

次のコマンドは、 `backup-101/snapshot-202209081330`ディレクトリに保存されている完全バックアップ データを復元します。

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

次のコマンドは、 `backup-101/snapshot-202209081330/incr`ディレクトリに保存されている増分バックアップ データを復元します。

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330/incr?access-key=${access-key}&secret-access-key=${secret-access-key}"
```
