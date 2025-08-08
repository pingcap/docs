---
title: TiDB Incremental Backup and Restore Guide
summary: 増分データは、開始スナップショットと終了スナップショット間の差分データとDDLです。これによりバックアップボリュームが削減され、増分バックアップにはtidb_gc_life_time`の設定が必要になります。増分バックアップには`tiup br backup`と`--lastbackupts`オプションを使用し、増分データを復元する前に以前のデータがすべて復元されていることを確認してください。
---

# TiDB 増分バックアップとリストアガイド {#tidb-incremental-backup-and-restore-guide}

TiDBクラスターの増分データは、期間の開始スナップショットと終了スナップショット間の差分データ、およびこの期間に生成されたDDLです。完全（スナップショット）バックアップデータと比較して増分データはサイズが小さいため、スナップショットバックアップの補足として機能し、バックアップデータの容量を削減します。増分バックアップを実行するには、指定された期間内に生成されたMVCCデータが[TiDB GCメカニズム](/garbage-collection-overview.md)によってガベージコレクションされないようにしてください。たとえば、1時間ごとに増分バックアップを実行するには、 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) 1時間より大きい値に設定する必要があります。

> **警告：**
>
> この機能の開発は停止しています。代替として[ログバックアップとPITR](/br/br-pitr-guide.md)使用することをお勧めします。

## 制限事項 {#limitations}

増分バックアップの復元では、増分 DDL ステートメントをフィルター処理するためにバックアップ時点のデータベース テーブルのスナップショットを使用するため、増分バックアップ プロセス中に削除されたテーブルはデータの復元後も存在する可能性があり、手動で削除する必要があります。

増分バックアップでは、テーブル名の一括変更はサポートされていません。増分バックアップ中にテーブル名の一括変更が行われた場合、データの復元が失敗する可能性があります。テーブル名の一括変更後に完全バックアップを実行し、復元時に最新の完全バックアップを使用して増分データを置き換えることをお勧めします。

バージョン8.3.0以降、増分バックアップと後続のログバックアップの互換性を制御するための構成パラメータ`--allow-pitr-from-incremental`が導入されました。デフォルト値は`true`で、増分バックアップと後続のログバックアップの互換性があることを意味します。

-   デフォルト値`true`ままにしておくと、増分リストアを開始する前に、再生が必要なDDLが厳密にチェックされます。このモードでは、 `ADD INDEX` 、 `MODIFY COLUMN` 、 `REORG PARTITION`まだサポートされていません。増分バックアップとログバックアップを併用する場合は、増分バックアッププロセス中に、前述のDDLが存在しないことを確認してください。そうでない場合、これら3つのDDLを正しく再生できません。

-   リカバリプロセス全体でログ バックアップなしで増分復元を使用する場合は、 `--allow-pitr-from-incremental`から`false`設定して増分リカバリ フェーズでのチェックをスキップできます。

## 増分データをバックアップする {#back-up-incremental-data}

増分データをバックアップするには、 `tiup br backup`コマンドを、**最終バックアップのタイムスタンプ**`--lastbackupts`を指定して実行します。これにより、br コマンドラインツールは`lastbackupts`から現在時刻の間に生成された増分データを自動的にバックアップします。9 `--lastbackupts`取得するには、 `validate`コマンドを実行します。以下は例です。

```shell
LAST_BACKUP_TS=`tiup br validate decode --field="end-version" --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"| tail -n1`
```

次のコマンドは、 `(LAST_BACKUP_TS, current PD timestamp]`とこの期間中に生成された DDL 間の増分データをバックアップします。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330/incr?access-key=${access-key}&secret-access-key=${secret-access-key}" \
--lastbackupts ${LAST_BACKUP_TS} \
--ratelimit 128
```

-   `--lastbackupts` : 最後のバックアップのタイムスタンプ。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV あたりの**最大速度 (MiB/秒)。
-   `storage` : バックアップデータのstorageパス。増分バックアップデータは、前回のスナップショットバックアップとは異なるパスに保存する必要があります。上記の例では、増分バックアップデータはフルバックアップデータの下の`incr`ディレクトリに保存されます。詳細は[外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

## 増分データを復元する {#restore-incremental-data}

増分データをリストアする際は、 `LAST_BACKUP_TS`より前にバックアップされたすべてのデータがターゲットクラスターにリストアされていることを確認してください。また、増分リストアはデータを更新するため、リストア中に他の書き込みが行われていないことを確認する必要があります。そうしないと、競合が発生する可能性があります。

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
